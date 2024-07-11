import fcl
import numpy as np

def print_distance_result(o1_name, o2_name, result):
    print(f"Distance between {o1_name} and {o2_name}:")
    print("-" * 30)
    print(f"Distance: {result.min_distance}")
    print("Closest Points:")
    print(result.nearest_points[0])
    print(result.nearest_points[1])
    print("")


def print_collision_result(o1_name, o2_name, result):
    print(f"Collision between {o1_name} and {o2_name}:")
    print("-" * 30)
    print(f"Collision?: {result.is_collision}")
    print(f"Number of contacts: {len(result.contacts)}")
    print("") 

def forwardKinematics(joint_list:list):
    """
    @param: joint_list
    @return: [[R, T],] for rotation axis list
    @return: [[R, T],] for geometry center list
    @return: [R, T] TCP pose
    """
    rot_axis = []
    geo_center = []
    tcp = []
    
    # plesae refer to fcl_py/urdf/dummyRobot.png
    # from world to base_link_1 frame
    Tw_b1 = np.eye(4)
    # from base_link_1 to base_link_2 frame
    Tb1_b2 = np.array([[ np.cos(joint_list[0]), -np.sin(joint_list[0]),  0,      0],
                       [ np.sin(joint_list[0]),  np.cos(joint_list[0]),  0,      0],
                       [                     0,                      0,  1,  0.091],
                       [                     0,                      0,  0,      1]])
    # from base_link_2 to shoulder frame
    Tb2_s = np.array([ [ np.cos(joint_list[1]), 0, np.sin(joint_list[1]),       0],
                       [                     0, 1,                     0,       0],
                       [-np.sin(joint_list[1]), 0, np.cos(joint_list[1]),  0.0445],
                       [                     0, 0,                     0,       1]])
    # from shoulder to elbow frame
    Ts_e = np.array([  [np.cos(joint_list[2]),  0, np.sin(joint_list[2]),       0],
                       [                     0, 1,                     0,       0],
                       [-np.sin(joint_list[2]), 0, np.cos(joint_list[2]),   0.135],
                       [                     0, 0,                     0,       1]])
    # from elbow to wrist_1 frame
    Te_w1 = np.array([ [ 1,                      0,                      0,    0.0615],
                       [ 0,  np.cos(joint_list[3]),  np.sin(joint_list[3]),         0],
                       [ 0, -np.sin(joint_list[3]),  np.cos(joint_list[3]),   0.03025],
                       [ 0,                      0,                      0,         1]])
    # from wrist_1 to wrist_2 frame
    Tw1_w2 = np.array([[ np.cos(joint_list[4]), 0, np.sin(joint_list[4]),  0.0585],
                       [                     0, 1,                     0,       0],
                       [-np.sin(joint_list[4]), 0, np.cos(joint_list[4]),       0],
                       [                     0, 0,                     0,       1]])

    
    rot_axis.append(Tw_b1)
    rot_axis.append(np.matmul(rot_axis[0], Tb1_b2))
    rot_axis.append(np.matmul(rot_axis[1], Tb2_s))
    rot_axis.append(np.matmul(rot_axis[2], Ts_e))
    rot_axis.append(np.matmul(rot_axis[3], Te_w1))
    rot_axis.append(np.matmul(rot_axis[4], Tw1_w2))
    
    geo_trans1 = np.eye(4)
    geo_trans1[0:3, 3] = [0, 0, 0.0455]
    geo_center.append(np.matmul(rot_axis[0], geo_trans1))
    geo_trans2 = np.eye(4)
    geo_trans2[0:3, 3] = [0, 0, 0.03875]
    geo_center.append(np.matmul(rot_axis[1], geo_trans2))
    geo_trans3 = np.eye(4)
    geo_trans3[0:3, 3] = [0, 0, 0.0675]
    geo_center.append(np.matmul(rot_axis[2], geo_trans3))
    geo_trans4 = np.eye(4)
    geo_trans4[0:3, 3] = [0.017, 0, 0.03025]
    geo_center.append(np.matmul(rot_axis[3], geo_trans4))
    geo_trans5 = np.eye(4)
    geo_trans5[0:3, 3] = [0.02925, 0, 0]
    geo_center.append(np.matmul(rot_axis[4], geo_trans5))
    geo_trans6 = np.eye(4)
    geo_trans6[0:3, 3] = [0.035, 0, 0]
    geo_center.append(np.matmul(rot_axis[5], geo_trans6))
    
    tcp_trans = np.eye(4)
    tcp_trans[0:3, 3] = [0.07, 0, 0]
    tcp = np.matmul(rot_axis[5], tcp_trans)
    
    # print(tcp)
    
    return rot_axis, geo_center, tcp


if __name__ == "__main__":
    rot_axis, geo_center, tcp = forwardKinematics([0, 1.3, 0.7, 0, 0])
    
    """_summary_FCL pairwise collision detection validation: 
    
    # b1 = fcl.Box(0.07, 0.07, 0.045)
    # c1 = fcl.Cylinder(0.05, 0.091)
    # print(geo_center[5])
    # print(geo_center[0])
    # R1 = geo_center[5][0:3, 0:3]
    # T1 = geo_center[5][0:3, 3]
    # R2 = geo_center[0][0:3, 0:3]
    # T2 = geo_center[0][0:3, 3]
    # tf1 = fcl.Transform(R1 , T1)
    # tf2 = fcl.Transform(R2 , T2)
    # o1 = fcl.CollisionObject(b1, tf1)
    # o2 = fcl.CollisionObject(c1, tf2)
    
    # request = fcl.CollisionRequest()
    # result = fcl.CollisionResult()
    # ret = fcl.collide(o1, o2, request, result)
    # print_collision_result("o1", "o2", result)

    
    # request = fcl.DistanceRequest(enable_nearest_points=True, enable_signed_distance=True)
    # result = fcl.DistanceResult()
    # ret = fcl.distance(o1, o2, request, result)
    # print_distance_result("o1", "o2", result)
    
    """
    
    
    