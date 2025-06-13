import math
import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk
import customtkinter as ctk
from PIL import Image, ImageTk
surges = [1.0, 1.03, 1.045, 1.055, 1.06]
health = 230
headshot = 42.61
bodyshot = 23.00
rpm = 327.27

burst = True #is burst weapon?
rpb = 2 #rounds per burst
burstRPM = 900

pi_multi = 0.04167 #damage multiplier for Precision Instrument - 1
epi_multi = 0.05 #damage multiplier for enhanced Precision Instrument - 1
def calculate():
    precision_instrument = bool(pi_num.get())
    enhanced_pi = bool(epi_num.get())
    if enhanced_pi:
        multi = epi_multi
    else:
        multi = pi_multi

    extra_multi = 1.0 * surges[surge_var.get()]
    for entry in multi_entries:
        try:
            extra_multi *= float(entry.get())
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
        timetokill = round((shots - 1) / (rpm / 60), 2)
    if burst:
        nBurst = math.ceil(shots / rpb) #number of bursts
        leftover = math.remainder(shots, rpb)
        if leftover == 0:
            timetokill = round((((nBurst - 1) * rpb) / rpm + (rpb - 1) / burstRPM) * 60, 3)
        else:
            timetokill = round((((nBurst - 1) * rpb) / rpm + (leftover - 1) / burstRPM) * 60, 3)
    result_text.configure(text = f"It would take {timetokill} seconds to kill in {headshots} headshots and {bodyshots} bodyshots")

# window
window = ctk.CTk()
window.title("D2 TTK Calculator")
window.geometry("1280x720")
ctk.set_appearance_mode("dark")

# title
title = ctk.CTkLabel(window, text = "Select a Weapon", pady = 10, font = ("Roboto", 75)).pack()

# images
auto_rifle_img_dark = Image.open("destiny2icons/whiteicons/auto-rifle-white.png")
auto_rifle_img = ctk.CTkImage(dark_image = auto_rifle_img_dark, size = (128, 36))
auto_rifle_img_ratio = 512 / 146
scout_rifle_img_dark = Image.open("destiny2icons/whiteicons/scout-rifle-white.png")
scout_rifle_img = ctk.CTkImage(dark_image = scout_rifle_img_dark, size = (128, 36))
smg_img_dark = Image.open("destiny2icons/whiteicons/smg-white.png")
smg_img = ctk.CTkImage(dark_image = smg_img_dark, size = (128, 64))
adaptive_frame_dark = Image.open("destiny2icons/whiteicons/adaptive-frame-white.png")
adaptive_frame_img = ctk.CTkImage(dark_image = adaptive_frame_dark, size = (64, 64))
aggressive_frame_dark = Image.open("destiny2icons/whiteicons/aggressive-frame-white.png")
aggressive_frame_img = ctk.CTkImage(dark_image = aggressive_frame_dark, size = (64, 64))
high_impact_frame_dark = Image.open("destiny2icons/whiteicons/high-impact-frame-white.png")
high_impact_frame_img = ctk.CTkImage(dark_image = high_impact_frame_dark, size = (64, 64))
lightweight_frame_dark = Image.open("destiny2icons/whiteicons/lightweight-frame-white.png")
lightweight_frame_img = ctk.CTkImage(dark_image = lightweight_frame_dark, size = (64, 64))
precision_frame_dark = Image.open("destiny2icons/whiteicons/precision-frame-white.png")
precision_frame_img = ctk.CTkImage(dark_image = precision_frame_dark, size = (64, 64))
rapid_fire_frame_dark = Image.open("destiny2icons/whiteicons/rapid-fire-frame-white.png")
rapid_fire_frame_img = ctk.CTkImage(dark_image = rapid_fire_frame_dark, size = (64, 64))
support_frame_dark = Image.open("destiny2icons/whiteicons/support-frame-white.png")
support_frame_img = ctk.CTkImage(dark_image = support_frame_dark, size = (64, 64))

# testing
test_var = ctk.StringVar(value = "option 1")
test_frame = ctk.CTkFrame(window)
test_frame.place(relx = 0.5, rely = 0.25, relwidth = 0.8, relheight = 0.2, anchor = "center")
test_frame.columnconfigure((0,1,2,3,4,5,6), weight = 1, uniform = "a")
test_frame.rowconfigure(0, weight = 1, uniform = "a")
active_test_button = None
def toggle_state(button):
    global active_test_button
    if active_test_button:
        if active_test_button == button:
            button.configure(border_width = 0)
            weapon_to_archetype[button].place_forget()
            active_test_button = None
        else:
            active_test_button.configure(border_width = 0)
            weapon_to_archetype[active_test_button].place_forget()
            button.configure(border_width = 2)
            weapon_to_archetype[button].place(relx = 0.5, rely = 0.45, relwidth = 0.6, relheight = 0.17, anchor = "center")
            active_test_button = button
    else:
        button.configure(border_width = 2)
        weapon_to_archetype[button].place(relx = 0.5, rely = 0.45, relwidth = 0.6, relheight = 0.17, anchor = "center")
        active_test_button = button

