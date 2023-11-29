import moviepy.editor as mp
import time
import os
import shutil

audio_flag = 0

def audio_extraction(video_path, audio_path):
    global audio_flag
    
    if not os.path.isdir(audio_path):
        os.makedirs(audio_path)

    n = 0
    while(True):    
        if not os.path.isfile(f"{video_path}/index{n}.ts") and audio_flag <= 20: # ts file이 존재하지 않는 경우
            time.sleep(1)
            audio_flag += 1
            continue
        elif os.path.isfile(f"{video_path}/index{n}.ts") and audio_flag <= 20: # 존재하는 경우
            audio_flag = 0
            clip = mp.VideoFileClip(f"{video_path}/index{n}.ts")
            clip.audio.write_audiofile(f"{audio_path}/index{n}.wav")
            n += 1
        elif audio_flag > 20:
            shutil.rmtree(audio_path)
            break

