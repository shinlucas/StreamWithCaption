import speech_recognition as sr
import os
import time
import shutil

recognizer = sr.Recognizer()
caption_flag = 0

def make_caption(audio_path, caption_path):
    global caption_flag
    
    n = 0
    
    if not os.path.isdir(caption_path):
        os.makedirs(caption_path)

    while(True):
        if not os.path.isfile(f"{audio_path}/index{n}.wav") and caption_flag <= 20:
            time.sleep(1)
            caption_flag += 1
            continue
        
        elif os.path.isfile(f"{audio_path}/index{n}.wav") and caption_flag <= 20:
            caption_flag = 0
            with sr.AudioFile(f'{audio_path}/index{n}.wav') as source:
                audio_data = recognizer.record(source)
            print("nnn : ", n)
            try:
                text = recognizer.recognize_google(audio_data, language="ko-KR")
                file = open(f'{caption_path}/index{n}.txt', 'w', encoding="UTF-8")
                file.write(text)
                file.close()
                
                n += 1
            except sr.UnknownValueError:
                print("UnknownValue오류 n:", n, "caption flag=", caption_flag)
                file = open(f'{caption_path}/index{n}.txt', 'w', encoding="UTF-8")
                file.write("음성 미인식 에러가 발생했습니다. 곧 다음 자막이 생성됩니다.")
                file.close()
                n += 1
                continue
            except sr.RequestError as e:
                break
        
        elif caption_flag > 20:  
            shutil.rmtree(caption_path)
            break
        
