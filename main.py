from hand_recognition import get_dis, detect

if __name__ == '__main__':
    while True:
        if get_dis() < 30:
            detect()
        else:
            continue
