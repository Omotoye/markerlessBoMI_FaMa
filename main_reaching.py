# General imports
import numpy as np
import pandas as pd
import os
import time
import matplotlib.pyplot as plt

# For multithreading
from threading import Thread, Lock
import queue

# For OpenCV
import cv2

# For GUI
import tkinter as tk
from tkinter import Label, Button, BooleanVar, Checkbutton, Text
import webbrowser

# For pygame
import pygame

# For reaching task
from reaching import Reaching
from stopwatch import StopWatch
from filter_butter_online import FilterButter3
import reaching_functions

# For controlling computer cursor
import pyautogui

# from get_res import get_display_size  # for getting the screen resolution of the machine

# For Mediapipe
import mediapipe as mp

# For training pca/autoencoder
from compute_bomi_map import Autoencoder, PrincipalComponentAnalysis, compute_vaf

# For the assignment solution
from solution import Solution

pyautogui.PAUSE = 0.01  # set fps of cursor to 100Hz ish when mouse_enabled is True

solution = None


class MainApplication(tk.Frame):
    """
    class that defines the main tkinter window --> graphic with buttons etc..
    """

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.calibPath = os.path.dirname(os.path.abspath(__file__)) + "/calib/"
        self.drPath = ""
        self.num_joints = 0
        self.joints = np.zeros((5, 1))
        self.dr_mode = "ae"
        self.font_size = 14
        
        """
        setting the label to Biomedical Project
      
        """

        self.lbl_tgt = Label(win, text="Biomedical Project")
        self.lbl_tgt.config(font=("Times new roman", 30))
        self.lbl_tgt.grid(row=0, column=2, pady=(20, 30), columnspan=2, sticky="w")

        self.btn_num_joints = Button(
            parent, text="Select Joints", command=self.select_joints
        )
        self.btn_num_joints.config(font=("Arial", self.font_size, "bold"))
        self.btn_num_joints["state"] = "disabled"
        self.btn_num_joints.grid(
            row=2, column=0, columnspan=2, padx=20, pady=30, sticky="nesw"
        )

        # set checkboxes for selecting joints
        self.check_nose = BooleanVar()
        self.check1 = Checkbutton(win, text="Nose", variable=self.check_nose)
        self.check1.config(font=("Arial", self.font_size))
        self.check1.grid(row=2, column=2, padx=(0, 40), pady=30, sticky="w")

        self.check_eyes = BooleanVar()
        self.check2 = Checkbutton(win, text="Eyes", variable=self.check_eyes)
        self.check2.config(font=("Arial", self.font_size))
        self.check2.grid(row=2, column=3, padx=(0, 40), pady=30, sticky="w")

        self.check_shoulders = BooleanVar()
        self.check3 = Checkbutton(win, text="Shoulders", variable=self.check_shoulders)
        self.check3.config(font=("Arial", self.font_size))
        self.check3.grid(row=2, column=4, padx=(0, 30), pady=30, sticky="w")

        self.check_forefinger = BooleanVar()
        self.check4 = Checkbutton(
            win, text="Right Forefinger", variable=self.check_forefinger
        )
        self.check4.config(font=("Arial", self.font_size))
        self.check4.grid(row=2, column=5, padx=(0, 20), pady=30, sticky="w")

        self.check_fingers = BooleanVar()
        self.check5 = Checkbutton(win, text="Fingers", variable=self.check_fingers)
        self.check5.config(font=("Arial", self.font_size))
        self.check5.grid(row=2, column=6, padx=(0, 20), pady=30, sticky="nesw")

        self.btn_calib = Button(parent, text="Calibration", command=self.calibration)
        self.btn_calib["state"] = "disabled"
        self.btn_calib.config(font=("Arial", self.font_size, "bold"))
        self.btn_calib.grid(
            row=3, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="nesw"
        )
        self.calib_duration = 30000

        # Calibration time remaining
        self.lbl_calib = Label(win, text="Calibration time: ")
        self.lbl_calib.config(font=("Arial", self.font_size))
        self.lbl_calib.grid(row=3, column=2, columnspan=2, pady=(20, 30), sticky="w")

        # BoMI map button and checkboxes
        self.btn_map = Button(parent, text="Calculate BoMI Map", command=self.train_map)
        self.btn_map["state"] = "disabled"
        self.btn_map.config(font=("Arial", self.font_size, "bold"))
        self.btn_map.grid(
            row=4, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="nesw"
        )

        self.check_pca = BooleanVar(value=True)
        self.check_pca1 = Checkbutton(win, text="PCA", variable=self.check_pca)
        self.check_pca1.config(font=("Arial", self.font_size))
        self.check_pca1.grid(row=4, column=2, padx=(0, 20), pady=(20, 30), sticky="w")

        self.check_ae = BooleanVar()
        self.check_ae1 = Checkbutton(win, text="AE", variable=self.check_ae)
        self.check_ae1.config(font=("Arial", self.font_size))
        self.check_ae1.grid(row=4, column=3, padx=(0, 20), pady=(20, 30), sticky="w")

        self.check_vae = BooleanVar()
        self.check_vae1 = Checkbutton(
            win, text="Variational AE", variable=self.check_vae
        )
        self.check_vae1.config(font=("Arial", self.font_size))
        self.check_vae1.grid(row=4, column=4, pady=(20, 30), sticky="w")

        self.btn_custom = Button(
            parent, text="Customization", command=self.customization
        )
        self.btn_custom["state"] = "disabled"
        self.btn_custom.config(font=("Arial", self.font_size, "bold"))
        self.btn_custom.grid(
            row=5, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="nesw"
        )

        self.btn_start = Button(parent, text="Practice", command=self.start)
        self.btn_start["state"] = "disabled"
        self.btn_start.config(font=("Arial", self.font_size, "bold"))
        self.btn_start.grid(
            row=6, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="nesw"
        )

        # set label for number of target remaining
        self.lbl_tgt = Label(win, text="Remaining targets: ")
        self.lbl_tgt.config(font=("Arial", self.font_size))
        self.lbl_tgt.grid(row=6, column=2, pady=(20, 30), columnspan=2, sticky="w")

        # !!!!!!!!!!!!! [ADD CODE HERE] Mouse control checkbox !!!!!!!!!!!!!
        
        """
        Simulating a pointer to the MainApplication class
      
        """
        self.object_pointer = {"MainApplication": self}

        """
        Initialising the Solution Class
      
        """
        global solution
        solution = Solution(self.object_pointer, parent, win)
        
        """
        Initialising the Mouse checkboxes and button
      
        """
        solution._init_mouse_checkbox()
        solution._init_mouse_select_button()
        #############################################################

        self.btn_close = Button(parent, text="Close", command=parent.destroy, bg="red")
        self.btn_close.config(font=("Arial", self.font_size, "bold"))
        self.btn_close.grid(
            row=7, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="nesw"
        )

        self.github_link = Button(
            parent, text="Link to gihub repository", command=self.github_callback
        )
        self.github_link.config(font=("Arial", 12, "italic"))
        self.github_link.grid(
            row=7, column=2, columnspan=2, padx=20, pady=(20, 30), sticky="nesw"
        )

    def github_callback(self):
        webbrowser.open("https://github.com/Omotoye/markerlessBoMI_FaMa", new=1)

    # Count number of joints selected
    def select_joints(self):
        nose_enabled = self.check_nose.get()
        eyes_enabled = self.check_eyes.get()
        shoulders_enabled = self.check_shoulders.get()
        forefinger_enabled = self.check_forefinger.get()
        fingers_enabled = self.check_fingers.get()
        if nose_enabled:
            self.num_joints += 2
            self.joints[0, 0] = 1
        if eyes_enabled:
            self.num_joints += 4
            self.joints[1, 0] = 1
        if shoulders_enabled:
            self.num_joints += 4
            self.joints[2, 0] = 1
        if forefinger_enabled:
            self.num_joints += 2
            self.joints[3, 0] = 1
        if fingers_enabled:
            self.num_joints += 10
            self.joints[4, 0] = 1
        if np.sum(self.joints, axis=0) != 0:
            self.btn_calib["state"] = "normal"
            self.btn_map["state"] = "normal"
            self.btn_custom["state"] = "normal"
            self.btn_start["state"] = "normal"
            print("Joints correctly selected.")

    def calibration(self):
        # start calibration dance - collect webcam data
        self.w = popupWindow(self.master, "You will now start calibration.")
        self.master.wait_window(self.w.top)
        compute_calibration(
            self.calibPath,
            self.calib_duration,
            self.lbl_calib,
            self.num_joints,
            self.joints,
        )
        self.btn_map["state"] = "normal"

    def train_map(self):
        # check whether calibration file exists first
        if os.path.isfile(self.calibPath + "Calib.txt"):
            self.w = popupWindow(self.master, "You will now train BoMI map")
            self.master.wait_window(self.w.top)
            if self.check_pca.get():
                self.drPath = self.calibPath + "PCA/"
                train_pca(self.calibPath, self.drPath)
                self.dr_mode = "pca"
            elif self.check_ae.get():
                self.drPath = self.calibPath + "AE/"
                train_ae(self.calibPath, self.drPath)
                self.dr_mode = "ae"
            elif self.check_vae.get():
                self.drPath = self.calibPath + "AE/"
                train_ae(self.calibPath, self.drPath)
                self.dr_mode = "ae"
            self.btn_custom["state"] = "normal"
        else:
            self.w = popupWindow(self.master, "Perform calibration first.")
            self.master.wait_window(self.w.top)
            self.btn_map["state"] = "disabled"

    def customization(self):
        # check whether PCA/AE parameters have been saved
        if os.path.isfile(self.drPath + "weights1.txt"):
            # open customization window
            self.newWindow = tk.Toplevel(self.master)
            self.newWindow.geometry("1000x500")
            self.newWindow.title("Customization")
            self.app = CustomizationApplication(
                self.newWindow,
                self,
                drPath=self.drPath,
                num_joints=self.num_joints,
                joints=self.joints,
                dr_mode=self.dr_mode,
            )
        else:
            self.w = popupWindow(self.master, "Compute BoMI map first.")
            self.master.wait_window(self.w.top)
            self.btn_custom["state"] = "disabled"

    def start(self):
        # check whether customization parameters have been saved
        if os.path.isfile(self.drPath + "offset_custom.txt"):
            # open pygame and start reaching task
            self.w = popupWindow(self.master, "You will now start practice.")
            self.master.wait_window(self.w.top)
            start_reaching(
                self.drPath,
                self.lbl_tgt,
                self.num_joints,
                self.joints,
                self.dr_mode,
                solution.check_device,
            )
            # [ADD CODE HERE: one of the argument of start reaching should be [self.check_mouse]
            # to check in the checkbox is enable] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            self.w = popupWindow(self.master, "Perform customization first.")
            self.master.wait_window(self.w.top)
            self.btn_start["state"] = "disabled"


