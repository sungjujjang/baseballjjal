import cv2
import os
from moviepy.editor import VideoFileClip

def getgif(start_time, end_time, max_size_mb=20, filepath="output.avi", output='output.gif'):
    try:
        clip = VideoFileClip(filepath)
        clip = clip.subclip(start_time, end_time)
        # 초기 해상도 및 FPS 설정
        width = 720  # 초기 너비
        fps = min(clip.fps, 15)  # 기본 15fps로 설정
        quality = "optimizeplus"  # GIF 최적화 옵션

        # 일단 1차 변환 시도
        clip_resized = clip.resize(width=width).set_fps(fps)
        clip_resized.write_gif(output, program="ffmpeg", opt=quality)

        # 파일 크기 확인 및 자동 조정
        while os.path.getsize(output) / (1024 * 1024) > max_size_mb:
            width = int(width * 0.8)  # 해상도를 80%로 축소
            fps = max(5, int(fps * 0.8))  # FPS도 감소 (최소 5)
            
            clip_resized = clip.resize(width=width).set_fps(fps)
            clip_resized.write_gif(output, program="ffmpeg", opt=quality)

            # 240px 이하로 내려가면 중단 (너무 작아지는 것 방지)
            if width < 240:
                print("해상도를 더 낮출 수 없습니다.")
                break

        print(f"최종 GIF 파일 크기: {os.path.getsize(output) / (1024 * 1024):.2f}MB")
        print(f"출력 파일: {output}")
    except Exception as e:
        pass

# 사용 예시
# getgif(start_time=1, end_time=10, filepath="output.avi", output="output.gif")

# video = cv2.VideoCapture(filepath)

# if not video.isOpened():
#     print("Could not Open :", filepath)
#     exit(0)

# length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
# width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# # fps = video.get(cv2.CAP_PROP_FPS)
# fps = 30
# lg = width/fps

# print("length :", lg)
# print("frames :", length)
# print("width :", width)
# print("height :", height)
# print("fps :", fps)

# try:
#     if not os.path.exists(filepath[:-4]):
#         os.makedirs(filepath[:-4])
# except OSError:
#     print ('Error: Creating directory. ' + filepath[:-4])
    
# count = 0
# print("fps : ", fps)

# while(video.isOpened()):
#     count += 1
#     ret, image = video.read()
#     if not ret:
#         break
#     if count % int(fps/2) == 0:
#         cv2.imwrite(filepath[:-4] + "/%d.jpg" % count, image)
#         print('Saved frame number :', str(count))

# video.release()
# cv2.destroyAllWindows()

# img_list = os.listdir("output")
# img_list = ["output" + '/' + x for x in img_list]
# img_list.sort()
# images = [Image.open(x) for x in img_list]

# im = images[0]
# duritation = (lg/len(images)) * 1000
# im.save(output, save_all=True, append_images=images[1:], loop=0xff, duration=duritation)
# # loop 반복 횟수
# # duration 프레임 전환 속도 (500 = 0.5초)
# # return Img(url='out.gif')