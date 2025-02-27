import cv2
import time

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

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)
        cv2.imshow('Live', frame)

        # 1초마다 프레임 플러시 시도
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    out.release()
    cv2.destroyAllWindows()