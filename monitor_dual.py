#!/usr/bin/env python3
import sys, time
import tkinter as tk
import math

CLOCK_SIZE = 600
TZ_OFFSET =  3600*9

class AnalogClock:
    fullScreen = False

    def __init__(self):
        self.root = tk.Tk()
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("<Alt-Return>", self.toggleFullScreen)
        self.root.bind("<Control-w>", self.quit)
        self.root.configure(background="black")
        self.root.title("Analog Clock")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.can_size = min(self.screen_width, self.screen_height)
        self.root.geometry("%dx%d+0+0" %((self.screen_width), (self.screen_height)))
        self.canvas = tk.Canvas(self.root, width=self.can_size, height=self.can_size, relief="groove", borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.pack(side="top")
        self.ratio =  CLOCK_SIZE/self.can_size
        self.draw_clock_face()
        self.update_clock()
        self.root.mainloop()

    def draw_clock_face(self):
        x0 = int((self.can_size-CLOCK_SIZE)/2)
        y0 = int((self.can_size-CLOCK_SIZE)/2)
        x1 = x0 + CLOCK_SIZE
        y1 = y0 + CLOCK_SIZE
        self.canvas.create_oval(x0,y0, x1, y1, outline="grey", fill="white", width=10)
        
        # Draw hour numbers
        for i in range(12):
            angle = i * math.pi/6 - math.pi/2
            x = self.can_size/2 + 0.75 * self.can_size/2 * math.cos(angle) * self.ratio
            y = self.can_size/2 + 0.75 * self.can_size/2 * math.sin(angle) * self.ratio
            # x = self.can_size/2 + 0.7 * self.can_size/2 * math.cos(angle)
            # y = self.can_size/2 + 0.7 * self.can_size/2 * math.sin(angle)

            if i == 0:
                self.canvas.create_text(x, y-10, text=str(i+12), font=("Helvetica", int(50*self.ratio)), fill="blue")
            else:
                self.canvas.create_text(x, y, text=str(i), font=("Helvetica", int(50*self.ratio)), fill="blue")

        # Draw minute lines
        for i in range(60):
            angle = i * math.pi/30 - math.pi/2
            x1 = self.can_size/2 + 0.88 * self.can_size/2 * math.cos(angle) * self.ratio
            y1 = self.can_size/2 + 0.88 * self.can_size/2 * math.sin(angle) * self.ratio
            x2 = self.can_size/2 + 0.97 * self.can_size/2 * math.cos(angle) * self.ratio
            y2 = self.can_size/2 + 0.97 * self.can_size/2 * math.sin(angle) * self.ratio
            if i % 5 == 0:
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=1)

        self.hour_hand   = self.canvas.create_line(0, 0, 0, 0, fill="black", width=20)
        self.minute_hand = self.canvas.create_line(0, 0, 0, 0, fill="black", width=10)
        self.second_hand = self.canvas.create_line(0, 0, 0, 0, fill="red",   width=2)

        l = int(self.can_size/2-30*self.ratio)
        r = int(self.can_size/2+30*self.ratio)
        self.canvas.create_oval(l, l, r, r, outline="black", width=1, fill="black")
        l = int(self.can_size/2-20*self.ratio)
        r = int(self.can_size/2+20*self.ratio)
        self.canvas.create_oval(l,l, r, r, outline="red", width=1, fill="red")


    def update_clock(self):
        t = time.time()
        now = time.gmtime(t+TZ_OFFSET)
        hour = now.tm_hour % 12
        minute = now.tm_min
        second = now.tm_sec
        msec =  math.modf(t)[0]

        # Draw hour hand
        hour_angle = (hour + minute/60) * math.pi/6 - math.pi/2
        hour_x = self.can_size/2 + 0.6 * self.can_size/2 * math.cos(hour_angle) * self.ratio
        hour_y = self.can_size/2 + 0.6 * self.can_size/2 * math.sin(hour_angle) * self.ratio
        self.canvas.coords(self.hour_hand, self.can_size/2, self.can_size/2, hour_x, hour_y)

        # Draw minute hand
        minute_angle = (minute + (second + msec)/60) * math.pi/30 - math.pi/2
        minute_x = self.can_size/2 + 0.8 * self.can_size/2 * math.cos(minute_angle) * self.ratio
        minute_y = self.can_size/2 + 0.8 * self.can_size/2 * math.sin(minute_angle) * self.ratio
        self.canvas.coords(self.minute_hand, self.can_size/2, self.can_size/2, minute_x, minute_y)

        # Draw second hand
        second_angle = (second + msec) * math.pi/30 - math.pi/2
        second_x = self.can_size/2 + 0.97 * self.can_size/2 * math.cos(second_angle) * self.ratio
        second_y = self.can_size/2 + 0.97 * self.can_size/2 * math.sin(second_angle) * self.ratio
        self.canvas.coords(self.second_hand, self.can_size/2, self.can_size/2, second_x, second_y)

        self.canvas.after(50, self.update_clock)



    def toggleFullScreen(self, event):
        if self.fullScreen:
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()

    def activateFullscreen(self):
        self.fullScreen = True

        # Store geometry for reset
        self.geometry = self.root.geometry()

        # Hides borders and make truly fullscreen
        self.root.overrideredirect(True)

        # Maximize window (Windows only). Optionally set screen geometry if you have it
        self.root.state("zoomed")

    def deactivateFullscreen(self):
        self.fullScreen = False
        self.root.state("normal")
        self.root.geometry(self.geometry)
        self.root.overrideredirect(False)

    def quit(self, event=None):
        print("quiting...", event)
        self.root.quit()


if __name__ == '__main__':
    AnalogClock()


sys.exit()    





import ctypes
user = ctypes.windll.user32

class RECT(ctypes.Structure):
  _fields_ = [
    ('left', ctypes.c_long),
    ('top', ctypes.c_long),
    ('right', ctypes.c_long),
    ('bottom', ctypes.c_long)
    ]
  def dump(self):
    return [int(val) for val in (self.left, self.top, self.right, self.bottom)]

class MONITORINFO(ctypes.Structure):
  _fields_ = [
    ('cbSize', ctypes.c_ulong),
    ('rcMonitor', RECT),
    ('rcWork', RECT),
    ('dwFlags', ctypes.c_ulong)
    ]

def get_monitors():
  retval = []
  CBFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)
  def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
    r = lprcMonitor.contents
    #print("cb: %s %s %s %s %s %s %s %s" % (hMonitor, type(hMonitor), hdcMonitor, type(hdcMonitor), lprcMonitor, type(lprcMonitor), dwData, type(dwData)))
    data = [hMonitor]
    data.append(r.dump())
    retval.append(data)
    return 1
  cbfunc = CBFUNC(cb)
  temp = user.EnumDisplayMonitors(0, 0, cbfunc, 0)
  #print(temp)
  return retval

def monitor_areas():
  retval = []
  monitors = get_monitors()
  for hMonitor, extents in monitors:
    data = [hMonitor]
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    mi.rcMonitor = RECT()
    mi.rcWork = RECT()
    res = user.GetMonitorInfoA(hMonitor, ctypes.byref(mi))
    data = mi.rcMonitor.dump()
#    data.append(mi.rcWork.dump())
    retval.append(data)
  return retval


if __name__ == "__main__":
  print(monitor_areas())