active_archetype = None
def select_archetype(arch):
    global active_archetype
    if active_archetype:
        if active_archetype == arch:
            arch.configure(border_width = 0)
            active_archetype = None
        else:
            active_archetype.configure(border_width = 0)
            arch.configure(border_width = 2)
            active_archetype = arch
    else:
        arch.configure(border_width = 2)
        active_archetype = arch
test_button1 = ctk.CTkButton(test_frame, text = "\nAuto Rifle", image = auto_rifle_img, compound = "top", font = ("Roboto", 16), command = lambda: toggle_state(test_button1))
test_button1.grid(row = 0, column = 0, sticky = "nsew", padx = 5)
test_button2 = ctk.CTkButton(test_frame, text = "tab 2", font = ("Roboto", 18))
test_button2.grid(row = 0, column = 1, sticky = "nsew", padx = 5)
test_button3 = ctk.CTkButton(test_frame, text = "tab 3", font = ("Roboto", 18))
test_button3.grid(row = 0, column = 2, sticky = "nsew", padx = 5)
test_button4 = ctk.CTkButton(test_frame, text = "tab 4", font = ("Roboto", 18))
test_button4.grid(row = 0, column = 3, sticky = "nsew", padx = 5)
test_button5 = ctk.CTkButton(test_frame, text = "\nScout Rifle", image = scout_rifle_img, compound = "top", font = ("Roboto", 16), command = lambda: toggle_state(test_button5))
test_button5.grid(row = 0, column = 4, sticky = "nsew", padx = 5)
test_button6 = ctk.CTkButton(test_frame, text = "tab 6", font = ("Roboto", 18))
test_button6.grid(row = 0, column = 5, sticky = "nsew", padx = 5)
test_button7 = ctk.CTkButton(test_frame, text = "Submachine Gun", image = smg_img, compound = "top", font = ("Roboto", 16), command = lambda: toggle_state(test_button7))
test_button7.grid(row = 0, column = 6, sticky = "nsew", padx = 5)

