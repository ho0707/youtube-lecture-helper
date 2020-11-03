import cv2
import numpy as np
import os
import pafy
import re

save_frames = []
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

def save(frame, image, title):
    print('Saved frame number : ' + str(frame))
    sec = frame // 29.97
    h, m, s = get_time(sec)
    imwrite("images/{}/{:0>2}h {:0>2}m {:0>2}s.jpg".format(title, h, m, s), image)

def binary_search(vidcap, left, right, left_image, right_image, title):
    global save_frames
    if right - left < 35:
        #저장
        save_frames.append(right)
        return
    mid = (left + right) // 2
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ret, mid_image = vidcap.read()
    mid_image = cv2.resize(mid_image, (400, 225))
    mid_image = cv2.cvtColor(mid_image, cv2.COLOR_BGR2GRAY)
    diff = np.subtract(left_image, mid_image, dtype=np.int16)
    diff = np.abs(diff)
    diff_sum_left = np.sum(diff>10)

    diff = np.subtract(mid_image, right_image, dtype=np.int16)
    diff = np.abs(diff)
    diff_sum_right = np.sum(diff>10)
    if diff_sum_left < 2000 and diff_sum_right < 2000:
        # 뭔가 이상한곳
        return
    if diff_sum_left > 2000 and diff_sum_right > 2000:
        binary_search(vidcap, left, mid, left_image, mid_image, title)
        binary_search(vidcap, mid, right, mid_image, right_image, title)
        return
    if diff_sum_left > 2000:
        binary_search(vidcap, left, mid, left_image, mid_image, title)
        return
    if diff_sum_right > 2000:
        binary_search(vidcap, mid, right, mid_image, right_image, title)
        return

def get_time(sec):
    hour, remain = sec // 3600, sec % 3600
    minute, sec = remain // 60, remain % 60
    return hour, minute, sec

def extract_from_youtube_url(youtube_url):
    global save_frames
    index = re.compile('&index=')
    url = index.search(youtube_url)
    if url:
        youtube_url = youtube_url[:url.start()]
    time = re.compile('&t=')
    url = time.search(youtube_url)
    if url:
        youtube_url = youtube_url[:url.start()]
    
    try:
        video = pafy.new(youtube_url)
    except:
        raise ValueError('url이 잘못 되었습니다.')
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
        if y1.end() + y2.end() + y3.end():
            tmp_title = tmp_title + char
        
    title = tmp_title

    if not(os.path.isdir('images')):
        os.makedirs(os.path.join('images'))
    if not(os.path.isdir('images\\' + title)):
        os.makedirs(os.path.join('images\\' + title))

    vidcap = cv2.VideoCapture(best.url)
    vidcap.set(3, 400)
    vidcap.set(4, 225)
    _, start_image = vidcap.read()
    end = int(video.length * 29.97) - 30
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, end)
    _, end_image = vidcap.read()
    start_image = cv2.resize(start_image, (400, 225))
    start_image = cv2.cvtColor(start_image, cv2.COLOR_BGR2GRAY)
    end_image = cv2.resize(end_image, (400, 225))
    end_image = cv2.cvtColor(end_image, cv2.COLOR_BGR2GRAY)

    save_frames = [0]
    binary_search(vidcap, 0, end, start_image, end_image, title)
    for frame in save_frames:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        _, image = vidcap.read()
        save(frame, image, title)


def main():
    while True:
        url = input('ppt를 추출할 유튜브 url을 입력해주세요(종료 0): ')
        if url == '0':
            break
        extract_from_youtube_url(url)


if __name__ == '__main__':
    main()