import time
from tkinter import *

def clock(): # 현재 시간 표시 / 반복
   live_T = time.strftime("%H:%M:%S") # Real Time
   clock_width.config(text=live_T)
   clock_width.after(200, clock) # .after(지연시간{ms}, 실행함수)

root = Tk()
root.title("Clock")
# root.geometry("-1-1")
# root.wm_attributes("-topmost", 1) # 창을 항상 상단에 배치 / 0 외 모든 인자 True

txt_frame = Frame(root)
txt_frame.pack()

clock_frame = Frame(root)
clock_frame.pack()

clock_width = Label(clock_frame, font=("Times",60,"bold"), bg="white", bd=8)
clock_width.pack()

clock()
root.mainloop()