class CustomizationApplication(tk.Frame):
    """
    class that defines the customization tkinter window
    """

    def __init__(self, parent, mainTk, drPath, num_joints, joints, dr_mode):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.mainTk = mainTk
        self.drPath = drPath
        self.num_joints = num_joints
        self.joints = joints
        self.dr_mode = dr_mode
        self.font_size = 18

        self.lbl_rot = Label(parent, text="Rotation ")
        self.lbl_rot.config(font=("Arial", self.font_size))
        self.lbl_rot.grid(column=0, row=0, padx=(300, 0), pady=(40, 20), sticky="w")
        self.txt_rot = Text(parent, width=10, height=1)
        self.txt_rot.config(font=("Arial", self.font_size))
        self.txt_rot.grid(column=1, row=0, pady=(40, 20))
        self.txt_rot.insert("1.0", "0")

        self.lbl_gx = Label(parent, text="Gain x ")
        self.lbl_gx.config(font=("Arial", self.font_size))
        self.lbl_gx.grid(column=0, row=1, padx=(300, 0), pady=(40, 20), sticky="w")
        self.txt_gx = Text(parent, width=10, height=1)
        self.txt_gx.config(font=("Arial", self.font_size))
        self.txt_gx.grid(column=1, row=1, pady=(40, 20))
        self.txt_gx.insert("1.0", "1")

        self.lbl_gy = Label(parent, text="Gain y ")
        self.lbl_gy.config(font=("Arial", self.font_size))
        self.lbl_gy.grid(column=0, row=2, padx=(300, 0), pady=(40, 20), sticky="w")
        self.txt_gy = Text(parent, width=10, height=1)
        self.txt_gy.config(font=("Arial", self.font_size))
        self.txt_gy.grid(column=1, row=2, pady=(40, 20))
        self.txt_gy.insert("1.0", "1")

        self.lbl_ox = Label(parent, text="Offset x ")
        self.lbl_ox.config(font=("Arial", self.font_size))
        self.lbl_ox.grid(column=0, row=3, padx=(300, 0), pady=(40, 20), sticky="w")
        self.txt_ox = Text(parent, width=10, height=1)
        self.txt_ox.config(font=("Arial", self.font_size))
        self.txt_ox.grid(column=1, row=3, pady=(40, 20))
        self.txt_ox.insert("1.0", "0")

        self.lbl_oy = Label(parent, text="Offset y ")
        self.lbl_oy.config(font=("Arial", self.font_size))
        self.lbl_oy.grid(column=0, row=4, padx=(300, 0), pady=(40, 20), sticky="w")
        self.txt_oy = Text(parent, width=10, height=1)
        self.txt_oy.config(font=("Arial", self.font_size))
        self.txt_oy.grid(column=1, row=4, pady=(40, 20))
        self.txt_oy.insert("1.0", "0")

        self.btn_save = Button(
            parent, text="Save parameters", command=self.save_parameters
        )
        self.btn_save.config(font=("Arial", self.font_size))
        self.btn_save.grid(column=2, row=1, sticky="nesw", padx=(80, 0), pady=(40, 20))

        self.btn_start = Button(parent, text="Start", command=self.customization)
        self.btn_start.config(font=("Arial", self.font_size))
        self.btn_start.grid(column=2, row=2, sticky="nesw", padx=(80, 0), pady=(40, 20))

        self.btn_close = Button(parent, text="Close", command=parent.destroy, bg="red")
        self.btn_close.config(font=("Arial", self.font_size))
        self.btn_close.grid(column=2, row=3, sticky="nesw", padx=(80, 0), pady=(40, 20))
        
    """
    functions to retrieve values of textbox programmatically
    """
    def retrieve_txt_rot(self):
        return self.txt_rot.get("1.0", "end-1c")

    def retrieve_txt_gx(self):
        return self.txt_gx.get("1.0", "end-1c")

    def retrieve_txt_gy(self):
        return self.txt_gy.get("1.0", "end-1c")

    def retrieve_txt_ox(self):
        return self.txt_ox.get("1.0", "end-1c")

    def retrieve_txt_oy(self):
        return self.txt_oy.get("1.0", "end-1c")

    def customization(self):
        initialize_customization(
            self, self.dr_mode, self.drPath, self.num_joints, self.joints
        )

    def save_parameters(self):
        save_parameters(self, self.drPath)
        self.parent.destroy()
        self.mainTk.btn_start["state"] = "normal"


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