# layer 2
# auto
layer2_frame_auto = ctk.CTkFrame(window)
adaptive_frame_auto = ctk.CTkButton(layer2_frame_auto, text = "Adaptive\nFrame", font = ("Roboto", 14), compound = "top", image = adaptive_frame_img, width = 110, command = lambda: select_archetype(adaptive_frame_auto))
adaptive_frame_auto.pack(side = "left", expand = True, fill = "both", padx = 5)
high_impact_frame_auto = ctk.CTkButton(layer2_frame_auto, text = "High-impact\nFrame", font = ("Roboto", 14), compound = "top", image = high_impact_frame_img, width = 110, command = lambda: select_archetype(high_impact_frame_auto))
high_impact_frame_auto.pack(side = "left", expand = True, fill = "both", padx = 5)
lightweight_frame_auto = ctk.CTkButton(layer2_frame_auto, text = "Lightweight\nFrame", font = ("Roboto", 14), compound = "top", image = lightweight_frame_img, width = 110, command = lambda: select_archetype(lightweight_frame_auto))
lightweight_frame_auto.pack(side = "left", expand = True, fill = "both", padx = 5)
precision_frame_auto = ctk.CTkButton(layer2_frame_auto, text = "Precision\nFrame", font = ("Roboto", 14), compound = "top", image = precision_frame_img, width = 110, command = lambda: select_archetype(precision_frame_auto))
precision_frame_auto.pack(side = "left", expand = True, fill = "both", padx = 5)
rapid_fire_frame_auto = ctk.CTkButton(layer2_frame_auto, text = "Rapid-fire\nFrame", font = ("Roboto", 14), compound = "top", image = rapid_fire_frame_img, width = 110, command = lambda: select_archetype(rapid_fire_frame_auto))
rapid_fire_frame_auto.pack(side = "left", expand = True, fill = "both", padx = 5)
support_frame_auto = ctk.CTkButton(layer2_frame_auto, text = "Support\nFrame", font = ("Roboto", 14), compound = "top", image = support_frame_img, width = 110, command = lambda: select_archetype(support_frame_auto))
support_frame_auto.pack(side = "left", expand = True, fill = "both", padx = 5)
# scout
layer2_frame_scout = ctk.CTkFrame(window)
aggressive_frame_scout = ctk.CTkButton(layer2_frame_scout, text = "Aggressive\nFrame", font = ("Roboto", 14), compound = "top", image = aggressive_frame_img, width = 110, command = lambda: select_archetype(aggressive_frame_scout))
aggressive_frame_scout.pack(side = "left", expand = True, fill = "both", padx = 5)
high_impact_frame_scout = ctk.CTkButton(layer2_frame_scout, text = "High-impact\nFrame", font = ("Roboto", 14), compound = "top", image = high_impact_frame_img, width = 110, command = lambda: select_archetype(high_impact_frame_scout))
high_impact_frame_scout.pack(side = "left", expand = True, fill = "both", padx = 5)
lightweight_frame_scout = ctk.CTkButton(layer2_frame_scout, text = "Lightweight\nFrame", font = ("Roboto", 14), compound = "top", image = lightweight_frame_img, width = 110, command = lambda: select_archetype(lightweight_frame_scout))
lightweight_frame_scout.pack(side = "left", expand = True, fill = "both", padx = 5)
precision_frame_scout = ctk.CTkButton(layer2_frame_scout, text = "Precision\nFrame", font = ("Roboto", 14), compound = "top", image = precision_frame_img, width = 110, command = lambda: select_archetype(precision_frame_scout))
precision_frame_scout.pack(side = "left", expand = True, fill = "both", padx = 5)
rapid_fire_frame_scout = ctk.CTkButton(layer2_frame_scout, text = "Rapid-fire\nFrame", font = ("Roboto", 14), compound = "top", image = rapid_fire_frame_img, width = 110, command = lambda: select_archetype(rapid_fire_frame_scout))
rapid_fire_frame_scout.pack(side = "left", expand = True, fill = "both", padx = 5)
# smg
layer2_frame_smg = ctk.CTkFrame(window)
adaptive_frame_smg = ctk.CTkButton(layer2_frame_smg, text = "Adaptive\nFrame", font = ("Roboto", 14), compound = "top", image = adaptive_frame_img, width = 110, command = lambda: select_archetype(adaptive_frame_smg))
adaptive_frame_smg.pack(side = "left", expand = True, fill = "both", padx = 5)
aggressive_frame_smg = ctk.CTkButton(layer2_frame_smg, text = "Aggressive\nFrame", font = ("Roboto", 14), compound = "top", image = aggressive_frame_img, width = 110, command = lambda: select_archetype(aggressive_frame_smg))
aggressive_frame_smg.pack(side = "left", expand = True, fill = "both", padx = 5)
lightweight_frame_smg = ctk.CTkButton(layer2_frame_smg, text = "Lightweight\nFrame", font = ("Roboto", 14), compound = "top", image = lightweight_frame_img, width = 110, command = lambda: select_archetype(lightweight_frame_smg))
lightweight_frame_smg.pack(side = "left", expand = True, fill = "both", padx = 5)
precision_frame_smg = ctk.CTkButton(layer2_frame_smg, text = "Precision\nFrame", font = ("Roboto", 14), compound = "top", image = precision_frame_img, width = 110, command = lambda: select_archetype(precision_frame_smg))
precision_frame_smg.pack(side = "left", expand = True, fill = "both", padx = 5)

weapon_to_archetype = {test_button1 : layer2_frame_auto, test_button5 : layer2_frame_scout, test_button7 : layer2_frame_smg}


# layer 3
layer3_frame = ctk.CTkFrame(window)
layer3_frame.place(relx = 0.5, rely = 0.6, relwidth = 0.8, relheight = 0.1, anchor = "center")
layer3_frame.columnconfigure((0,1,2), weight = 1, uniform = "a")
layer3_frame.rowconfigure(0, weight = 1, uniform = "a")
# layer 3 section 1
layer3_subframe1 = ctk.CTkFrame(layer3_frame)
layer3_subframe1.grid(row = 0, column = 0, sticky = "nsew")
layer3_subframe1.columnconfigure(0, weight = 5, uniform = "a")
layer3_subframe1.columnconfigure(1, weight = 3, uniform = "a")
layer3_subframe1.rowconfigure(0, weight = 1, uniform = "a")
def show_epi():
    if pi_num.get():
        epi_switch.grid(row = 0, column = 1)
    else:
        epi_switch.grid_forget()

pi_num = ctk.IntVar(value = 0)
epi_num = ctk.IntVar(value = 0)
pi_checkbox = ctk.CTkCheckBox(layer3_subframe1, text = "Precision Instrument", font = ("Roboto", 18), command = show_epi, variable = pi_num)
pi_checkbox.grid(row = 0, column = 0)
epi_switch = ctk.CTkSwitch(layer3_subframe1, text = "Enhanced", font = ("Roboto", 18), variable = epi_num)

