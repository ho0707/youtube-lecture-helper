import cv2
import numpy as np
import os
import pafy

def download(youtube_url):
    video = pafy.new(youtube_url)
    best = video.getbestaudio()

    title = video.title

    if not(os.path.isdir('audio')):
        os.makedirs(os.path.join('audio'))

    best.download('audio\\')

def main():
    while True:
        url = input('다운로드 받을 유튜브 url을 입력해주세요: ')
        if url == '0':
            break
        download(url)

if __name__ == '__main__':
    main()

 