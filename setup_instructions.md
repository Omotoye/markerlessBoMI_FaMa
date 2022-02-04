# Abstract

# UBUNTU installation steps:

**TESTED with python>=3.7**

step 0 --> open a terminal and cd to the home folder:

```
    $ cd
```

step 1 --> [if not done yet] install pip and venv:

```
    $ sudo apt-get update
    $ sudo apt install python3-pip
    $ sudo apt install build-essential libssl-dev libffi-dev python3-dev
    $ sudo apt install python3-venv
```

step 2 --> create a virtual environment called BoMI:

```
    $ python3 -m venv BoMI
```

step 3 --> activate virtual enviroment:

```
    $ source BoMI/bin/activate
```

step 4 --> upgrade pip and install all the packages nedded for markerlessBoMI:

```
    $ pip install --upgrade pip
    $ pip install git+https://github.com/Omotoye/markerlessBoMI_FaMa
```

step 5 --> istall tkinter:

```
    $ sudo apt install python3-tk
```

step 6 --> clone the github repository:

```
    $ git clone https://github.com/Omotoye/markerlessBoMI_FaMa
```

step 7 --> cd in the correct folder and run main_reaching.py:

```
    $ cd markerlessBoMI_FaMa/
    $ python3 main_reaching.py
```

step 8 --> follow the steps in the GUI (see below after WINDOWS installation steps)

# MAC installation steps:

**TESTED with python>=3.7**

step 0 --> install python (if not already installed), pip and virtualenv

step 1 --> create a virtual environment called BoMI:

```
    $ python3 -m venv BoMI
```

step 2 --> activate virtual enviroment:

```
    $ source BoMI/bin/activate
```

step 3 --> upgrade pip and install all the packages nedded for markerlessBoMI:

```
    $ pip install --upgrade pip
    $ pip install git+https://github.com/Omotoye/markerlessBoMI_FaMa
```

step 4 --> istall tkinter:

```
    $ pip install tk
```

step 5 --> clone the github repository:

```
    $ git clone https://github.com/Omotoye/markerlessBoMI_FaMa
```

step 6 --> cd in the correct folder and run main_reaching.py:

```
    $ cd markerlessBoMI_FaMa/
    $ python3 main_reaching.py
```

step 7 --> follow the steps in the GUI (see below after WINDOWS installation steps)

# WINDOWS installation steps:

**TESTED with python>=3.7**

step 0 --> download Python3 at this link https://www.python.org/downloads/ [**During installation select Add Python to PATH**]

step 1 --> enable long path (https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/) --> remember to launch regedit as root ("amministratore")

step 2 --> open a command window (terminal) as root ("amministratore") and type

```
    $ cd
```

step 3 --> install pip and virtualenv

```
    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py
    $ pip install virtualenv
```

step 4 --> create virtualenv (named BoMI) and activate it

```
    $ python -m venv BoMI
    $ BoMI\Scripts\activate
```

step 5 --> Upgrade pip and download all the packages (you should be in the folder where requirments.txt is). In the terminal type:

```
    $ pip install --upgrade pip
    $ pip install -r requirments.txt
```

If the line before does not work, download all the following packages (in the terminal):

```
    $ pip install numpy
    $ pip install pandas
    $ pip install matplotlib
    $ pip install pygame
    $ pip install pyautogui
    $ pip install tensorflow
    $ pip install mediapipe
    $ pip install scipy
    $ pip install sklearn
    $ pip install opencv-python
```

