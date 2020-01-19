import tkinter as tk
import pyautogui as pgui

class Frame(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.position=tk.Label(self,text="")
        self.position.pack()

        self.update_capture()

    def update_capture(self):
        currentPosition=pgui.position()
        self.position.configure(text=currentPosition)
        self.after(20,self.update_capture)

if __name__ == "__main__":
    f = Frame()
    f.pack()
    f.mainloop()
