import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self, title, size):
        # setup
        super().__init__()
        self.title(title)
        ctk.set_appearance_mode("dark")
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])
        self.active_archetype = None

        self.create_images()
        self.create_dict()
        self.weapon_select = WeaponSelect(self)

        # run
        self.mainloop()

    def create_images(self):
        self.adaptive_frame_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/adaptive-frame-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/adaptive-frame-white.png"), size = (64, 64))
        self.aggressive_frame_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/aggressive-frame-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/aggressive-frame-white.png"), size = (64, 64))
        self.heavy_burst_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/heavy-burst-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/heavy-burst-white.png"), size = (64, 64))
        self.high_impact_frame_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/high-impact-frame-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/high-impact-frame-white.png"), size = (64, 64))
        self.lightweight_frame_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/lightweight-frame-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/lightweight-frame-white.png"), size = (64, 64))
        self.precision_frame_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/precision-frame-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/precision-frame-white.png"), size = (64, 64))
        self.rapid_fire_frame_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/rapid-fire-frame-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/rapid-fire-frame-white.png"), size = (64, 64))
        self.support_frame_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/support-frame-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/support-frame-white.png"), size = (64, 64))
        self.lightweight_frame_bow_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/lightweight-frame-bow-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/lightweight-frame-bow-white.png"), size = (64, 64))
        self.precision_frame_bow_img = ctk.CTkImage(light_image = Image.open("destiny2icons/blackicons/precision-frame-bow-black.png"),
                                               dark_image = Image.open(f"destiny2icons/whiteicons/precision-frame-bow-white.png"), size = (64, 64))
        
    def create_dict(self):
        self.archetype_display = {"adaptiveframe" : ("Adaptive\nFrame", self.adaptive_frame_img),
                              "aggressiveframe" : ("Aggressive\nFrame", self.aggressive_frame_img),
                              "heavyburst" : ("Heavy\nBurst", self.heavy_burst_img),
                              "highimpactframe": ("High-Impact\nFrame", self.high_impact_frame_img),
                              "lightweightframe" : ("Lightweight\nFrame", self.lightweight_frame_img),
                              "precisionframe" : ("Precision\nFrame", self.precision_frame_img),
                              "rapidfireframe" : ("Rapid-Fire\nFrame", self.rapid_fire_frame_img),
                              "supportframe" : ("Support\nFrame", self.support_frame_img),
                              "lightweightbow" : ("Lightweight\nFrame", self.lightweight_frame_bow_img),
                              "precisionbow" : ("Precision\nFrame", self.precision_frame_bow_img),
                              "adaptiveburst" : ("Adaptive\nBurst", self.adaptive_frame_img)}

    def select_archetype(self, arch):
        if self.active_archetype:
            if self.active_archetype == arch:
                arch.configure(border_width = 0)
                self.active_archetype = None
            else:
                self.active_archetype.configure(border_width = 0)
                arch.configure(border_width = 2)
                self.active_archetype = arch
        else:
            arch.configure(border_width = 2)
            self.active_archetype = arch