step 6 --> Download Visual Studio Code (https://code.visualstudio.com/download)

Step 7 --> Download the repository from the current github page and open it as a folder in Visual Studio Code

step 8 --> Download 'python extension' for Visual Studio Code (on the left side select 'Extensions' and download python)

step 9 --> Set the correct python interpreter (the one of the virtual environment created - BoMI\Scripts\python) in Visual Studio Code from the bottom left corner: left click on the bottom left corner and follow the instruction searching for BoMI\Scripts\python.

step 10 --> eventually [not always] there is the possibility that it is necessary to do the steps described here https://support.microsoft.com/help/2977003/the-latest-supported-visual-c-downloads

step 11 --> On Visual Studio Code run the file main_reaching.py

# Graphical User Interface

[**READ CAREFULLY UNTIL THE END**]
If you run the script main_reaching.py, you should see something like this:

![BoMI_0](https://user-images.githubusercontent.com/75327840/142367411-f78e3f09-481a-4edd-95c4-f8a23778b0e2.png)
Figure 1. Markerless BoMI GUI.

**Step 1: Select Joints**. As you can notice, only the button **Select Joints** is available. You should select the anatomical joints you want to use to control the cursor (click on the corresponding checkbox, try for example **Nose** and **Shouders**), and, then, press **Select Joints**:

![BoMI_1](https://user-images.githubusercontent.com/75327840/142368575-1152f407-1e94-474d-acee-292905ff7db8.png)
Figure 2. Select the anatomical points you want to use to control the cursor and then press Select Joints.

After this step, also the others buttons should be visible. To complete the task, you have to follow the following steps **in order**.

**Step 2: Calibration**. During the calibration step, you should move the anatomical points you selected during the previous step facing your webcam. Make sure only you are visible from the webcam with nobody else (only one person should be visible). Press the button **Calibration**: a new window will pop up (see Figure 3). Press **ok** and start moving your joints facing the webcam for 30 seconds (a countdown as in Figure 4 will appear). **During the calibration try to cover with your movements all the space seen by your webcam**. The calibration is an important step and it is possible that you have to do it multiple times.

![BoMI_3](https://user-images.githubusercontent.com/75327840/142370385-1e202942-34ce-4f54-8f0b-eb73aa30f8cc.png)
Figure 3. Window that will pop up after pressing the button **Calibration**. Press **ok** and start moving your selected joints.

![BoMI_4](https://user-images.githubusercontent.com/75327840/142370626-20db02ec-17ff-48bf-bf3b-af29bd5de480.png)
Figure 4. Countdown during calibration. You should move for 30 seconds.

**Step 3: Calculate BoMI Map**. **Before** pressing the button, select the checkbox correspondent to the dimensionality reduction algorithm you want to use. By default 'PCA' is selected (see Figure 2). If you want to change it, deselect the checkbox near 'PCA' and select another one. We suggest to use **Variational AE** (variational autoencoder) as in Figure 5. **After** that, you can press the button **Calculate BoMI Map**. A new window similar to the one in Figure 3 will pop up. Press **ok** and **wait** some seconds (needed to calculate the BoMI Map - have a look at the terminal, you should see when the process is done.

![BoMI_5](https://user-images.githubusercontent.com/75327840/142371433-4a5e15af-4301-4702-8ab4-746d46aa2f0e.png)
Figure 5. Select Variational AE and, then, press Calculate BoMI Map.

**Step 4: Customization**. When the Calculate BoMI Map step is done (look at the terminal), you can press the button **Customization**. A window as the one shown in Figure 6 should pop up.

![BoMI_6](https://user-images.githubusercontent.com/75327840/142372287-21feb4e8-2e72-4f97-acb8-75aa4648dd1c.png)
Figure 6. Window that will pop up after pressing the **Customization** button.

At this point you can press the button **Start**. A window as the one in Figure 7 should appear. **If you move the joints selected, you should see the small green dot (virtual cursor) moving**. The default parameters suggested in the window (Figure 6) should be fine to cover all the space. If yes, close the window in Figure 7 and press **Save Parameters**. If you notice some problems (for example you can not reach with your movements some target of the window in Figure 7 with the green virtual cursor), you have to close the window in Figure 7, change the parameters in the Figure 6 and then press the button **Start**. You should repet this process until all the targets of the window in Figure 7 are reachable. At the end press **Save Parameters**.

![BoMI_7](https://user-images.githubusercontent.com/75327840/142373973-f321173b-e6fd-4f0c-8aee-1ace747f4785.png)
Figure 7. Window to tune the customization parameters.

**Step 5: Practice**. When you finish with the customization step, you can press the button **Pratice** and a window as the one in Figure 8 will appear. At this point you will start the **reaching task**.
**[IMPORTANT!! If for any reason you are stuck and you want to close the application press the key 'p' in your keyboard and it will pause the program]**

The reaching task is composed of many steps (almost 300, you will take ~45 minutes to finish it and you should do it without interrupting). You should move your joints in order to move the green dot (virtual cursor) in order to reach the targets that appear in the screen. Once reached, the targets color become yellow. You have to stay inside the target for some milliseconds and then you will see another target appearing somewhere in the screen. Keep going until the end. Two events could happen: (i) sometimes the virtual cursor disappear for some seconds (~15s); you should try to reach the target as always but without having the visual feedback of where the virtual cursor is. If you can not reach it before ~15s the virtual cursor will appear again and you will be able to reach the target with the visual feedback. (ii) After some trial, periodically, the virtual cursor will freeze in order to give you the possibility to do a small break. If you want to continue the task, press the key 'p' on your keyboard.

**[VERY IMPORTANT, for robotics students!! At the end of the practice, inside the folder markerlessBoMI_FaMa, you will see that a folder called 'Practice' will be created. Inside it you will find a file called 'PracticeLog.txt'. Rename it if you want to do multiple practice.]** Anyway, at the end of each practice (the ones during which you reach the very end) rename the file 'PracticeLog.txt' with your 'Name_Surname.txt' and send it to matteo.moro@edu.unige.it. In the email you should indicate the joints you selected for the task (the easiest ones are nose and/or shoulders), the dimensionality reduction algorithm you used (PCA, AE, Variational AE) and the specifics of the computer where you performed it (CPU, if you have a GPU, etc ....).

![BoMI_8](https://user-images.githubusercontent.com/75327840/142374722-5f860b01-58fd-4293-882d-bfee32afd507.png)
Figure 8. Start the reaching task.
