import cv2
import os
import imageio
import matplotlib.pyplot as plt
from PIL import Image
from IPython.display import Image as Img
from IPython.display import display

filepath = 'output.avi'

def getgif(filepath, output='output.gif'):
    video = cv2.VideoCapture(filepath)

    if not video.isOpened():
        print("Could not Open :", filepath)
        exit(0)

    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    print("length :", length)
    print("width :", width)
    print("height :", height)
    print("fps :", fps)

    try:
        if not os.path.exists(filepath[:-4]):
            os.makedirs(filepath[:-4])
    except OSError:
        print ('Error: Creating directory. ' + filepath[:-4])
        
    count = 0

    while(video.isOpened()):
        ret, image = video.read()
        if not ret:
            break
        if count % int(fps) == 0:  # FPS에 맞춰 프레임을 추출
            cv2.imwrite(filepath[:-4] + "/%d.jpg" % count, image)
            print('Saved frame number :', str(count))
        count += 1
    
    video.release()
    cv2.destroyAllWindows()
    
    img_list = os.listdir("output")
    img_list = ["output" + '/' + x for x in img_list]
    images = [Image.open(x) for x in img_list]
    
    im = images[0]
    im.save(output, save_all=True, append_images=images[1:],loop=0xff, duration=1/fps*0.001)
    # loop 반복 횟수
    # duration 프레임 전환 속도 (500 = 0.5초)
    # return Img(url='out.gif')

# 사용 예시
getgif(filepath, "output.gif")