# layer 3 section 2
layer3_subframe2 = ctk.CTkFrame(layer3_frame)
layer3_subframe2.grid(row = 0, column = 1, sticky = "nsew")
layer3_subframe2.columnconfigure((0,1,2,3,4,5,6), weight = 1, uniform = "a")
layer3_subframe2.rowconfigure((0,1,2,3,4,5), weight = 1, uniform = "a")
surge_title = ctk.CTkLabel(layer3_subframe2, text = "Surges", font = ("Roboto", 18))
surge_title.grid(row = 0, column = 0, columnspan = 2, rowspan = 3, sticky = "s")
surge_var = ctk.IntVar(value = 0)
surge_slider = ctk.CTkSlider(layer3_subframe2, from_= 0, to = 4, number_of_steps = 4, variable = surge_var, command = lambda x: surge_val.configure(text = f"{int(x)}"))
surge_slider.grid(row = 0, column = 2, columnspan = 5, rowspan = 4, sticky = "we", padx = 20)
surge_val = ctk.CTkLabel(layer3_subframe2, text = "0", font = ("Roboto", 18))
surge_val.grid(row = 3, column = 0, columnspan = 2, rowspan = 3, sticky = "n")
surge_label0 = ctk.CTkLabel(layer3_subframe2, text = "0", font = ("Roboto", 14))
surge_label0.grid(row = 5, column = 2, rowspan = 2, sticky = "n")
surge_label1 = ctk.CTkLabel(layer3_subframe2, text = "1", font = ("Roboto", 14))
surge_label1.grid(row = 5, column = 3, rowspan = 2, sticky = "n")
surge_label2 = ctk.CTkLabel(layer3_subframe2, text = "2", font = ("Roboto", 14))
surge_label2.grid(row = 5, column = 4, rowspan = 2, sticky = "n")
surge_label3 = ctk.CTkLabel(layer3_subframe2, text = "3", font = ("Roboto", 14))
surge_label3.grid(row = 5, column = 5, rowspan = 2, sticky = "n")
surge_label4 = ctk.CTkLabel(layer3_subframe2, text = "4", font = ("Roboto", 14))
surge_label4.grid(row = 5, column = 6, rowspan = 2, sticky = "n")
# layer 3 section 3
num_of_multi = 0
def remove_multi_func(num):
    global num_of_multi
    num_of_multi -= 1
    for i in range(num, num_of_multi):
        multi_entries[i].set(multi_entries[i+1].get())
    multi_entries[num_of_multi].set("1.0")
    layer4_subframes[num_of_multi].grid_forget()

def add_multi_func():
    global num_of_multi
    if not num_of_multi > 6:
        layer4_subframes[num_of_multi].grid(row = 0, column = num_of_multi, sticky = "nsew")
        num_of_multi += 1
layer3_subframe3 = ctk.CTkFrame(layer3_frame)
layer3_subframe3.grid(row = 0, column = 2, sticky = "nsew")
layer3_subframe3.columnconfigure((0,1), weight = 1, uniform = "a")
layer3_subframe3.rowconfigure((0,), weight = 1, uniform = "a")
add_multi_text = ctk.CTkLabel(layer3_subframe3, text = "Add an Extra Buff ?", font = ("Roboto", 18))
add_multi_text.grid(row = 0, column = 0)
add_multi_button = ctk.CTkButton(layer3_subframe3, text = "Add Multiplier", font = ("Roboto", 14), command = add_multi_func)
add_multi_button.grid(row = 0, column = 1)
# layer 4
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

layer4_frame = ctk.CTkFrame(window)
layer4_frame.place(relx = 0.5, rely = 0.7, relwidth = 0.8, relheight = 0.1, anchor = "center")
layer4_frame.columnconfigure(tuple(range(7)), weight = 1, uniform = "a")
layer4_frame.rowconfigure(0, weight = 1, uniform = "a")
layer4_subframes = []
multi_entries = []
for i in range(7):
    subframe = ctk.CTkFrame(layer4_frame)
    subframe.columnconfigure(0, weight = 7, uniform = "a")
    subframe.columnconfigure(1, weight = 2, uniform = "a")
    subframe.rowconfigure(0, weight = 1, uniform = "a")
    layer4_subframes.append(subframe)

    entry = Float_Only_Entry(subframe, justify = "center")
    button = ctk.CTkButton(subframe, text = "X", command = lambda x = i: remove_multi_func(x))
    entry.grid(row = 0, column = 0, sticky = "ew", padx = 1)
    button.grid(row = 0, column = 1, padx = 1)

    multi_entries.append(entry)
#layer 5
calc_button = ctk.CTkButton(window, text = "Calculate", font = ("Roboto", 18), command = calculate)
calc_button.place(relx = 0.5, rely = 0.825, relwidth = 0.4, relheight = 0.05, anchor = "center")
result_text = ctk.CTkLabel(window, text = "", font = ("Roboto", 24))
result_text.place(relx = 0.5, rely = 0.925, anchor = "center")
# run
window.mainloop()
