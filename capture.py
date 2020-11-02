import cv2
import numpy as np
import os
import pafy
import re

def imwrite(filename, img, params=None): 
    try: 
        ext = os.path.splitext(filename)[1] 
        result, n = cv2.imencode(ext, img, params) 
        if result: 
            with open(filename, mode='w+b') as f: 
                n.tofile(f) 
            return True 
        else: 
            return False 
    except Exception as e: 
        print(e) 
        return False

def get_time(sec):
    hour, remain = sec // 3600, sec % 3600
    minute, sec = remain // 60, remain % 60
    return hour, minute, sec

def extract_from_youtube_url(youtube_url):
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
    tmp_title = ''
    usable1 = re.compile("[가-힣]?")
    usable2 = re.compile("[a-zA-Z]?")
    usable3 = re.compile("[!@#$%^()\[\]_+-=}{';.,]?")
    
    for char in title:
        if char == ' ':
            tmp_title = tmp_title + char
            continue
        y1 = usable1.match(char)
        y2 = usable2.match(char)
        y3 = usable3.match(char)
        print(char)
        print(y1, y2, y3)
        if y1.end() + y2.end() + y3.end():
            tmp_title = tmp_title + char
        
    title = tmp_title
    print(title)
    if not(os.path.isdir('images')):
        os.makedirs(os.path.join('images'))
    if not(os.path.isdir('images\\' + title)):
        os.makedirs(os.path.join('images\\' + title))

    vidcap = cv2.VideoCapture(best.url)
    count = 0
    vidcap.set(3, 400)
    vidcap.set(4, 225)
    flag = 0
    stack = 0
    frame = 0
    ret, prev = vidcap.read()
    imwrite("images/{}/00h 00m 00s.jpg".format(title), prev)
    while(vidcap.isOpened()):
        frame += 150
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, image = vidcap.read()
        if not ret:
            stack += 1
            if stack > 5:
                break
            continue
        stack = 0
        prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        diff = np.subtract(prev_gray, image_gray, dtype=np.int16)
        diff = np.abs(diff)
        diff = cv2.resize(diff, (400, 225))
        sum_diff = np.sum(diff>10)
        if sum_diff > 2000:
            print('Saved frame number : ' + str(frame))
            sec = frame // 29.97
            h, m, s = get_time(sec)
            imwrite("images/{}/{} {:0>2}h {:0>2}m {:0>2}s.jpg".format(title, sum_diff, h, m, s), image)
            count += 1
        prev = image
    # cv2.imwrite("images/{}/{}_{}.jpg".format(title, count, sum_diff), prev)
    vidcap.release()

def main():
    while True:
        url = input('ppt를 추출할 유튜브 url을 입력해주세요: ')
        if url == '0':
            break
        extract_from_youtube_url(url)


if __name__ == '__main__':
    main()