def compute_calibration(drPath, calib_duration, lbl_calib, num_joints, joints):
    """
    function called to collect calibration data from webcam
    :param drPath: path to save calibration file
    :param calib_duration: duration of calibration as read by the textbox in the main window
    :param lbl_calib: label in the main window that shows calibration time remaining
    :return:
    """
    # Create object of openCV and Reaching (needed for terminating mediapipe thread)
    cap = cv2.VideoCapture(0)
    r = Reaching()

    # The clock will be used to control how fast the screen updates. Stopwatch to count calibration time elapsed
    clock = pygame.time.Clock()
    timer_calib = StopWatch()

    # initialize MediaPipe Pose
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        smooth_landmarks=False,
    )

    # initialize lock for avoiding race conditions in threads
    lock = Lock()

    # global variable accessed by main and mediapipe threads that contains the current vector of body landmarks
    global body
    body = np.zeros((num_joints,))  # initialize global variable
    body_calib = (
        []
    )  # initialize local variable (list of body landmarks during calibration)

    # start thread for OpenCV. current frame will be appended in a queue in a separate thread
    q_frame = queue.Queue()
    cal = 1  # if cal==1 (meaning during calibration) the opencv thread will display the image
    opencv_thread = Thread(target=get_data_from_camera, args=(cap, q_frame, r, cal))
    opencv_thread.start()
    print("openCV thread started in calibration.")

    # initialize thread for mediapipe operations
    mediapipe_thread = Thread(
        target=mediapipe_forwardpass,
        args=(holistic, mp_holistic, lock, q_frame, r, num_joints, joints),
    )
    mediapipe_thread.start()
    print("mediapipe thread started in calibration.")

    # start the timer for calibration
    timer_calib.start()

    print("main thread: Starting calibration...")

    while not r.is_terminated:

        if timer_calib.elapsed_time > calib_duration:
            r.is_terminated = True

        # get current value of body
        body_calib.append(np.copy(body))

        # update time elapsed label
        time_remaining = int((calib_duration - timer_calib.elapsed_time) / 1000)
        lbl_calib.configure(text="Calibration time: " + str(time_remaining))
        lbl_calib.update()

        # --- Limit to 50 frames per second
        clock.tick(50)

    # Stop the game engine and release the capture
    holistic.close()
    print("pose estimation object released in calibration.")
    cap.release()
    cv2.destroyAllWindows()
    print("openCV object released in calibration.")

    # print calibration file
    body_calib = np.array(body_calib)
    if not os.path.exists(drPath):
        os.makedirs(drPath)
    np.savetxt(drPath + "Calib.txt", body_calib)

    print("Calibration finished. You can now train BoMI forward map.")


