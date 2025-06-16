import tkinter as tk
import customtkinter as ctk
import math
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self, title, size):
        # setup
        super().__init__()
        self.title(title)
        ctk.set_appearance_mode("dark")
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        self.active_archetype = None # which weapon archetype button is currently selected, name can be pulled with .name
        self.pi_num = ctk.IntVar(value = 0) # precision instrument enabled(1) or disabled(0)
        self.epi_num = ctk.IntVar(value = 0) # enhanced(1) or not(0)
        self.surges = ctk.IntVar(value = 0) # number of surges active
        self.surge_values = [1.0, 1.03, 1.045, 1.055, 1.06] # multiplier value for each amount of surges(0-4)
        self.multipliers = [] #list of all extra entries multipliers(max 7, default value of 1.0), values can be pull with .entry

        self.create_images()
        self.create_dict()
        self.weapon_select = WeaponSelect(self)
        self.buff_bar = BuffBar(self)
        self.calc_button = ctk.CTkButton(self, text = "Calculate", font = ("Roboto", 18), command = self.calculate)
        self.calc_button.place(relx = 0.5, rely = 0.825, relwidth = 0.4, relheight = 0.05, anchor = "center")
        self.result_text = ctk.CTkLabel(self, text = "", font = ("Roboto", 24))
        self.result_text.place(relx = 0.5, rely = 0.925, anchor = "center")

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
        
        self.archetype_damage_profiles = {
            "adaptiveframeautorifle" : {
                "headshot damage" : 26.335,
                "bodyshot damage" : 15.007,
                "rounds per minute" : 600.0,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "highimpactframeautorifle" : {
                "headshot damage" : 43.052,
                "bodyshot damage" : 23.996,
                "rounds per minute" : 360.0,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "precisionframeautorifle" : {
                "headshot damage" : 33.916,
                "bodyshot damage" : 19.997,
                "rounds per minute" : 450.0,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "rapidfireframeautorifle" : {
                "headshot damage" : 23.069,
                "bodyshot damage" : 13.601,
                "rounds per minute" : 720.0,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "supportframeautorifle" : {
                "headshot damage" : 26.408,
                "bodyshot damage" : 18.837,
                "rounds per minute" : 600.0,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "lightweightbowbow" : {
                "headshot damage" : 123.945,
                "bodyshot damage" : 77.561,
                "rounds per minute" : 60000 / (500 + 100 + 580), # this is miliseconds in a minute / (fastest reload in ms + constant nock delay in ms + draw time)
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "precisionbowbow" : {
                "headshot damage" : 131.355,
                "bodyshot damage" : 100.738,
                "rounds per minute" : 60000 / (500 + 100 + 684), # this is miliseconds in a minute / (fastest reload in ms + constant nock delay in ms + draw time)
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframehandcannon" : {
                "headshot damage" : 79.845,
                "bodyshot damage" : 44.504,
                "rounds per minute" : 138.5,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "aggressiveframehandcannon" : {
                "headshot damage" : 90.806,
                "bodyshot damage" : 49.006,
                "rounds per minute" : 120.0,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "heavybursthandcannon" : {
                "headshot damage" : 52.809,
                "bodyshot damage" : 23.996,
                "rounds per minute" : 257.1,
                "is burst weapon?" : True,
                "rounds per burst" : 2,
                "rpm mid burst" : 600.0
            },
            "precisionframehandcannon" : {
                "headshot damage" : 70.608,
                "bodyshot damage" : 45.296,
                "rounds per minute" : 180.0,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframepulserifle" : {
                "headshot damage" : 36.446,
                "bodyshot damage" : 21.997,
                "rounds per minute" : 385.7,
                "is burst weapon?" : True,
                "rounds per burst" : 3,
                "rpm mid burst" : 900.0
            },
            "aggressiveframepulserifle" : {
                "headshot damage" : 30.231,
                "bodyshot damage" : 15.495,
                "rounds per minute" : 450.0,
                "is burst weapon?" : True,
                "rounds per burst" : 4,
                "rpm mid burst" : 900.0
            },
            "heavyburstpulserifle" : {
                "headshot damage" : 42.623,
                "bodyshot damage" : 23.003,
                "rounds per minute" : 327.3,
                "is burst weapon?" : True,
                "rounds per burst" : 2,
                "rpm mid burst" : 600.0
            },
            "highimpactframepulserifle" : {
                "headshot damage" : 38.557,
                "bodyshot damage" : 21.491,
                "rounds per minute" : 337.5,
                "is burst weapon?" : True,
                "rounds per burst" : 3,
                "rpm mid burst" : 900.0
            },
            "lightweightframepulserifle" : {
                "headshot damage" : 31.491,
                "bodyshot damage" : 19.706,
                "rounds per minute" : 450.0,
                "is burst weapon?" : True,
                "rounds per burst" : 3,
                "rpm mid burst" : 900.0
            },
            "rapidfireframepulserifle" : {
                "headshot damage" : 27.809,
                "bodyshot damage" : 15.008,
                "rounds per minute" : 540.0,
                "is burst weapon?" : True,
                "rounds per burst" : 3,
                "rpm mid burst" : 900.0
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            "adaptiveframeauto" : {
                "headshot damage" : 2,
                "bodyshot damage" : 1,
                "rounds per minute" : 1,
                "is burst weapon?" : False,
                "rounds per burst" : 1,
                "rpm mid burst" : 1
            },
            }

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

    def calculate(self):
        health = 230
        pi_multi = 0.04167 #damage multiplier for Precision Instrument - 1
        epi_multi = 0.05 #damage multiplier for enhanced Precision Instrument - 1
        precision_instrument = bool(self.pi_num.get())
        enhanced_pi = bool(self.epi_num.get())

        try:
            damage_profile = self.archetype_damage_profiles[self.active_archetype.name]
        except:
            self.result_text.configure(text = f"Please Select a Weapon Type")
            return

        headshot = damage_profile["headshot damage"]
        bodyshot = damage_profile["bodyshot damage"]
        rpm = damage_profile["rounds per minute"]

        burst = damage_profile["is burst weapon?"]
        rpb = damage_profile["rounds per burst"]
        burstRPM = damage_profile["rpm mid burst"]

        if enhanced_pi:
            multi = epi_multi
        else:
            multi = pi_multi

        extra_multi = 1.0 * self.surge_values[self.surges.get()]
        for entry in self.multipliers:
            try:
                extra_multi *= float(entry.entry.get())
            except:
                print("Error: missing extra multiplier entry")
        hsd = extra_multi * headshot
        bsd = extra_multi * bodyshot
        dmg = 0

        if not precision_instrument:
            shots = 0

            while dmg <= health:
                dmg += hsd
                shots += 1

            headshots = shots
            bodyshots = 0

            while dmg > health:
                dmg = dmg + bsd - hsd
                headshots -= 1
                bodyshots += 1

            headshots += 1
            bodyshots -= 1

        else:
            shots = 0
            pi_count = 0

            while dmg <= health:
                if pi_count == 0:
                    dmg += hsd
                else:
                    dmg += hsd * (1 + multi * pi_count)
                shots += 1
                pi_count += 1

            headshots = shots
            bodyshots = 0
            pi_count = 0

            while dmg > health:
                if pi_count == 0:
                    dmg = dmg + bsd - hsd
                else:
                    dmg = dmg + bsd - (hsd * (1 + multi * pi_count))

                headshots -= 1
                bodyshots += 1
                pi_count += 1

            headshots += 1
            bodyshots -= 1
        if not burst:
            timetokill = round((shots - 1) / (rpm / 60), 3)
        if burst:
            nBurst = math.ceil(shots / rpb) #number of bursts
            leftover = shots % rpb
            if leftover == 0:
                timetokill = round((((nBurst - 1) * rpb) / rpm + (rpb - 1) / burstRPM) * 60, 3)
            else:
                timetokill = round((((nBurst - 1) * rpb) / rpm + (leftover - 1) / burstRPM) * 60, 3)
        self.result_text.configure(text = f"It would take {timetokill} seconds to kill in {headshots} headshots and {bodyshots} bodyshots")

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
        self.auto_rifle_archetypes_list = ["adaptiveframe", "highimpactframe", "precisionframe", "rapidfireframe", "supportframe"]
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

class BuffBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        self.master = master
        self.num_of_multi = 0

        super().__init__(self.master, **kwargs)
        self.columnconfigure(tuple(range(3)), weight = 1, uniform = "a")
        self.rowconfigure(0, weight = 1, uniform = "a")
        self.place(relx = 0.5, rely = 0.6, relwidth = 0.8, relheight = 0.1, anchor = "center")

        self.create_pi_section()
        self.create_surge_section()
        self.create_add_multi_section()

    def create_pi_section(self):
        self.pi_section = ctk.CTkFrame(self)
        self.pi_section.grid(row = 0, column = 0, sticky = "nsew")
        self.pi_section.columnconfigure(0, weight = 5, uniform = "a")
        self.pi_section.columnconfigure(1, weight = 3, uniform = "a")
        self.pi_section.rowconfigure(0, weight = 1, uniform = "a")

        self.pi_checkbox = ctk.CTkCheckBox(self.pi_section, text = "Precision Instrument", font = ("Roboto", 18), command = self.show_epi, variable = self.master.pi_num)
        self.pi_checkbox.grid(row = 0, column = 0)
        self.epi_switch = ctk.CTkSwitch(self.pi_section, text = "Enhanced", font = ("Roboto", 18), variable = self.master.epi_num)

    def show_epi(self):
        if self.master.pi_num.get():
            self.epi_switch.grid(row = 0, column = 1)
        else:
            self.epi_switch.grid_forget()

    def create_surge_section(self):
        self.surge_section = ctk.CTkFrame(self)
        self.surge_section.grid(row = 0, column = 1, sticky = "nsew")
        self.surge_section.columnconfigure(tuple(range(7)), weight = 1, uniform = "a")
        self.surge_section.rowconfigure(tuple(range(6)), weight = 1, uniform = "a")

        self.surge_title = ctk.CTkLabel(self.surge_section, text = "Surges", font = ("Roboto", 18))
        self.surge_title.grid(row = 0, column = 0, columnspan = 2, rowspan = 3, sticky = "s")
        self.surge_slider = ctk.CTkSlider(self.surge_section, from_= 0, to = 4, number_of_steps = 4, variable = self.master.surges,
                                           command = lambda x: self.surge_val.configure(text = f"{int(x)}"))
        self.surge_slider.grid(row = 0, column = 2, columnspan = 5, rowspan = 4, sticky = "we", padx = 20)
        self.surge_val = ctk.CTkLabel(self.surge_section, text = "0", font = ("Roboto", 18))
        self.surge_val.grid(row = 3, column = 0, columnspan = 2, rowspan = 3, sticky = "n")

        for x in range(5):
            label = ctk.CTkLabel(self.surge_section, text = f"{x}", font = ("Roboto", 14))
            label.grid(row = 5, column = x + 2, rowspan = 2, sticky = "n")

    def create_add_multi_section(self):
        self.add_multi_section = ctk.CTkFrame(self)
        self.add_multi_section.grid(row = 0, column = 2, sticky = "nsew")
        self.add_multi_section.columnconfigure((0,1), weight = 1, uniform = "a")
        self.add_multi_section.rowconfigure((0), weight = 1, uniform = "a")

        self.add_multi_text = ctk.CTkLabel(self.add_multi_section, text = "Add an Extra Buff ?", font = ("Roboto", 18))
        self.add_multi_text.grid(row = 0, column = 0)
        self.add_multi_button = ctk.CTkButton(self.add_multi_section, text = "Add Multiplier", font = ("Roboto", 14), command = self.add_multi)
        self.add_multi_button.grid(row = 0, column = 1)

        self.extra_multi_section = ctk.CTkFrame(self.master)
        self.extra_multi_section.place(relx = 0.5, rely = 0.7, relwidth = 0.8, relheight = 0.1, anchor = "center")
        self.extra_multi_section.columnconfigure(tuple(range(7)), weight = 1, uniform = "a")
        self.extra_multi_section.rowconfigure(0, weight = 1, uniform = "a")

        for i in range(7):
            multi = ExtraMultiplier(self.extra_multi_section, parent = self, num = i)
            self.master.multipliers.append(multi)


    def add_multi(self):
        if not self.num_of_multi > 6:
            self.master.multipliers[self.num_of_multi].grid(row = 0, column = self.num_of_multi, sticky = "nsew")
            self.num_of_multi += 1

    def remove_multi(self, num):
        self.num_of_multi -= 1
        for i in range(num, self.num_of_multi):
            self.master.multipliers[i].entry.set(self.master.multipliers[i+1].entry.get())
        self.master.multipliers[self.num_of_multi].entry.set("1.0")
        self.master.multipliers[self.num_of_multi].grid_forget()

class ExtraMultiplier(ctk.CTkFrame):
    def __init__(self, master, parent, num, **kwargs):
        self.master = master
        self.parent = parent
        super().__init__(self.master, **kwargs)
        self.columnconfigure(0, weight = 7, uniform = "a")
        self.columnconfigure(1, weight = 2, uniform = "a")
        self.rowconfigure(0, weight = 1, uniform = "a")

        self.entry = Float_Only_Entry(self, justify = "center")
        self.entry.grid(row = 0, column = 0, sticky = "ew", padx = 1)

        self.button = ctk.CTkButton(self, text = "X", command = lambda: self.parent.remove_multi(num))
        self.button.grid(row = 0, column = 1, padx = 1)

class Float_Only_Entry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        self.var = ctk.StringVar(value = "1.0")
        ctk.CTkEntry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = "1.0"
        self.var.trace_add("write", self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        try:
            # the current value is only floats; allow this
            float(self.get())
            self.old_value = self.get()
        except:
            # reject non-floats, but allow it to be blank
            if not self.get() == "":
                self.set(self.old_value)

    
App("D2 TTK Calculator", (1280, 720))
