import tkinter as tk
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, title, size):
        # setup
        super().__init__()
        self.title(title)
        ctk.set_appearance_mode("dark")
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])
        
        # run
        self.mainloop()






App("D2 TTK Calculator", (800, 600))
