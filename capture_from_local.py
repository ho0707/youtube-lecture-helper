import cv2
import numpy as np
import os
import pafy
import re
import datetime

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
    sec = frame // 30
    h, m, s = get_time(sec)
    imwrite("images/{}/{:0>2}h {:0>2}m {:0>2}s.jpg".format(title, h, m, s), image)
    # imwrite("images/{}/{}.jpg".format(title, sec), image)

def divide_and_conquer(vidcap, left, right, left_image, right_image, title):
    global save_frames
    if right - left < 20:
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
        return
    if diff_sum_left > 2000 and diff_sum_right > 2000:
        if right - left < 600:
            divide_and_conquer(vidcap, mid, right, mid_image, right_image, title)
        else:
            divide_and_conquer(vidcap, left, mid, left_image, mid_image, title)
            divide_and_conquer(vidcap, mid, right, mid_image, right_image, title)
        return
    if diff_sum_left > 2000:
        divide_and_conquer(vidcap, left, mid, left_image, mid_image, title)
        return
    if diff_sum_right > 2000:
        divide_and_conquer(vidcap, mid, right, mid_image, right_image, title)
        return

def get_time(sec):
    if sec < 0: 
        return 0, 0, 0
    hour, remain = sec // 3600, sec % 3600
    minute, sec = remain // 60, remain % 60
    return hour, minute, sec

def extract_from_path(path):
    global save_frames
    title = path.split('.')[0]
    if not(os.path.isdir('images')):
        os.makedirs(os.path.join('images'))
    if not(os.path.isdir('images\\' + title)):
        os.makedirs(os.path.join('images\\' + title))
    vidcap = cv2.VideoCapture(path)
    vidcap.set(3, 400)
    vidcap.set(4, 225)
    _, start_image = vidcap.read()
    left = 0
    right = 1000000000
    while left < right:
        mid = (left + right) // 2
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, mid)
        ret, _ = vidcap.read()
        if ret:
            left = mid + 1
        else:
            right = mid - 1
    end = right
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, end)
    _, end_image = vidcap.read()
    start_image = cv2.resize(start_image, (400, 225))
    start_image = cv2.cvtColor(start_image, cv2.COLOR_BGR2GRAY)
    end_image = cv2.resize(end_image, (400, 225))
    end_image = cv2.cvtColor(end_image, cv2.COLOR_BGR2GRAY)

    save_frames = [0]
    divide_and_conquer(vidcap, 0, end, start_image, end_image, title)
    for frame in save_frames:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        _, image = vidcap.read()
        save(frame, image, title)


def main():
    while True:
        path = input('ppt를 추출할 파일의 상대경로를 입력해주세요(종료: 0): ')
        if path == '0':
            break
        start = datetime.datetime.now()
        extract_from_path(path)
        end = datetime.datetime.now()
        print(end - start)

if __name__ == '__main__':
    main()