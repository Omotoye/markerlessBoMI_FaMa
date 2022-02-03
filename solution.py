# For GUI
import tkinter as tk
from tkinter import Label, Button, BooleanVar, Checkbutton, Text

# For controlling computer cursor
import pyautogui

# for getting the screen resolution of the machine
from get_res import get_display_size

# for check when to click
from stopwatch import StopWatch

from CoppeliaSim.scripts.kuka_controller import KukaMobileRobot
from CoppeliaSim.scripts.manipulator_controller import ManipulatorController

import sys
import os


import time


class Solution:
    def __init__(self, MainApplication, parent, win):
        self.real_mouse_val = BooleanVar()
        self.virtual_mouse_val = BooleanVar()
        self.planar_manipulator_val = BooleanVar()
        self.parallel_manipulator_val = BooleanVar()
        self.kuka_robot_val = BooleanVar()
        self.MainApplication = (
            MainApplication  # Initialising a reference to the MainApplication class
        )
        self.parent = parent
        self.win = win
        self.font_size = 14
        self.size = (1, 1)
        self.state = 1  # 1: if the cursor is just moving around, 2: if the cursor has a possible target, 3: definite target found and its time to click
        self.get_real_width_height()
        self.stopwatch = StopWatch()
        self.stopwatch_started = False
        self.select_point = False
        self.x_min, self.x_max, self.y_min, self.y_max = 0, 0, 0, 0
        pyautogui.FAILSAFE = False  # to stop pyautogui from stopping when the cursor goes to the edges of the screen

        self.parallel_man_sim_launched = False
        self.planar_man_sim_launched = False
        self.kuka_sim_launched = False
        self.planar_manipulator_abspath = os.path.abspath(
            "CoppeliaSim\scenes\PlanarManipulator3D.ttt"
        )
        self.parallel_manipulator_abspath = os.path.abspath(
            "CoppeliaSim\scenes\ParallelTestv3.ttt"
        )
        self.kuka_robot_abspath = os.path.abspath(
            "CoppeliaSim\scenes\kuka_robot_scene.ttt"
        )
        self.check_device = False
        self.check_real_mouse = False
        self.check_planar_manipulator = False
        self.check_parallel_manipulator = False
        self.check_kuka_robot = False

    def _init_mouse_checkbox(self):
        # Real Mouse checkbox
        self.real_mouse_checkbox = Checkbutton(
            self.win, text="Real Mouse", variable=self.real_mouse_val
        )
        self.real_mouse_checkbox.config(font=("Arial", self.font_size))
        self.real_mouse_checkbox.grid(
            row=1, column=2, padx=(0, 40), pady=30, sticky="w"
        )

        # Virtual Mouse checkbox
        self.virtual_mouse_checkbox = Checkbutton(
            self.win, text="Virtual Mouse", variable=self.virtual_mouse_val
        )
        self.virtual_mouse_checkbox.config(font=("Arial", self.font_size))
        self.virtual_mouse_checkbox.grid(
            row=1, column=3, padx=(0, 40), pady=30, sticky="w"
        )

        # Planar Manipulator checkbox
        self.planar_manipulator_checkbox = Checkbutton(
            self.win, text="Planar Manipulator", variable=self.planar_manipulator_val
        )
        self.planar_manipulator_checkbox.config(font=("Arial", self.font_size))
        self.planar_manipulator_checkbox.grid(
            row=1, column=4, padx=(0, 40), pady=30, sticky="w"
        )

        # Kuka mobile robot checkbox
        self.kuka_robot_checkbox = Checkbutton(
            self.win, text="KUKA Robot", variable=self.kuka_robot_val
        )
        self.kuka_robot_checkbox.config(font=("Arial", self.font_size))
        self.kuka_robot_checkbox.grid(
            row=1, column=5, padx=(0, 40), pady=30, sticky="w"
        )

        # Parallel Manipulator checkbox
        self.parallel_manipulator_checkbox = Checkbutton(
            self.win,
            text="Parallel Manipulator(BETA)",
            variable=self.parallel_manipulator_val,
        )
        self.parallel_manipulator_checkbox.config(font=("Arial", self.font_size))
        self.parallel_manipulator_checkbox.grid(
            row=1, column=6, padx=(0, 40), pady=30, sticky="w"
        )

    def _init_mouse_select_button(self):
        # The Button to select the Mouse to control (Virtual/Real)
        self.mouse_control = Button(
            self.parent, text="Select Device", command=self.select_device_clbk
        )
        self.mouse_control.config(font=("Arial", self.font_size, "bold"))
        self.mouse_control.grid(
            row=1, column=0, columnspan=2, padx=20, pady=30, sticky="nesw"
        )

    def select_device_clbk(self):
        checkbox_vals = [
            self.real_mouse_val,
            self.virtual_mouse_val,
            self.planar_manipulator_val,
            self.parallel_manipulator_val,
            self.kuka_robot_val,
        ]
        count = 0
        for checkbox in checkbox_vals:
            if checkbox.get() == True:
                count += 1
        if count > 1:
            print("You need to pick only one of the options")

        elif count == 0:
            print("You need to pick one of the options")
        else:
            self.MainApplication["MainApplication"].btn_num_joints["state"] = "normal"
            if self.real_mouse_val.get():
                self.check_kuka_robot = False
                self.check_planar_manipulator = False
                self.check_parallel_manipulator = False
                self.check_device = True  # if the real mouse would be used
                self.check_real_mouse = True
                print("You have picked the Real Mouse")
            elif self.virtual_mouse_val.get():
                self.check_device = False  # if the virtual mouse would be used
                print("You have picked the Virtual Mouse")
            elif self.planar_manipulator_val.get():
                self.check_kuka_robot = False
                self.check_parallel_manipulator = False
                self.check_real_mouse = False
                print("You have picked the Planar Manipulator")
                self.check_planar_manipulator = True  # if a robot would be used
                self.check_device = True
                if self.planar_man_sim_launched == False:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "Press Play on Coppeliasim to start the connection\n when Coppeliasim is started",
                    )
                else:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "Press Play on Coppeliasim to start the connection",
                    )
                self.MainApplication["MainApplication"].master.wait_window(
                    self.MainApplication["MainApplication"].w.top
                )
                time.sleep(1)
                if self.planar_man_sim_launched == False:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "CoppeliaSim will now start",
                    )
                    self.MainApplication["MainApplication"].master.wait_window(
                        self.MainApplication["MainApplication"].w.top
                    )

                    os.startfile(self.planar_manipulator_abspath)
                    self.planar_man_sim_launched = True
                    time.sleep(5)
                self.planar_manipulator = ManipulatorController()
            elif self.parallel_manipulator_val.get():
                self.check_kuka_robot = False
                self.check_planar_manipulator = False
                self.check_real_mouse = False
                print("You have picked the Parallel Manipulator")
                self.check_device = True
                self.check_parallel_manipulator = True
                if self.parallel_man_sim_launched == False:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "Press Play on Coppeliasim to start the connection\n when Coppeliasim is started",
                    )
                else:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "Press Play on Coppeliasim to start the connection",
                    )

                self.MainApplication["MainApplication"].master.wait_window(
                    self.MainApplication["MainApplication"].w.top
                )
                time.sleep(1)
                if self.parallel_man_sim_launched == False:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "CoppeliaSim will now start",
                    )
                    self.MainApplication["MainApplication"].master.wait_window(
                        self.MainApplication["MainApplication"].w.top
                    )

                    os.startfile(self.parallel_manipulator_abspath)
                    self.parallel_man_sim_launched = True
                    time.sleep(5)
                self.parallel_manipulator = ManipulatorController()
            elif self.kuka_robot_val.get():
                self.check_planar_manipulator = False
                self.check_parallel_manipulator = False
                self.check_real_mouse = False
                print("You have picked the KuKa Mobile Robot")
                self.check_device = True
                self.check_kuka_robot = True
                if self.kuka_sim_launched == False:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "Press Play on Coppeliasim to start the connection\n when Coppeliasim is started",
                    )
                else:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "Press Play on Coppeliasim to start the connection",
                    )

                self.MainApplication["MainApplication"].master.wait_window(
                    self.MainApplication["MainApplication"].w.top
                )
                time.sleep(1)
                if self.kuka_sim_launched == False:
                    self.MainApplication["MainApplication"].w = popupWindow(
                        self.MainApplication["MainApplication"].master,
                        "CoppeliaSim will now start",
                    )
                    self.MainApplication["MainApplication"].master.wait_window(
                        self.MainApplication["MainApplication"].w.top
                    )

                    os.startfile(self.kuka_robot_abspath)
                    self.kuka_sim_launched = True
                    time.sleep(5)
                self.kuka_robot = KukaMobileRobot()

    def get_real_width_height(self):
        # real_screen_width, real_screen_height = get_display_size()
        self.real_screen_width = pyautogui.size().width
        self.real_screen_height = pyautogui.size().height

    def move_real_mouse(self, r):
        # Scaling virtual cursor coordinates to real screen coordinates
        self.real_mouse_x_coord = (r.crs_x / r.width) * self.real_screen_width
        self.real_mouse_y_coord = (r.crs_y / r.height) * self.real_screen_height

        pyautogui.moveTo(self.real_mouse_x_coord, self.real_mouse_y_coord)

    def move_mobile_robot(self, r):
        if self.stopwatch_started == False:
            self.stopwatch.start()
            self.stopwatch_started = True

        if self.stopwatch.elapsed_time >= 2000:
            #  x, y = self._coord_converter(
            #     ((r.crs_x / r.width) * , ((r.crs_y / r.width) * 4)
            # )
            x, y = self._coord_converter(r)
            self.kuka_robot.move_mobile_robot(x, y)
            self.stopwatch_started = False

    def move_planar_manipulator(self, r):
        # x = (r.crs_x / r.width) * 0.9
        x = (r.crs_x / r.width) * (0.5 - (-0.7)) + (-0.7)
        # y = (r.crs_y / r.width) * 0.9
        y = (r.crs_y / r.height) * (0.9 - (-0.9)) + (-0.9)
        target_coord = [x, y, 0.35]
        self.planar_manipulator.move_manipulator_tip(target_coord)

    def move_parallel_manipulator(self, r):
        # x = (r.crs_x / r.width) * 0.9
        x = (r.crs_x / r.width) * (0.5 - (-0.7)) + (-0.7)
        # y = (r.crs_y / r.width) * 0.9
        y = (r.crs_y / r.height) * (0.9 - (-0.9)) + (-0.9)
        target_coord = [x, y, 0.35]
        self.parallel_manipulator.move_manipulator_tip(target_coord)

    def _coord_converter(self, r):
        x = (r.crs_x / r.width) * (2 - (-2)) + (-2)
        # y = (r.crs_y / r.width) * 0.9
        y = (r.crs_y / r.height) * (2 - (-2)) + (-2)

        #  x = x - 2
        # if (0 <= y) and (y < 2):
        #    y = 2 + y
        # else:
        #    y = 2 - y
        return x, y

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
            if self.stopwatch.elapsed_time >= 1850:
                if self.check_mouse_stability():
                    self.state = 3
                else:
                    self.state = 1
                self.stopwatch.pause()
                self.stopwatch_started = False

        if self.state == 3:
            # pyautogui.leftClick()
            pyautogui.mouseDown()
            time.sleep(1)
            pyautogui.mouseUp()
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


class popupWindow(object):
    """
    class that defines the popup tkinter window
    """

    def __init__(self, master, msg):
        top = self.top = tk.Toplevel(master)
        self.lbl = Label(top, text=msg)
        self.lbl.pack()
        self.btn = Button(top, text="Ok", command=self.cleanup)
        self.btn.pack()

    def cleanup(self):
        self.top.destroy()