def train_pca(calibPath, drPath):
    """
    function to train BoMI forward map - PCA
    :param drPath: path to save BoMI forward map
    :return:
    """
    r = Reaching()
    # read calibration file and remove all the initial zero rows
    xp = list(pd.read_csv(calibPath + "Calib.txt", sep=" ", header=None).values)
    x = [i for i in xp if all(i)]
    x = np.array(x)

    # randomly shuffle input
    np.random.shuffle(x)

    # define train/test split
    thr = 80
    split = int(len(x) * thr / 100)
    train_x = x[0:split, :]
    test_x = x[split:, :]

    # initialize object of class PCA
    n_pc = 2
    PCA = PrincipalComponentAnalysis(n_pc)

    # train PCA
    pca, train_x_rec, train_pc, test_x_rec, test_pc = PCA.train_pca(
        train_x, x_test=test_x
    )
    print("PCA has been trained.")

    # save weights and biases
    if not os.path.exists(drPath):
        os.makedirs(drPath)
    np.savetxt(drPath + "weights1.txt", pca.components_[:, :2])

    print("BoMI forward map (PCA parameters) has been saved.")

    # compute train/test VAF
    print(f"Training VAF: {compute_vaf(train_x, train_x_rec)}")
    print(f"Test VAF: {compute_vaf(test_x, test_x_rec)}")

    # normalize latent space to fit the monitor coordinates
    # Applying rotation
    train_pc = np.dot(train_x, pca.components_[:, :2])
    rot = 0
    train_pc[0] = train_pc[0] * np.cos(np.pi / 180 * rot) - train_pc[1] * np.sin(
        np.pi / 180 * rot
    )
    train_pc[1] = train_pc[0] * np.sin(np.pi / 180 * rot) + train_pc[1] * np.cos(
        np.pi / 180 * rot
    )
    # Applying scale
    scale = [r.width / np.ptp(train_pc[:, 0]), r.height / np.ptp(train_pc[:, 1])]
    train_pc = train_pc * scale
    # Applying offset
    off = [
        r.width / 2 - np.mean(train_pc[:, 0]),
        r.height / 2 - np.mean(train_pc[:, 1]),
    ]
    train_pc = train_pc + off

    # Plot latent space
    plt.figure()
    plt.scatter(train_pc[:, 0], train_pc[:, 1], c="green", s=20)
    plt.title("Projections in workspace")
    plt.axis("equal")

    # save AE scaling values
    with open(drPath + "rotation_dr.txt", "w") as f:
        print(rot, file=f)
    np.savetxt(drPath + "scale_dr.txt", scale)
    np.savetxt(drPath + "offset_dr.txt", off)

    print("PCA scaling values has been saved. You can continue with customization.")


def train_ae(calibPath, drPath):
    """
    function to train BoMI forward map
    :param drPath: path to save BoMI forward map
    :return:
    """
    r = Reaching()

    # Autoencoder parameters
    n_steps = 3001
    lr = 0.02
    cu = 2
    nh1 = 6
    activ = "tanh"

    # read calibration file and remove all the initial zero rows
    xp = list(pd.read_csv(calibPath + "Calib.txt", sep=" ", header=None).values)
    x = [i for i in xp if all(i)]
    x = np.array(x)

    # randomly shuffle input
    np.random.shuffle(x)

    # define train/test split
    thr = 80
    split = int(len(x) * thr / 100)
    train_x = x[0:split, :]
    test_x = x[split:, :]

    # initialize object of class Autoencoder
    AE = Autoencoder(n_steps, lr, cu, activation=activ, nh1=nh1, seed=0)

    # train AE network
    history, ws, bs, train_x_rec, train_cu, test_x_rec, test_cu = AE.train_network(
        train_x, x_test=test_x
    )
    # history, ws, bs, train_x_rec, train_cu, test_x_rec, test_cu = AE.train_vae(train_x, beta=0.00035, x_test=test_x)
    print("AE has been trained.")

    # save weights and biases
    if not os.path.exists(drPath):
        os.makedirs(drPath)
    for layer in range(3):
        np.savetxt(drPath + "weights" + str(layer + 1) + ".txt", ws[layer])
        np.savetxt(drPath + "biases" + str(layer + 1) + ".txt", bs[layer])

    print("BoMI forward map (AE parameters) has been saved.")

    # compute train/test VAF
    print(f"Training VAF: {compute_vaf(train_x, train_x_rec)}")
    print(f"Test VAF: {compute_vaf(test_x, test_x_rec)}")

    # normalize latent space to fit the monitor coordinates
    # Applying rotation
    rot = 0
    train_cu[0] = train_cu[0] * np.cos(np.pi / 180 * rot) - train_cu[1] * np.sin(
        np.pi / 180 * rot
    )
    train_cu[1] = train_cu[0] * np.sin(np.pi / 180 * rot) + train_cu[1] * np.cos(
        np.pi / 180 * rot
    )
    # Applying scale
    scale = [r.width / np.ptp(train_cu[:, 0]), r.height / np.ptp(train_cu[:, 1])]
    train_cu = train_cu * scale
    # Applying offset
    off = [
        r.width / 2 - np.mean(train_cu[:, 0]),
        r.height / 2 - np.mean(train_cu[:, 1]),
    ]
    train_cu = train_cu + off

    # Plot latent space
    plt.figure()
    plt.scatter(train_cu[:, 0], train_cu[:, 1], c="green", s=20)
    plt.title("Projections in workspace")
    plt.axis("equal")

    # save AE scaling values
    with open(drPath + "rotation_dr.txt", "w") as f:
        print(rot, file=f)
    np.savetxt(drPath + "scale_dr.txt", scale)
    np.savetxt(drPath + "offset_dr.txt", off)

    print("AE scaling values has been saved. You can continue with customization.")


