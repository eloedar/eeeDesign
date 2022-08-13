import time

from hand_recognition import get_dis, detect, open_top

if __name__ == '__main__':
    while True:
        time.sleep(2)
        if get_dis() < 30:
            detect()
        else:
            continue
