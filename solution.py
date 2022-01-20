# For GUI
import tkinter as tk
from tkinter import Label, Button, BooleanVar, Checkbutton, Text

# For controlling computer cursor
import pyautogui

# for getting the screen resolution of the machine
from get_res import get_display_size

# for check when to click
from stopwatch import StopWatch


class Solution:
    def __init__(self, MainApplication, parent, win):
        self.real_mouse_val = BooleanVar()
        self.virtual_mouse_val = BooleanVar()
        self.MainApplication = (
            MainApplication  # Initialising a reference to the MainApplication class
        )
        self.parent = parent
        self.win = win
        self.font_size = 18
        self.size = (1, 1)
        self.state = 1  # 1: if the cursor is just moving around, 2: if the cursor has a possible target, 3: definite target found and its time to click
        self.get_real_width_height()
        self.stopwatch = StopWatch()
        self.stopwatch_started = False
        self.select_point = False
        self.x_min, self.x_max, self.y_min, self.y_max = 0, 0, 0, 0
        pyautogui.FAILSAFE = False  # to stop pyautogui from stopping when the cursor goes to the edges of the screen

    def _init_mouse_checkbox(self):
        # Real Mouse checkbox
        self.real_mouse_checkbox = Checkbutton(
            self.win, text="Real Mouse", variable=self.real_mouse_val
        )
        self.real_mouse_checkbox.config(font=("Arial", self.font_size))
        self.real_mouse_checkbox.grid(
            row=0, column=2, padx=(0, 40), pady=30, sticky="w"
        )

        # Virtual Mouse checkbox
        self.virtual_mouse_checkbox = Checkbutton(
            self.win, text="Virtual Mouse", variable=self.virtual_mouse_val
        )
        self.virtual_mouse_checkbox.config(font=("Arial", self.font_size))
        self.virtual_mouse_checkbox.grid(
            row=0, column=3, padx=(0, 40), pady=30, sticky="w"
        )

    def _init_mouse_select_button(self):
        # The Button to select the Mouse to control (Virtual/Real)
        self.mouse_control = Button(
            self.parent, text="Select Mouse", command=self.select_mouse_clbk
        )
        self.mouse_control.config(font=("Arial", self.font_size))
        self.mouse_control.grid(
            row=0, column=0, columnspan=2, padx=20, pady=30, sticky="nesw"
        )

    def select_mouse_clbk(self):
        if self.real_mouse_val.get() == True and self.virtual_mouse_val.get() == True:
            print("You need to pick only one of the options")

        elif (
            self.real_mouse_val.get() == False and self.virtual_mouse_val.get() == False
        ):
            print("You need to pick one of the options")
        else:
            self.MainApplication["MainApplication"].btn_num_joints["state"] = "normal"
            if self.real_mouse_val.get():
                self.check_mouse = True  # if the real mouse would be used
                print("You have picked the Real Mouse")
            elif self.virtual_mouse_val.get():
                self.check_mouse = False  # if the virtual mouse would be used
                print("You have picked the Virtual Mouse")

    def get_real_width_height(self):
        # real_screen_width, real_screen_height = get_display_size()
        self.real_screen_width = pyautogui.size().width
        self.real_screen_height = pyautogui.size().height

    def move_real_mouse(self, r):
        # Scaling virtual cursor coordinates to real screen coordinates
        self.real_mouse_x_coord = (r.crs_x / r.width) * self.real_screen_width
        self.real_mouse_y_coord = (r.crs_y / r.height) * self.real_screen_height

        pyautogui.moveTo(self.real_mouse_x_coord, self.real_mouse_y_coord)

    def click_real_mouse(self):
        print(self.state)
        if self.state == 1:
            if self.select_point == False:
                self.set_point_boundary()
                self.time_mouse_stability()
                self.select_point = True

            if self.stopwatch_started == True:
                if self.stopwatch.elapsed_time >= 500:
                    if self.check_mouse_stability():
                        self.state = 2
                    self.select_point = False

        if self.state == 2:
            if self.stopwatch.elapsed_time >= 1000:
                if self.check_mouse_stability() == False:
                    self.state == 1
                    self.stopwatch.pause()
                    self.stopwatch_started = False
            if self.stopwatch.elapsed_time >= 1500:
                if self.check_mouse_stability() == False:
                    self.state == 1
                    self.stopwatch.pause()
                    self.stopwatch_started = False
            if self.stopwatch.elapsed_time >= 2000:
                if self.check_mouse_stability():
                    self.state = 3
                else:
                    self.state = 1
                self.stopwatch.pause()
                self.stopwatch_started = False

        if self.state == 3:
            pyautogui.leftClick()
            print("Click")
            self.state = 1

    def check_mouse_stability(self):
        if (self.x_min < self.real_mouse_x_coord < self.x_max) and (
            self.y_min < self.real_mouse_y_coord < self.y_max
        ):
            return True
        else:
            return False

    def set_point_boundary(self):
        self.x_min, self.x_max = (
            self.real_mouse_x_coord - 50,
            self.real_mouse_x_coord + 50,
        )
        self.y_min, self.y_max = (
            self.real_mouse_y_coord - 50,
            self.real_mouse_y_coord + 50,
        )

    def time_mouse_stability(self):
        if self.stopwatch_started == False:
            self.stopwatch.start()
            self.stopwatch_started = True