def load_bomi_map(dr_mode, drPath):
    if dr_mode == "pca":
        map = pd.read_csv(drPath + "weights1.txt", sep=" ", header=None).values
    elif dr_mode == "ae":
        ws = []
        bs = []
        ws.append(pd.read_csv(drPath + "weights1.txt", sep=" ", header=None).values)
        ws.append(pd.read_csv(drPath + "weights2.txt", sep=" ", header=None).values)
        ws.append(pd.read_csv(drPath + "weights3.txt", sep=" ", header=None).values)
        bs.append(pd.read_csv(drPath + "biases1.txt", sep=" ", header=None).values)
        bs[0] = bs[0].reshape((bs[0].size,))
        bs.append(pd.read_csv(drPath + "biases2.txt", sep=" ", header=None).values)
        bs[1] = bs[1].reshape((bs[1].size,))
        bs.append(pd.read_csv(drPath + "biases3.txt", sep=" ", header=None).values)
        bs[2] = bs[2].reshape((bs[2].size,))

        map = (ws, bs)

    return map


def initialize_customization(self, dr_mode, drPath, num_joints, joints):
    """
    initialize objects needed for online cursor control. Start all the customization threads as well
    :param self: CustomizationApplication tkinter Frame. needed to retrieve textbox values programmatically
    :param drPath: path to load the BoMI forward map
    :return:
    """

    # Create object of openCV, Reaching class and filter_butter3
    cap = cv2.VideoCapture(0)
    r = Reaching()
    filter_curs = FilterButter3("lowpass_4")

    # initialize target position
    reaching_functions.initialize_targets(r)

    # load BoMI forward map parameters for converting body landmarks into cursor coordinates
    map = load_bomi_map(dr_mode, drPath)

    # initialize MediaPipe Pose
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        smooth_landmarks=False,
    )

    # load scaling values saved after training AE for covering entire monitor workspace
    rot = pd.read_csv(drPath + "rotation_dr.txt", sep=" ", header=None).values
    scale = pd.read_csv(drPath + "scale_dr.txt", sep=" ", header=None).values
    scale = np.reshape(scale, (scale.shape[0],))
    off = pd.read_csv(drPath + "offset_dr.txt", sep=" ", header=None).values
    off = np.reshape(off, (off.shape[0],))

    # initialize lock for avoiding race conditions in threads
    lock = Lock()

    # global variable accessed by main and mediapipe threads that contains the current vector of body landmarks
    global body
    body = np.zeros((num_joints,))  # initialize global variable

    # start thread for OpenCV. current frame will be appended in a queue in a separate thread
    q_frame = queue.Queue()
    cal = 0
    opencv_thread = Thread(target=get_data_from_camera, args=(cap, q_frame, r, cal))
    opencv_thread.start()
    print("openCV thread started in customization.")

    # initialize thread for mediapipe operations
    mediapipe_thread = Thread(
        target=mediapipe_forwardpass,
        args=(holistic, mp_holistic, lock, q_frame, r, num_joints, joints),
    )
    mediapipe_thread.start()
    print("mediapipe thread started in customization.")

    # Define some colors
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    CURSOR = (0.19 * 255, 0.65 * 255, 0.4 * 255)

    pygame.init()

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # Open a new window
    size = (r.width, r.height)
    screen = pygame.display.set_mode(size)
    # screen = pygame.display.toggle_fullscreen()

    # -------- Main Program Loop -----------
    while not r.is_terminated:
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                r.is_terminated = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                    r.is_terminated = True
                if (
                    event.key == pygame.K_SPACE
                ):  # Pressing the space Key will click the mouse
                    pyautogui.click(r.crs_x, r.crs_y)

        if not r.is_paused:
            # Copy old cursor position
            r.old_crs_x = r.crs_x
            r.old_crs_y = r.crs_y

            # get current value of body
            r.body = np.copy(body)

            # apply BoMI forward map to body vector to obtain cursor position
            r.crs_x, r.crs_y = reaching_functions.update_cursor_position_custom(
                r.body, map, rot, scale, off
            )

            # Apply extra customization according to textbox values (try/except allows to catch invalid inputs)
            try:
                rot_custom = int(self.retrieve_txt_rot())
            except:
                rot_custom = 0
            try:
                gx_custom = float(self.retrieve_txt_gx())
            except:
                gx_custom = 1.0
            try:
                gy_custom = float(self.retrieve_txt_gy())
            except:
                gy_custom = 1.0
            try:
                ox_custom = int(self.retrieve_txt_ox())
            except:
                ox_custom = 0
            try:
                oy_custom = int(self.retrieve_txt_oy())
            except:
                oy_custom = 0

            # Applying rotation
            r.crs_x = r.crs_x * np.cos(np.pi / 180 * rot_custom) - r.crs_y * np.sin(
                np.pi / 180 * rot_custom
            )
            r.crs_y = r.crs_x * np.sin(np.pi / 180 * rot_custom) + r.crs_y * np.cos(
                np.pi / 180 * rot_custom
            )
            # Applying scale
            r.crs_x = r.crs_x * gx_custom
            r.crs_y = r.crs_y * gy_custom
            # Applying offset
            r.crs_x = r.crs_x + ox_custom
            r.crs_y = r.crs_y + oy_custom

            # Limit cursor workspace
            if r.crs_x >= r.width:
                r.crs_x = r.width
            if r.crs_x <= 0:
                r.crs_x = 0
            if r.crs_y >= r.height:
                r.crs_y = 0
            if r.crs_y <= 0:
                r.crs_y = r.height

            # Filter the cursor
            r.crs_x, r.crs_y = reaching_functions.filter_cursor(r, filter_curs)

            # Set target position to update the GUI
            reaching_functions.set_target_reaching_customization(r)

            # First, clear the screen to black. In between screen.fill and pygame.display.flip() all the draw
            screen.fill(BLACK)

            # draw cursor
            pygame.draw.circle(
                screen, CURSOR, (int(r.crs_x), int(r.crs_y)), r.crs_radius
            )

            # draw each test target
            for i in range(8):
                tgt_x = r.tgt_x_list[r.list_tgt[i]]
                tgt_y = r.tgt_y_list[r.list_tgt[i]]
                pygame.draw.circle(
                    screen, GREEN, (int(tgt_x), int(tgt_y)), r.tgt_radius, 2
                )

            # --- update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 50 frames per second
            clock.tick(50)

    # Once we have exited the main program loop, stop the game engine and release the capture
    pygame.quit()
    print("game engine object released in customization.")
    holistic.close()
    print("pose estimation object released terminated in customization.")
    cap.release()
    cv2.destroyAllWindows()
    print("openCV object released in customization.")


