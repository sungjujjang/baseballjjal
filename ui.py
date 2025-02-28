import tkinter
import os
from PIL import Image, ImageTk

try:
    os.remove("output.avi")
    os.remove("./copies/output.avi")
except:
    pass

window = tkinter.Tk()

window.title("디시 자동 GIF 프로그램")
window.geometry("640x480")
window.resizable(False, False)

video_path = "output.avi"

def showimg():
    pass

# 이미지 로드 및 크기 조정
img = Image.open("./assets/loading.png")
img = img.resize((250, 180), Image.LANCZOS)  # 원하는 크기로 조정
img_r = ImageTk.PhotoImage(img)  # ImageTk.PhotoImage로 변환

label = tkinter.Label(window, image=img_r)
label.image = img_r  # 가비지 컬렉션 방지
label.pack()  # 레이블을 화면에 배치

window.mainloop()