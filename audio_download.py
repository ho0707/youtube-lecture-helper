import cv2
import numpy as np
import os
import pafy

def download(youtube_url):
    cnt = 0
    while cnt < 10:
        try:
            video = pafy.new(youtube_url)
            break
        except:
            cnt += 1
    else:
        raise ValueError('url이 잘못되었습니다.')
    best = video.getbestaudio()
    title = video.title

    if not(os.path.isdir('audio')):
        os.makedirs(os.path.join('audio'))

    best.download('audio\\')

def main():
    while True:
        url = input('다운로드 받을 유튜브 url을 입력해주세요(종료: 0): ')
        if url == '0':
            break
        download(url)

if __name__ == '__main__':
    main()

 