def save_parameters(self, drPath):
    """
    function to save customization values
    :param self: CustomizationApplication tkinter Frame. needed to retrieve textbox values programmatically
    :param drPath: path where to load the BoMI forward map
    :return:
    """
    # retrieve values stored in the textbox
    rot = int(self.retrieve_txt_rot())
    gx_custom = float(self.retrieve_txt_gx())
    gy_custom = float(self.retrieve_txt_gy())
    scale = [gx_custom, gy_custom]
    ox_custom = int(self.retrieve_txt_ox())
    oy_custom = int(self.retrieve_txt_oy())
    off = [ox_custom, oy_custom]

    # save customization values
    with open(drPath + "rotation_custom.txt", "w") as f:
        print(rot, file=f)
    np.savetxt(drPath + "scale_custom.txt", scale)
    np.savetxt(drPath + "offset_custom.txt", off)

    print("Customization values have been saved. You can continue with practice.")


# [ADD CODE HERE: check_mouse as function input]
def start_reaching(drPath, lbl_tgt, num_joints, joints, dr_mode, check_mouse):
    """
    function to perform online cursor control - practice
    :param drPath: path where to load the BoMI forward map and customization values
    :param check_mouse: tkinter Boolean value that triggers mouse control instead of reaching task
    :param lbl_tgt: label in the main window that shows number of targets remaining
    :return:
    """
    pygame.init()

    # [ADD CODE HERE] get value from checkbox - is mouse enabled? !!!!!!!!!!!!!!!!!!!
    ## Select Mouse button Callback function in use for this
    ############################################################

    # Define some colors
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    CURSOR = (0.19 * 255, 0.65 * 255, 0.4 * 255)

    # Create object of openCV, Reaching class and filter_butter3
    cap = cv2.VideoCapture(0)
    r = Reaching()
    filter_curs = FilterButter3("lowpass_4")

    if check_mouse == True:
        size = solution.size
    else:
        size = (r.width, r.height)

    # Open a new window
    screen = pygame.display.set_mode(size)
    # screen = pygame.display.toggle_fullscreen()

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # Initialize stopwatch for counting time elapsed in the different states of the reaching
    timer_enter_tgt = StopWatch()
    timer_start_trial = StopWatch()
    timer_practice = StopWatch()
    # initialize targets and the reaching log file header
    reaching_functions.initialize_targets(r)
    reaching_functions.write_header(r)

    # load BoMI forward map parameters for converting body landmarks into cursor coordinates
    map = load_bomi_map(dr_mode, drPath)

    # initialize MediaPipe Pose
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        smooth_landmarks=False,
    )

    # load scaling values for covering entire monitor workspace
    rot_dr = pd.read_csv(drPath + "rotation_dr.txt", sep=" ", header=None).values
    scale_dr = pd.read_csv(drPath + "scale_dr.txt", sep=" ", header=None).values
    scale_dr = np.reshape(scale_dr, (scale_dr.shape[0],))
    off_dr = pd.read_csv(drPath + "offset_dr.txt", sep=" ", header=None).values
    off_dr = np.reshape(off_dr, (off_dr.shape[0],))
    rot_custom = pd.read_csv(
        drPath + "rotation_custom.txt", sep=" ", header=None
    ).values
    scale_custom = pd.read_csv(drPath + "scale_custom.txt", sep=" ", header=None).values
    scale_custom = np.reshape(scale_custom, (scale_custom.shape[0],))
    off_custom = pd.read_csv(drPath + "offset_custom.txt", sep=" ", header=None).values
    off_custom = np.reshape(off_custom, (off_custom.shape[0],))

    # initialize lock for avoiding race conditions in threads
    lock = Lock()

    # global variable accessed by main and mediapipe threads that contains the current vector of body landmarks
    global body
    body = np.zeros((num_joints,))  # initialize global variable

    # start thread for OpenCV. current frame will be appended in a queue in a separate thread
    q_frame = queue.Queue()
    cal = 0
    opencv_thread = Thread(target=get_data_from_camera, args=(cap, q_frame, r, cal))
    opencv_thread.start()
    print("openCV thread started in practice.")

    # initialize thread for mediapipe operations
    mediapipe_thread = Thread(
        target=mediapipe_forwardpass,
        args=(holistic, mp_holistic, lock, q_frame, r, num_joints, joints),
    )
    mediapipe_thread.start()
    print("mediapipe thread started in practice.")

    # initialize thread for writing reaching log file
    wfile_thread = Thread(target=write_practice_files, args=(r, timer_practice))
    timer_practice.start()  # start the timer for PracticeLog
    wfile_thread.start()
    print("writing reaching log file thread started in practice.")
    print("cursor control thread is about to start...")

    # -------- Main Program Loop -----------
    while not r.is_terminated:
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                r.is_terminated = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                    r.is_terminated = True
                if (
                    event.key == pygame.K_p
                ):  # Pressing the p Key will pause/resume the game
                    reaching_functions.pause_acquisition(r, timer_practice)
                if (
                    event.key == pygame.K_SPACE
                ):  # Pressing the space Key will click the mouse
                    pyautogui.click(r.crs_x, r.crs_y)

        if not r.is_paused:
            # Copy old cursor position
            r.old_crs_x = r.crs_x
            r.old_crs_y = r.crs_y

            # get current value of body
            r.body = np.copy(body)

            # apply BoMI forward map to body vector to obtain cursor position.
            r.crs_x, r.crs_y = reaching_functions.update_cursor_position(
                r.body,
                map,
                rot_dr,
                scale_dr,
                off_dr,
                rot_custom,
                scale_custom,
                off_custom,
            )

            # Check if the crs is bouncing against any of the 4 walls:
            if r.crs_x >= r.width:
                r.crs_x = r.width
            if r.crs_x <= 0:
                r.crs_x = 0
            if r.crs_y >= r.height:
                r.crs_y = 0
            if r.crs_y <= 0:
                r.crs_y = r.height

            # Filter the cursor
            r.crs_x, r.crs_y = reaching_functions.filter_cursor(r, filter_curs)

            # if mouse checkbox was enabled do not draw the reaching GUI,
            # only change coordinates of the computer cursor !!!!!!!!!!!!!!!!!!!!!
            # [ADD CODE HERE] !!!!!!!!!!!!!!!!!!!!!
            ##Checking which device is selected
            if check_mouse == True:
                # if the checkbox for real mouse is selected move the real mouse according to the body movement and activate the clicking 
                if solution.check_real_mouse:
                    solution.move_real_mouse(r)
                    solution.click_real_mouse()
                # else if the checkbox for planar manipulator is selected move the planar manipulator according to the body movement
                elif solution.check_planar_manipulator:
                    solution.move_planar_manipulator(r)
                # else if the checkbox for kuka robot is selected move the kuka according to the body movement
                elif solution.check_kuka_robot:
                    solution.move_mobile_robot(r)
                else:
                    # else if the checkbox for the parallel manipulator is selected move the parallel manipulator according to the body movement
                    solution.move_parallel_manipulator(r)

            # else: do the reaching

            else:
                # Set target position to update the GUI
                reaching_functions.set_target_reaching(r)
                # First, clear the screen to black. In between screen.fill and pygame.display.flip() all the draw
                screen.fill(BLACK)
                # Do not show the cursor in the blind trials when the cursor is outside the home target
                if not r.is_blind:
                    # draw cursor
                    pygame.draw.circle(
                        screen, CURSOR, (int(r.crs_x), int(r.crs_y)), r.crs_radius
                    )

                # draw target. green if blind, state 0 or 1. yellow if notBlind and state 2
                if r.state == 0:  # green
                    pygame.draw.circle(
                        screen, GREEN, (int(r.tgt_x), int(r.tgt_y)), r.tgt_radius, 2
                    )
                elif r.state == 1:
                    pygame.draw.circle(
                        screen, GREEN, (int(r.tgt_x), int(r.tgt_y)), r.tgt_radius, 2
                    )
                elif r.state == 2:  # yellow
                    if r.is_blind:  # green again if blind trial
                        pygame.draw.circle(
                            screen, GREEN, (int(r.tgt_x), int(r.tgt_y)), r.tgt_radius, 2
                        )
                    else:  # yellow if not blind
                        pygame.draw.circle(
                            screen,
                            YELLOW,
                            (int(r.tgt_x), int(r.tgt_y)),
                            r.tgt_radius,
                            2,
                        )

                # Display scores:
                font = pygame.font.Font(None, 80)
                text = font.render(str(r.score), True, RED)
                screen.blit(text, (1250, 10))

                # --- update the screen with what we've drawn.
                pygame.display.flip()

                # After showing the cursor, check whether cursor is in the target
                reaching_functions.check_target_reaching(r, timer_enter_tgt)
                # Then check if cursor stayed in the target for enough time
                reaching_functions.check_time_reaching(
                    r, timer_enter_tgt, timer_start_trial, timer_practice
                )

                # update label with number of targets remaining
                tgt_remaining = 248 - r.trial + 1
                lbl_tgt.configure(text="Remaining targets: " + str(tgt_remaining))
                lbl_tgt.update()

                # --- Limit to 50 frames per second
                clock.tick(50)

    # Once we have exited the main program loop, stop the game engine and release the capture
    pygame.quit()
    print("game engine object released in practice.")
    # pose.close()
    holistic.close()
    print("pose estimation object released in practice.")
    cap.release()
    cv2.destroyAllWindows()
    print("openCV object released in practice.")


