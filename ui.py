import tkinter
import os
import tkinter.messagebox
from PIL import Image, ImageTk
import cv2
import random, string, subprocess
import ffmpeg, time
from tkinter import messagebox
from moviepy.editor import VideoFileClip
from to_gif import getgif

is_rec = False
process = None

def make_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def start_recording():
    global is_rec
    global process

    if not is_rec:  # 녹화가 꺼져 있을 때
        try:
            # 새 창에서 capture.py 실행
            process = subprocess.Popen(["python", "capture.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            is_rec = True
            messagebox.showinfo("녹화 시작", "녹화가 시작되었습니다")
            startrec.config(text="녹화 종료")
        except Exception as e:
            messagebox.showerror("오류", f"녹화 시작 실패: {e}")
    else:  # 녹화 중일 때 종료
        if process:
            try:
                process.terminate()
                process.wait()  # 프로세스 종료 대기
                process = None
                is_rec = False
                messagebox.showinfo("녹화 종료", "녹화가 종료되었습니다")
                startrec.config(text="녹화 시작")
            except Exception as e:
                messagebox.showerror("오류", f"녹화 종료 실패: {e}")

try:
    os.remove("output.avi")
    os.remove("./copies/output.avi")
    os.remove("./copies/output.mp4")
except Exception as e:
    print(e)

window = tkinter.Tk()

window.title("디시 자동 GIF 프로그램")
window.geometry("570x480")
window.resizable(False, False)

video_path = "output.avi"

def to_second(h, m, s):
    return h * 3600 + m * 60 + s

def get_video_duration(_video_path):
    clip = VideoFileClip(_video_path)
    return clip.duration

def getnowtime():
    if os.path.exists("checktime.txt"):
        with open("checktime.txt", "w") as f:
            f.write(f"get")
        fm = open("checktime.txt", "r").read()
        count = 0
        while True:
            fm = open("checktime.txt", "r").read()
            time.sleep(0.01)
            if fm.startswith("send"):
                t = fm.split(":")[1]
                return int(t)
            count += 1
            if count == 200:
                return None
    else:
        return None

def sectohms(sec):
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return h, m, s

def s_getimg():
    # get start h,m ,s
    h = int(start_h.get())
    m = int(start_m.get())
    s = int(start_s.get())
    t = to_second(h, m, s)
    try:
        img = ImageTk.PhotoImage(Image.open(f"images/{t}.png").resize((250, 180), Image.LANCZOS))
        label.config(image=img)
        label.image = img
    except:
        messagebox.showerror("오류", "영상이 없습니다")

def e_getimg():
    h = int(end_h.get())
    m = int(end_m.get())
    s = int(end_s.get())
    t = to_second(h, m, s)
    try:
        img = ImageTk.PhotoImage(Image.open(f"images/{t}.png").resize((250, 180), Image.LANCZOS))
        label.config(image=img)
        label.image = img
    except:
        messagebox.showerror("오류", "영상이 없습니다")

def s_getnowbtn():
    duration = getnowtime()
    if duration is not None:
        h, m, s = sectohms(duration)
        start_h.delete(0, tkinter.END)
        start_h.insert(0, h)
        start_m.delete(0, tkinter.END)
        start_m.insert(0, m)
        start_s.delete(0, tkinter.END)
        start_s.insert(0, s)
        shownowdef()

def e_getnowbtn():
    duration = getnowtime()
    if duration is not None:
        h, m, s = sectohms(duration)
        end_h.delete(0, tkinter.END)
        end_h.insert(0, h)
        end_m.delete(0, tkinter.END)
        end_m.insert(0, m)
        end_s.delete(0, tkinter.END)
        end_s.insert(0, s)
        shownowdef()
        
def make_gif():
    if check_blank():
        messagebox.showerror("오류", "빈 칸을 채워주세요")
        return
    try:
        start = to_second(int(start_h.get()), int(start_m.get()), int(start_s.get()))
        end = to_second(int(end_h.get()), int(end_m.get()), int(end_s.get()))
        print(start, end)
        if start >= end:
            messagebox.showerror("오류", "시작 시간이 종료 시간보다 늦습니다")
            return
        title = titletext.get()
        print(f'getgif(start_time={start}, end_time={end}, filepath="output.avi", output=f"./gifs/{title}.gif")')
        getgif(start_time=start, end_time=end, filepath="output.avi", output=f"./gifs/{title}.gif")
        messagebox.showinfo("완료", "GIF 제작이 완료되었습니다")
    except Exception as e:
        messagebox.showerror("오류", f"예외 발생: {e}")

def check_blank():
    if start_h.get() == "" or start_m.get() == "" or start_s.get() == "":
        return True
    elif end_h.get() == "" or end_m.get() == "" or end_s.get() == "":
        return True
    elif titletext.get() == "":
        return True
    return False

def get_last_frame(filename):
    if os.path.exists("checkframe.txt"):
        with open("checkframe.txt", "w") as f:
            f.write(f"{filename}")
        fm = open("checkframe.txt", "r").read()
        count = 0
        while fm != '0':
            fm = open("checkframe.txt", "r").read()
            time.sleep(0.01)
            count += 1
            if count == 200:
                return None
        img = ImageTk.PhotoImage(Image.open(f"assets/{filename}").resize((250, 180), Image.LANCZOS))
        os.remove(f"assets/{filename}")
        return img
    else:
        return None

# 이미지 로드 및 크기 조정
img = Image.open("./assets/loading.png")
img = img.resize((250, 180), Image.LANCZOS)  # 원하는 크기로 조정
img_r = ImageTk.PhotoImage(img)  # ImageTk.PhotoImage로 변환

label = tkinter.Label(window, image=img_r)
label.image = img_r  # 가비지 컬렉션 방지
label.pack()  # 레이블을 화면에 배치

def shownowdef():
    # filename = make_random_string(10)
    filename = "frame.jpg"
    img_r = get_last_frame(f"{filename}")
    if img_r is None:
        messagebox.showerror("오류", "영상이 없습니다")
    label.config(image=img_r)
    label.image = img_r

starttext = tkinter.Label(window, text="시작", font=("맑은 고딕", 13))
starttext.place(x=30, y=200)
startshowbtn = tkinter.Button(window, text="시작 위치 표시", font=("맑은 고딕", 10), command=s_getimg)
startshowbtn.place(x=100, y=200)
start_h = tkinter.Entry(window, font=("맑은 고딕", 13))
start_h.place(x=230, y=200, width=50)
start_h.insert(0, 0)
start_m = tkinter.Entry(window, font=("맑은 고딕", 13))
start_m.place(x=290, y=200, width=50)
start_m.insert(0, 0)
start_s = tkinter.Entry(window, font=("맑은 고딕", 13))
start_s.place(x=350, y=200, width=50)
start_s.insert(0, 0)
getnowbtnstart = tkinter.Button(window, text="현재 위치 선택", font=("맑은 고딕", 10), command=s_getnowbtn)
getnowbtnstart.place(x=430, y=200)

endtext = tkinter.Label(window, text="종료", font=("맑은 고딕", 13))
endtext.place(x=30, y=250)
endshowbtn = tkinter.Button(window, text="종료 위치 표시", font=("맑은 고딕", 10), command=e_getimg)
endshowbtn.place(x=100, y=250)
end_h = tkinter.Entry(window, font=("맑은 고딕", 13))
end_h.place(x=230, y=250, width=50)
end_h.insert(0, 0)
end_m = tkinter.Entry(window, font=("맑은 고딕", 13))
end_m.place(x=290, y=250, width=50)
end_m.insert(0, 0)
end_s = tkinter.Entry(window, font=("맑은 고딕", 13))
end_s.place(x=350, y=250, width=50)
end_s.insert(0, 0)
getnowbtnend = tkinter.Button(window, text="현재 위치 선택", font=("맑은 고딕", 10), command=e_getnowbtn)
getnowbtnend.place(x=430, y=250)

namelabel = tkinter.Label(window, text="제목", font=("맑은 고딕", 13))
namelabel.place(x=30, y=300)
titletext = tkinter.Entry(window, font=("맑은 고딕", 13))
titletext.place(x=100, y=300, width=300)
makegif = tkinter.Button(window, text="GIF 제작", font=("맑은 고딕", 10), command=make_gif)
makegif.place(x=430, y=300)

shownow = tkinter.Button(window, text="현재 위치", font=("맑은 고딕", 13), command=shownowdef)
shownow.place(x=200, y=400)
startrec = tkinter.Button(window, text="녹화 시작", font=("맑은 고딕", 13), command=start_recording)
startrec.place(x=300, y=400)

def on_closing():
    if process:
        process.terminate()
        process.wait()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()