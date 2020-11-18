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
    cnt = 0
    while cnt < 10:
        try:
            video = pafy.new(youtube_url)
            break
        except:
            cnt += 1
    else:
        raise ValueError('url이 잘못되었습니다.')
    best = video.getbest()

    if not(os.path.isdir('video')):
        os.makedirs(os.path.join('video'))

    best.download('video\\')

def main():
    while True:
        url = input('url을 입력해주세요(종료 0): ')
        if url == '0':
            break
        download(url)

if __name__ == '__main__':
    main()