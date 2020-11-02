import cv2
import numpy as np
import os
import pafy
import re

def download(youtube_url):
    index = re.compile('&index=')
    url = index.search(youtube_url)
    if url:
        youtube_url = youtube_url[:url.start()]
    time = re.compile('&t=')
    url = time.search(youtube_url)
    if url:
        youtube_url = youtube_url[:url.start()]


    video = pafy.new(youtube_url)
    best = video.getbest()

    title = video.title

    if not(os.path.isdir('video')):
        os.makedirs(os.path.join('video'))

    best.download('video\\')

def main():
    while True:
        url = input('다운로드 받을 유튜브 url을 입력해주세요(종료 0): ')
        if url == '0':
            break
        download(url)

if __name__ == '__main__':
    main()