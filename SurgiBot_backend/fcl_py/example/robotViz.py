#
# Created on Fri Apr 19 2024 09:40:04
#
# Author by Steve Liu
#
# Discription: 
# Simulate the collision situation for Meca500 robotic arm
# The geometry is simplified Meca500 robotic arm
# Unit is in "meter(m)"


import skrobot
import time
from skrobot.model.primitives import Axis
from skrobot.model.primitives import Box, Cylinder
import numpy as np

path = "D:/SurgiBot/SurgiBot_backend/fcl_py/urdf/robot.urdf"
robot_model = skrobot.models.urdf.RobotModelFromURDF(urdf_file=path)

# world coordinate
world_coords = skrobot.coordinates.Coordinates([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
# obstacle center
obs_c = [0.2, 0, 0]
obs_coords = skrobot.coordinates.Coordinates(obs_c, [0.0, 0.0, 0.0])

#show link names
print("###########link_list###########")
for link in robot_model.link_list:
   print(link.name)

#show joint names
print("###########joint_list###########")
for joint in robot_model.joint_list:
    print(joint.name)

# #set joint values
# print("###########set joint value###########")
# robot_model.robot_joint1.joint_angle(0.09575396281725412)
# print(robot_model.robot_joint1.joint_angle())
# robot_model.robot_joint2.joint_angle(0.28998445103667736)
# robot_model.robot_joint3.joint_angle(0.9744225867485715)
# robot_model.robot_joint4.joint_angle(1.9287843711404111)
# robot_model.robot_joint5.joint_angle(0.8904314020438977)
# robot_model.robot_joint6.joint_angle(0.5)
 

# obstacle
box = Box(extents=[0.2, 0.3, 0.4], with_sdf=True)
box.translate(np.array(obs_c))
viewer = skrobot.viewers.TrimeshSceneViewer(resolution=(640, 480))
viewer.add(robot_model)
viewer.add(Axis(pos=world_coords.worldpos(), rot=world_coords.worldrot(), axis_length=0.7))
viewer.add(Axis(pos=obs_coords.worldpos(), rot=obs_coords.worldrot(), axis_length=0.15))
viewer.add(box)
viewer.show()

print("###############################")
print("press f: %20s" %("full screen"))
print("press G: %20s" %("show underground"))
print("press q: %20s" %("quit"))

cur_j = [0,0,0,0,0]

while not viewer.has_exit:
    time.sleep(0.1)
    viewer.redraw()
    
    print("current joint: ", cur_j)
    i_ = input("please provide user input: ")
    
    if (i_ == "e"):
        print("moving joint1 by 0.1")
        cur_j[0] += 0.1
        robot_model.robot_joint1.joint_angle(cur_j[0])
    elif (i_ == "r"):
        print("moving joint1 by -0.1")
        cur_j[0] -= 0.1
        robot_model.robot_joint1.joint_angle(cur_j[0])
    elif (i_ == "t"):
        print("moving joint2 by 0.1")
        cur_j[1] += 0.1
        robot_model.robot_joint2.joint_angle(cur_j[1])
    elif (i_ == "y"):
        print("moving joint1 by -0.1")
        cur_j[1] -= 0.1
        robot_model.robot_joint2.joint_angle(cur_j[1])
    elif (i_ == "u"):
        print("moving joint1 by 0.1")
        cur_j[2] += 0.1
        robot_model.robot_joint3.joint_angle(cur_j[2])
    elif (i_ == "i"):
        print("moving joint1 by -0.1")
        cur_j[2] -= 0.1
        robot_model.robot_joint3.joint_angle(cur_j[2])
    elif (i_ == "o"):
        print("moving joint1 by 0.1")
        cur_j[3] += 0.1
        robot_model.robot_joint4.joint_angle(cur_j[3])
    elif (i_ == "p"):
        print("moving joint1 by -0.1")
        cur_j[3] += 0.1
        robot_model.robot_joint4.joint_angle(cur_j[3])
    elif (i_ == "k"):
        print("moving joint1 by 0.1")
        cur_j[4] += 0.1
        robot_model.robot_joint5.joint_angle(cur_j[4])
    elif (i_ == "l"):
        print("moving joint1 by -0.1")
        cur_j[4] += 0.1
        robot_model.robot_joint5.joint_angle(cur_j[4])    