import cv2
import numpy as np
import os
import pafy

def download(youtube_url):
    video = pafy.new(youtube_url)
    best = video.getbest()

    title = video.title

    if not(os.path.isdir('video')):
        os.makedirs(os.path.join('video'))

    best.download('video\\')

def main():
    while True:
        url = input('url을 입력해주세요: ')
        if url == '0':
            break
        download(url)

if __name__ == '__main__':
    main()