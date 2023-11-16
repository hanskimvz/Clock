import tkinter as tk
import time, sys
import math
 
WIDTH = 1000
HEIGHT = 1000
TZ_OFFSET = 3600*9

canvas      = None
hour_hand   = None
minute_hand = None
second_hand = None
can_size = 0

def draw_clock_face():
   global canvas, hour_hand, minute_hand, second_hand 
   x0 = int((can_size-WIDTH)/2)
   y0 = int((can_size-HEIGHT)/2)
   x1 = x0 + WIDTH
   y1 = y0 + HEIGHT
   canvas.create_oval(x0,y0, x1, y1, outline="grey", fill="white", width=10)
   canvas.create_oval(can_size/2-30,can_size/2-30, can_size/2+30, can_size/2+30, outline="black", width=1, fill="black")
   c_second = canvas.create_oval(can_size/2-20,can_size/2-20, can_size/2+20, can_size/2+20, outline="red", width=1, fill="red")
   # Draw hour numbers
   for i in range(12):
      angle = i * math.pi/6 - math.pi/2
      x = can_size/2 + 0.7 * can_size/2 * math.cos(angle)
      y = can_size/2 + 0.7 * can_size/2 * math.sin(angle)
      if i == 0:
         canvas.create_text(x, y-10, text=str(i+12), font=("Helvetica", 50))
      else:
         canvas.create_text(x, y, text=str(i), font=("Helvetica", 50))

   # Draw minute lines
   for i in range(60):
      angle = i * math.pi/30 - math.pi/2
      x1 = can_size/2 + 0.8 * can_size/2 * math.cos(angle)
      y1 = can_size/2 + 0.8 * can_size/2 * math.sin(angle)
      x2 = can_size/2 + 0.9 * can_size/2 * math.cos(angle)
      y2 = can_size/2 + 0.9 * can_size/2 * math.sin(angle)
      if i % 5 == 0:
         canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
      else:
         canvas.create_line(x1, y1, x2, y2, fill="black", width=1)
   # Draw hour hand
   hour_hand   = canvas.create_line(0, 0, 0, 0, fill="black", width=20)

   # Draw minute hand
   minute_hand = canvas.create_line(0, 0, 0, 0, fill="black", width=10)

   # Draw second hand
   second_hand = canvas.create_line(0, 0, 0, 0, fill="red",   width=2)
   canvas.lift(c_second)


def update_clock():
   global canvas, hour_hand, minute_hand, second_hand
   # canvas.delete("all")
   # now = time.localtime()
   # hour = now.tm_hour % 12
   # minute = now.tm_min
   # second = now.tm_sec
   # msec =  math.modf(time.time())[0]

   # t = time.gmtime(time.time())
   # print (t)
   # print (msec)

   
   t = time.time()
   now = time.gmtime(t+TZ_OFFSET)
   hour = now.tm_hour % 12
   minute = now.tm_min
   second = now.tm_sec
   msec =  math.modf(t)[0]




   # Draw hour hand
   hour_angle = (hour + minute/60) * math.pi/6 - math.pi/2
   hour_x = can_size/2 + 0.5 * can_size/2 * math.cos(hour_angle)
   hour_y = can_size/2 + 0.5 * can_size/2 * math.sin(hour_angle)
   # canvas.create_line(WIDTH/2, HEIGHT/2, hour_x, hour_y, fill="black", width=6)
   canvas.coords(hour_hand, can_size/2, can_size/2, hour_x, hour_y)

   # Draw minute hand
   minute_angle = (minute + second/60) * math.pi/30 - math.pi/2
   minute_x = can_size/2 + 0.7 * can_size/2 * math.cos(minute_angle)
   minute_y = can_size/2 + 0.7 * can_size/2 * math.sin(minute_angle)
   # canvas.create_line(WIDTH/2, HEIGHT/2, minute_x, minute_y, fill="black", width=4)
   canvas.coords(minute_hand, can_size/2, can_size/2, minute_x, minute_y)

   # Draw second hand
   second_angle = (second + msec) * math.pi/30 - math.pi/2
   second_x = can_size/2 + 0.9 * can_size/2 * math.cos(second_angle)
   second_y = can_size/2 + 0.9 * can_size/2 * math.sin(second_angle)
   # canvas.create_line(WIDTH/2, HEIGHT/2, second_x, second_y, fill="red", width=2)
   canvas.coords(second_hand, can_size/2, can_size/2, second_x, second_y)
   
   canvas.after(50, update_clock)


def exitProgram(event=None):
    global Running
    Running = False

    root.destroy()
    root.quit()
    print ("destroyed root")
    sys.stdout.flush()

    return False

if __name__ == '__main__':
   root = tk.Tk()
   screen_width = root.winfo_screenwidth()
   screen_height = root.winfo_screenheight()

   CENTER = (int(screen_height/2), int(screen_height/2))
   
   can_size = min(screen_width, screen_height)

   root.geometry("%dx%d+0+0" %((screen_width), (screen_height)))

   # root.bind('<Double-Button-1>', edit_screen)
   # root.wm_attributes("-transparentcolor", 'grey')
   root.bind('<Button-3>', exitProgram)
   # root.protocol("WM_DELETE_WINDOW", exitProgram)
   root.configure(background="black")
   root.title("Analog Clock")
   
   canvas = tk.Canvas(root, width=can_size, height=can_size, relief="groove", borderwidth=0, highlightthickness=0, bg="black")
   # canvas.place(x=600, y = 540, anchor="center")
   canvas.pack(side="top")

   # tk.Label(root, text= "2023-11-16", font=("Helvetica", 100)).place(x=1200, y=540)
   
   draw_clock_face()
   update_clock()
   
   root.attributes("-fullscreen", True)
   root.resizable (False, False)
   root.mainloop()