class WeaponSelect(ctk.CTkFrame):
    def __init__(self, master,**kwargs):
        self.master = master
        self.active_test_button = None
        super().__init__(self.master, **kwargs)
        self.columnconfigure(tuple(range(7)), weight = 1, uniform = "a")
        self.rowconfigure(0, weight = 1, uniform = "a")
        self.create_buttons()
        self.place_buttons()
        self.place(relx = 0.5, rely = 0.25, relwidth = 0.8, relheight = 0.2, anchor = "center")

    def create_buttons(self):
        self.auto_rifle_archetypes_list = ["adaptiveframe", "highimpactframe", "lightweightframe", "precisionframe", "supportframe"]
        self.auto_rifle = WeaponButton(self, image_type = "auto-rifle", text = "\n\nAuto Rifle", dimensions = (128, 36), list = self.auto_rifle_archetypes_list)
        self.bow_archetypes_list = ["lightweightbow", "precisionbow"]
        self.bow = WeaponButton(self, image_type = "bow", text = "\n\nBow", dimensions = (128, 42), list = self.bow_archetypes_list)
        self.hand_cannon_archetypes_list = ["adaptiveframe", "aggressiveframe", "heavyburst", "precisionframe"]
        self.hand_cannon = WeaponButton(self, image_type = "hand-cannon", text = "\nHand Cannon", dimensions = (128, 64), list = self.hand_cannon_archetypes_list)
        self.pulse_rifle_archetypes_list = ["adaptiveframe", "aggressiveframe", "heavyburst", "highimpactframe", "lightweightframe", "rapidfireframe"]
        self.pulse_rifle = WeaponButton(self, image_type = "pulse-rifle", text = "\n\nPulse Rifle", dimensions = (128, 44), list = self.pulse_rifle_archetypes_list)
        self.scout_rifle_archetypes_list = ["aggressiveframe", "highimpactframe", "lightweightframe", "precisionframe", "rapidfireframe"]
        self.scout_rifle = WeaponButton(self, image_type = "scout-rifle", text = "\n\nScout Rifle", dimensions = (128, 36), list = self.scout_rifle_archetypes_list)
        self.sidearm_archetypes_list = ["adaptiveframe", "adaptiveburst", "heavyburst", "lightweightframe", "precisionframe", "rapidfireframe"]
        self.sidearm = WeaponButton(self, image_type = "sidearm", text = "\nSidearm", dimensions = (85, 63), list = self.sidearm_archetypes_list)
        self.smg_archetypes_list = ["adaptiveframe", "aggressiveframe", "lightweightframe", "precisionframe"]
        self.smg = WeaponButton(self, image_type = "smg", text = "\nSubmachine Gun", dimensions = (128, 64), list = self.smg_archetypes_list)

    def place_buttons(self):
        self.auto_rifle.grid(row = 0, column = 0, sticky = "nsew", padx = 5)
        self.bow.grid(row = 0, column = 1, sticky = "nsew", padx = 5)
        self.hand_cannon.grid(row = 0, column = 2, sticky = "nsew", padx = 5)
        self.pulse_rifle.grid(row = 0, column = 3, sticky = "nsew", padx = 5)
        self.scout_rifle.grid(row = 0, column = 4, sticky = "nsew", padx = 5)
        self.sidearm.grid(row = 0, column = 5, sticky = "nsew", padx = 5)
        self.smg.grid(row = 0, column = 6, sticky = "nsew", padx = 5)
        
    def toggle_state(self, button):
        if self.active_test_button:
            if self.active_test_button == button:
                button.configure(border_width = 0)
                button.archetypes.place_forget()
                self.active_test_button = None
            else:
                self.active_test_button.configure(border_width = 0)
                self.active_test_button.archetypes.place_forget()
                button.configure(border_width = 2)
                button.archetypes.place(relx = 0.5, rely = 0.45, relwidth = 0.6, relheight = 0.17, anchor = "center")
                self.active_test_button = button
        else:
            button.configure(border_width = 2)
            button.archetypes.place(relx = 0.5, rely = 0.45, relwidth = 0.6, relheight = 0.17, anchor = "center")
            self.active_test_button = button
            
class ArchetypeSelect(ctk.CTkFrame):
    def __init__(self, master, list, weapon_name, **kwargs):
        self.master = master
        self.list = list
        self.weapon_name = weapon_name
        super().__init__(self.master, **kwargs)
        self.create_buttons()
    def create_buttons(self):
        for item in self.list:
            text, image = self.master.archetype_display[item]
            button = ArchetypeButton(self, text = text, image = image, name = item + self.weapon_name)
            button.pack(side = "left", expand = True, fill = "both", padx = 5)
    
class WeaponButton(ctk.CTkButton):
    def __init__(self, master, image_type, dimensions, list, **kwargs):
        self.master = master
        self.name = image_type.replace("-", "")
        self.image = ctk.CTkImage(light_image = Image.open(f"destiny2icons/blackicons/{image_type}-black.png"),
                                  dark_image = Image.open(f"destiny2icons/whiteicons/{image_type}-white.png"), size = dimensions)
        self.archetypes = ArchetypeSelect(self.master.master, list = list, weapon_name = self.name)
        super().__init__(self.master, image = self.image, compound = "top", font = ("Roboto", 16), command = lambda: master.toggle_state(self), **kwargs)

class ArchetypeButton(ctk.CTkButton):
    def __init__(self, master, name, **kwargs):
        self.master = master
        self.name = name
        super().__init__(self.master, font = ("Roboto", 14), compound = "top", width = 110, command = lambda: self.master.master.select_archetype(self), **kwargs)

App("D2 TTK Calculator", (1280, 720))
