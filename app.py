from flask import render_template, Flask, send_from_directory, request, redirect, url_for
import streamlink
import os
import subprocess
import threading
import audio
import time
import caption
import shutil


app = Flask(__name__)

# 각 파일들의 경로
video_folder = "./video"
m3u8_file = "index.m3u8"
audio_folder = "./audio"
caption_folder = "./static/caption"
ffmpeg_path = r"C:\ffmpeg-6.0-essentials_build/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe"

# 영상의 실제 link를 streamlink를 통해 확보
def get_video(url):
    streams = streamlink.streams(url)
    if "best" in streams:
        return streams["best"].url
    else:
        return None


# download_video(url, run_time, chunk_size)
# url과 Process

def download_video(url):
    if not os.path.isdir(video_folder):
        os.makedirs(video_folder)
    
    # ffmpeg -> https://www.gyan.dev/ffmpeg/builds/ -> lastest Release essential_build 설치
    # 압축 해제 후 exe file 3개가 들어있는 bin 폴더를 PAth에 추가
    # --> 시스템 환경 변수 편집 -> 환경변수 -> 시스템변수/PATH -> 해당 bin 폴더를 PATH에 추가
    stream_url = get_video(url)
    if not stream_url:
        pass
    # cmd = f"ffmpeg -i {stream_url} -c:v copy -c:a copy -f hls -hls_time 10 -hls_list_size 0 {os.path.join(video_folder, m3u8_file)}"
    cmd = [ffmpeg_path, "-i", stream_url, "-c:v", "copy", "-c:a", "copy", "-f", "hls", "-hls_time", "10", "-hls_list_size", "0", "C:\Live_stream_v4/video/" + m3u8_file]

    try:
        sub_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    except subprocess.TimeoutExpired:
        sub_proc.kill()
        
 
def delete_video(run_time, video_path):
    time.sleep(run_time)
    try:
        shutil.rmtree(video_path)
        time.sleep(1)
    except:
        pass
    
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        video_link = request.form['video_link']
        get_video(video_link)
        download_thread = threading.Thread(target=download_video, args=(video_link, ))
        extraction_thread = threading.Thread(target = audio.audio_extraction, args=(video_folder, audio_folder, ))
        caption_thread = threading.Thread(target=caption.make_caption, args=(audio_folder, caption_folder, ))
        download_thread.start()
        extraction_thread.start()
        caption_thread.start()
        return redirect(url_for('loading'))
    return render_template('index.html')



# flask 웹페이지 구성


# Main page (유튜브 링크 입력)
@app.route('/video')
def video():
    return render_template('video.html')

# Loading page (최초 영상 다운로드 / 음성 추출 / 자막 생성 등의 대기 시간)
@app.route('/loading')
def loading():
    return render_template('load.html')

# 재생에 필요한 ts 파일을 전송
@app.route('/video/<string:file_name>')
def play_video(file_name):
    video_dir = './video'
    return send_from_directory(video_dir, file_name)


if __name__ == '__main__':
    app.run(host = '127.0.0.1', threaded = True, debug = True, port=8080)
    
    