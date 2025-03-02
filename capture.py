import cv2
import time
import os
import keyboard

# make checkframe.txt
if not os.path.exists("checkframe.txt"):
    with open("checkframe.txt", "w") as f:
        f.write("0")

if not os.path.exists("checktime.txt"):
    with open("checktime.txt", "w") as f:
        f.write("0")

# delete all filein images folder
if os.path.exists("images"):
    for file in os.listdir("images"):
        os.remove(f"images/{file}")

def check_frame():
    with open("checkframe.txt", "r") as f:
        filename = f.read()
        if filename == '0':
            return False
        else:
            return filename

def check_time():
    with open("checktime.txt", "r") as f:
        filename = f.read()
        if filename.startswith("get"):
            return True
        else:
            return False

def get_available_cameras(max_cameras=10):
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

def select_camera():
    camera_list = get_available_cameras()
    if not camera_list:
        print("No cameras available")
        exit()
    print("Available cameras:")
    for i, cam in enumerate(camera_list):
        print(f"{i}: Camera {cam}")
    selected = int(input("Select camera: "))
    return camera_list[selected]

# 비디오 설정
width, height = 1280, 720
fps = 60

# 코덱 변경 (MJPG + AVI 조합)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
filename = 'output.avi'  # AVI 형식으로 변경

# 카메라 선택 및 설정
camera_index = select_camera()
cap = cv2.VideoCapture(camera_index)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, fps)

# 비디오 라이터 초기화
out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
count = 0
s = 0

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        count += 1
        if count % fps == 0:
            s += 1
            print(f"Captured {s} seconds")
        out.write(frame)
        # cv2.imshow('Live', frame)

        # 1초마다 프레임 플러시 시도
        fm = check_frame()
        if fm:
            with open("checkframe.txt", "w") as f:
                f.write("0")
            cv2.imwrite(f"assets/{fm}", frame)
        fm = None
        fm = check_time()
        if fm:
            with open("checktime.txt", "w") as f:
                f.write(f"send:{str(s)}")
            cv2.imwrite(f"images/{str(s)}.png", frame)
        
        if keyboard.is_pressed('q'):
            cap.release()
            out.release()
            cap = cv2.VideoCapture(camera_index)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_FPS, fps)

            # 비디오 라이터 초기화
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
            count = 0
            s = 0
        
        if s > 120:
            cap.release()
            out.release()
            cap = cv2.VideoCapture(camera_index)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_FPS, fps)

            # 비디오 라이터 초기화
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
            count = 0
            s = 0

finally:
    cap.release()
    out.release()
    # cv2.destroyAllWindows()