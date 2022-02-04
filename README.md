<a href="https://unige.it/en/">
<img src="images/genoa_logo.png" width="20%" height="20%" title="University of Genoa" alt="University of Genoa" >
</a>

# Biomedical Robotics Final Project

## Project Members

|            Name            | Student ID |      Email Address       |
| :------------------------: | :--------: | :----------------------: |
|     Yara Abdelmottaleb     |  5066359   |   yara.ala96@gmail.com   |
|   Adedamola Ayodeji Sode   |  5360004   | adedamola.sode@yahoo.com |
|     Leonardo Borgioli      |  5359961   | borgioli27@gmail.com     |
| Omotoye Shamsudeen Adekoya |  5066348   | adekoyaomotoye@gmail.com |

## Project Objectives

for more information about the project objectives [click here](docs/assignment_instructions.pdf)

## Link to Videos
The different videos demonstrating the project can be found [here](https://drive.google.com/drive/folders/1mqPmZlZjmXwdSp38TwOnLGj_f8_i_d6y?usp=sharing)

## Code description

The main features of the code may be found [click here](https://omotoye.github.io/markerlessBoMI_FaMa/)

## User Guide
1. First you need to follow the setup instructions on this [link](setup_instructions.md)
1. Install Coppeliasim EDU version [click here](https://www.coppeliarobotics.com/downloads), it will be necessary to control the robots. 
2. Run the `main_reaching.py` script (it could take some time to run) the following interface should appear:
 
![image](https://user-images.githubusercontent.com/72743858/152410128-0d1a43e0-89cc-447b-b098-9c3798f4aa47.png)

3. It works exactly like the previous one the main changes are in the `select device` part. 3 other devices can now be controlled in a really similar way. 
For example in the case of "planar manipulator":

- By selecting it two successive windows will appear and Coppeliasim will open on your computer as follows: 
![image](https://user-images.githubusercontent.com/72743858/152410958-648de308-8578-4f6c-8cb3-b421449068ae.png)

- Press the play ![image](https://user-images.githubusercontent.com/72743858/152411034-623de161-0f2d-41fe-839e-fb4128cd6f56.png) button to allows to link CoppeliaSim with the script.
- Execute the calibration and then the practice as in the previous cases (this last step may take some time).
- Now by moving the head the robot should move accordingly.
- To have better control we advise changing the view for a top one clicking on the icon below.

![image](https://user-images.githubusercontent.com/72743858/152435220-8d173692-96f9-4fc8-ab0b-164656d3706f.png)

 

## Available systems

Three different robots may be controlled thanks to the BOMI system: 
1. **RRR Planar manipulator**, made by us in the AUTOCAD program  [AUTODESKINVENTOR](https://www.autodesk.com/products/inventor-lt/overview?mktvar002=afc_fr_nmpi_ppc&AID=11043042&PID=8227014&gclsrc=aw.ds&ds_rl=1232386&ds_rl=1232407&ds_rl=1232410&SID=jkp_CjwKCAiAl-6PBhBCEiwAc2GOVKCKCVERaGmKnMb4ls1yjDRXe1MEFt0hfhDcdbmbsovZApgB4GwjxBoCvQ8QAvD_BwE&cjevent=4239846f852511ec8110083e0a180513&affname=8227014_11043042&cjdata=MXxZfDB8WXww)

The model is made in three parts which .obj file can be found in the `...\markerlessBoMI_FaMa-main\CoppeliaSim\Parts` folder. 

![image](https://user-images.githubusercontent.com/72743858/152412787-5c7ae4e0-c41f-43f7-bfe8-00d0dc972061.png)

In Coppeliasim to reduce time computation some basic shapes as been used as kinematic meshes, and the 3D meshes as visible ones. 

![image](https://user-images.githubusercontent.com/72743858/152413574-219d271b-4a1f-4fd2-af63-980a7db69f22.png)
![image](https://user-images.githubusercontent.com/72743858/152413817-d878e2db-bf0f-46ea-b528-eb4ff1a9006e.png)

The gripper instead is a model already implemented in Coppeliasim. 

2. **3-PRRR Planar Manipulator**, it is still in "beta" as the dimensions are not satisfactory and allow a small workspace. It's a parallel robot with only the prismatic joints actuated. The goal of such a device is to allow to have a large load without using too much power by limiting as possible the weight of actuators and their effects on inertial. 
The Kinematic model of such devices can be easily found in the literature (for example [here](
https://github.com/Omotoye/markerlessBoMI_FaMa/files/7997616/JPM_DirectKinematicsPlanarParallelManipulators.pdf)).
To go further on this topic an optimization algorithm could be used to optimize the lengths of the different links as suggested [on this paper](https://github.com/Omotoye/markerlessBoMI_FaMa/files/7997633/CIRP_Design_2010_Book_Caro_Chablat_UrRehman_Wenger.pdf).

![image](https://user-images.githubusercontent.com/72743858/152417492-2eb13b37-a8b4-484b-9733-f9387f4b4648.png)

3. **Kukka Mobile Robot**, this system is composed of 4 actuated Swedish Wheels (allowing also a translation along the perpendicular axis to the chassis).

![image](https://user-images.githubusercontent.com/72743858/152420317-4648a47d-70bf-4f0a-8623-e3362d1847dc.png)