def get_data_from_camera(cap, q_frame, r, cal):
    """
    function that runs in the thread to capture current frame and put it into the queue
    :param cap: object of OpenCV class
    :param q_frame: queue to store current frame
    :param r: object of Reaching class
    :return:
    """
    while not r.is_terminated:
        if not r.is_paused:
            ret, frame = cap.read()
            q_frame.put(frame)
            # if cal == 1:
            #     cv2.imshow("current frame", frame)
    print("OpenCV thread terminated.")


def mediapipe_forwardpass(holistic, mp_holistic, lock, q_frame, r, num_joints, joints):
    """
    function that runs in the thread for estimating pose online
    :param pose: object of Mediapipe class used to predict poses
    :param mp_pose: object of Mediapipe class for extracting body landmarks
    :param lock: lock for avoiding race condition on body vector
    :param q_frame: queue where to append current webcam frame
    :param r: object of Reaching class
    :return:
    """
    global body
    while not r.is_terminated:
        if not r.is_paused:
            # not sure if we want to put try/catch here, just in case "ask forgiveness, not permission"
            # try:
            # get current frame from thread
            curr_frame = q_frame.get()
            body_list = []

            # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(curr_frame, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to pass by reference.
            image.flags.writeable = False
            results = holistic.process(image)

            if not results.pose_landmarks:
                continue
            if joints[0, 0] == 1:
                body_list.append(
                    results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x
                )
                body_list.append(
                    results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y
                )
            if joints[1, 0] == 1:
                body_list.append(
                    results.pose_landmarks.landmark[
                        mp_holistic.PoseLandmark.RIGHT_EYE
                    ].x
                )
                body_list.append(
                    results.pose_landmarks.landmark[
                        mp_holistic.PoseLandmark.RIGHT_EYE
                    ].y
                )
                body_list.append(
                    results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].x
                )
                body_list.append(
                    results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE].y
                )
            if joints[2, 0] == 1:
                body_list.append(
                    results.pose_landmarks.landmark[
                        mp_holistic.PoseLandmark.RIGHT_SHOULDER
                    ].x
                )
                body_list.append(
                    results.pose_landmarks.landmark[
                        mp_holistic.PoseLandmark.RIGHT_SHOULDER
                    ].y
                )
                body_list.append(
                    results.pose_landmarks.landmark[
                        mp_holistic.PoseLandmark.LEFT_SHOULDER
                    ].x
                )
                body_list.append(
                    results.pose_landmarks.landmark[
                        mp_holistic.PoseLandmark.LEFT_SHOULDER
                    ].y
                )
            if joints[3, 0] == 1 or joints[4, 0] == 1:
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.INDEX_FINGER_TIP
                    ].x
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.INDEX_FINGER_TIP
                    ].y
                )
            if joints[4, 0] == 1:
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.THUMB_TIP
                    ].x
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.THUMB_TIP
                    ].y
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.MIDDLE_FINGER_TIP
                    ].x
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.MIDDLE_FINGER_TIP
                    ].y
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.RING_FINGER_TIP
                    ].x
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.RING_FINGER_TIP
                    ].y
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.PINKY_TIP
                    ].x
                )
                body_list.append(
                    results.right_hand_landmarks.landmark[
                        mp_holistic.HandLandmark.PINKY_TIP
                    ].y
                )

            body_mp = np.array(body_list)
            q_frame.queue.clear()
            with lock:
                body = np.copy(body_mp)
            # except:
            #     print('Expection in mediapipe_forwardpass. Closing thread')
            #     r.is_terminated = True
    print("Mediapipe_forwardpass thread terminated.")


def write_practice_files(r, timer_practice):
    """
    function that runs in the thread for writing reaching log in a file
    :param r: object of Reaching class
    :param timer_practice: stopwatch that keeps track of elapsed time during reaching
    :return:
    """
    while not r.is_terminated:
        if not r.is_paused:
            starttime = time.time()

            log = (
                str(timer_practice.elapsed_time)
                + "\t"
                + "\t".join(map(str, r.body))
                + "\t"
                + str(r.crs_x)
                + "\t"
                + str(r.crs_y)
                + "\t"
                + str(r.block)
                + "\t"
                + str(r.repetition)
                + "\t"
                + str(r.target)
                + "\t"
                + str(r.trial)
                + "\t"
                + str(r.state)
                + "\t"
                + str(r.comeback)
                + "\t"
                + str(r.is_blind)
                + "\t"
                + str(r.at_home)
                + "\t"
                + str(r.count_mouse)
                + "\t"
                + str(r.score)
                + "\n"
            )

            with open(r.path_log + "PracticeLog.txt", "a") as file_log:
                file_log.write(log)

            # write @ 50 Hz
            time.sleep(0.033 - ((time.time() - starttime) % 0.033))

    print("Writing reaching log file thread terminated.")


# CODE STARTS HERE
if __name__ == "__main__":
    # initialize mainApplication tkinter window
    win = tk.Tk()
    win.title("BoMI Settings")
    # Brain-Computer-Interface
    window_width = 1536  # 1200
    window_height = 864  # 520

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    win.geometry(
        "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate)
    )
    # Add image file
    bg = tk.PhotoImage(file="elctrobrain.png")

    # Show image using label
    label1 = Label(win, image=bg)
    label1.place(x=0, y=0)

    MainApplication(win)

    # initiate Tkinter mainloop
    win.mainloop()
