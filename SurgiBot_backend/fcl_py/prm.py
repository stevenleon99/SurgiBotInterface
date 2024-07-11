#
# Created on Sat Apr 20 2024 19:08:20
#
# Author by Steve Liu
#
# Discription: PRM algorithm to build road map for MECA500
#

import fcl
import numpy as np
from util.kinematics import *
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

# joint limits
joint_range = {"joint1": [-3.0, 3.0],
               "joint2": [-1.2, 1.5],
               "joint3": [-2.3, 1,2],
               "joint4": [-2.9, 2.9],
               "joint5": [2.0, 2.0]}
# number of sample
N = 600
# assume workspace x, -x, y, -y, z, -z
ws = {"x": [ 0.10, 0.20],
      "y": [-0.10, 0.10],
      "z": [-0.05, 0.20]}

b1 = fcl.Cylinder(0.05, 0.091)
b2 = fcl.Box(0.085, 0.1, 0.0775)
b3 = fcl.Cylinder(0.0425, 0.135)
b4 = fcl.Box(0.089, 0.1, 0.0605)
b5 = fcl.Box(0.0585, 0.07, 0.045)
b6 = fcl.Box(0.07, 0.07, 0.045)
def selfCollision(geo_center) -> bool:
    R = [r[0:3, 0:3] for r in geo_center]
    T = [t[0:3, 3] for t in geo_center]
    tf = [fcl.Transform(r, t) for r, t in zip(R, T)]
    
    o1 = fcl.CollisionObject(b1, tf[0])
    o2 = fcl.CollisionObject(b2, tf[1])
    o3 = fcl.CollisionObject(b3, tf[2])
    o4 = fcl.CollisionObject(b4, tf[3])
    o5 = fcl.CollisionObject(b5, tf[4])
    o6 = fcl.CollisionObject(b6, tf[5])

    request = fcl.CollisionRequest()
    result = fcl.CollisionResult()
    fcl.collide(o1, o5, request, result)
    if result.is_collision:
        return True
    fcl.collide(o1, o6, request, result)
    if result.is_collision:
        return True
    fcl.collide(o2, o5, request, result)
    if result.is_collision:
        return True
    fcl.collide(o2, o6, request, result)
    if result.is_collision:
        return True
    fcl.collide(o3, o5, request, result)
    if result.is_collision:
        return True
    fcl.collide(o3, o6, request, result)
    if result.is_collision:
        return True
    return False
    
    
def viz_pts(points, plot_path=False, path=[]):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x_vals = [x[0] for x in points]
    y_vals = [x[1] for x in points]
    z_vals = [x[2] for x in points]

    ax.scatter(x_vals, y_vals, z_vals)
    
    # Vertices of a rectangular prism
    vertices = np.array([
        [ws["x"][0], ws["y"][0], ws["z"][0]],
        [ws["x"][0], ws["y"][0], ws["z"][1]],
        [ws["x"][0], ws["y"][1], ws["z"][0]],
        [ws["x"][0], ws["y"][1], ws["z"][1]],
        [ws["x"][1], ws["y"][0], ws["z"][0]],
        [ws["x"][1], ws["y"][0], ws["z"][1]],
        [ws["x"][1], ws["y"][1], ws["z"][0]],
        [ws["x"][1], ws["y"][1], ws["z"][1]]
    ])

    # Generate the list of sides' connections
    edges = [
        [vertices[0], vertices[1], vertices[3], vertices[2], vertices[0]],  # Side 1
        [vertices[4], vertices[5], vertices[7], vertices[6], vertices[4]],  # Side 2
        [vertices[0], vertices[1], vertices[5], vertices[4], vertices[0]],  # Side 3
        [vertices[2], vertices[3], vertices[7], vertices[6], vertices[2]],  # Side 4
        [vertices[1], vertices[3], vertices[7], vertices[5], vertices[1]],  # Side 5
        [vertices[0], vertices[2], vertices[6], vertices[4], vertices[0]]   # Side 6
    ]

    # Plot each side
    for edge in edges:
        Xs, Ys, Zs = zip(*edge)
        ax.plot(Xs, Ys, Zs, color="b")

    if plot_path:
        for i in range(1, len(path)):
            xs, ys, zs = zip(path[i], path[i-1])
            ax.plot(xs, ys, zs, color="g")
    
    ax.set_xlabel('X Coordinates')
    ax.set_ylabel('Y Coordinates')
    ax.set_zlabel('Z Coordinates')

    plt.show()


def interpolate(q1, q2, N):
    q= []
    for i in range(1, N):
        t = 1/N * i
        q.append((1-t) * q1 + t * q2)
    return q

def findtopK(target, q_list, topk):
    q_idx_picked = []
    # calculate the distance between target and all in q_list
    dist = []
    for q_e in q_list:
        dist.append(np.linalg.norm(target - q_e))
    # sort based on distance
    sorted_indices = sorted(enumerate(dist), key=lambda x: x[1])
    
    for i in range(1, topk+1): # leave the first one as target itself
        q_interpolate = interpolate(target , q_list[sorted_indices[i][0]], 10)
        iscollision = False
        for q_i in q_interpolate:
            _, geo_center, _ = forwardKinematics(q_i)
            if selfCollision(geo_center):
                iscollision = True
                break
        if not iscollision:
            q_idx_picked.append(sorted_indices[i][0])
    return q_idx_picked

def findpath(edge_picked, v_init, v_goal): #dijiastra algorithm
    path = []
    numNode = len(edge_picked.keys())
    dist = np.full(numNode, np.inf)
    prev = np.full(numNode, np.nan)
    
    dist[v_init] = 0
    
    unvisit = np.arange(0, numNode, 1)
    
    while v_goal in unvisit:
        c = mindistnode(dist, unvisit)
        unvisit[c] = -1
        
        vi = edge_picked[c] # all the neighborhood of c
        for i in range(len(vi)):
            alt = dist[c] + 1 # distance 1 to all neighborhood vertex
            if alt < dist[vi[i]]:
                dist[vi[i]] = alt
                prev[vi[i]] = c
                
    path.append(int(v_goal))

    while v_init not in path:
        cur = path[len(path)-1]
        path.append(int(prev[cur]))
    
    return list(reversed(path))  
        

def mindistnode(dist, unvisit):
    # get the index with minimal distance
    min_distance = sorted(enumerate(dist), key=lambda x : x[1])
    # if index in the unvisit list
    idx = -1
    for i in min_distance:
        if unvisit[i[0]] < 0:
            continue
        else:
            idx = i[0]
            break
    return idx
    
    
if __name__ == "__main__":
    
    vertexes = []
    # random sample in the configuration space
    np.random.seed(123)
    for _ , idx in enumerate(joint_range):
        v = np.random.rand(N)
        vertexes.append((joint_range[idx][0] + (joint_range[idx][1] - joint_range[idx][0])) * v)
    
    # create effective vertex list
    vertexes_picked = []
    tcp_picked = []
    for j1, j2, j3, j4, j5 in zip(vertexes[0], vertexes[1], vertexes[2], vertexes[3], vertexes[4]):
        _, geo_center, tcp = forwardKinematics([j1, j2, j3, j4, j5])
        tcp = tcp[0:3, 3]
        if (tcp[0]>=ws["x"][0] and tcp[0]<=ws["x"][1]) and (tcp[1]>=ws["y"][0] and tcp[1]<=ws["y"][1]) and (tcp[2]>=ws["z"][0] and tcp[2]<=ws["z"][1]) :
            if not selfCollision(geo_center):
                vertexes_picked.append([j1, j2, j3, j4, j5])
                tcp_picked.append(tcp)
            # else:
            #     print(j1, j2, j3, j4, j5)
    
    # print(len(vertexes_picked))
    viz_pts(tcp_picked)
    # print(len(vertexes_picked))
    
    # create effective edge list
    topk = 5
    edge_picked = {}
    for i in range(len(vertexes_picked)):
        topk_q_dix = findtopK(np.array(vertexes_picked[i]), np.array(vertexes_picked), topk)
        edge_picked[i] = topk_q_dix

    for idx, val in enumerate(edge_picked):
        print("%2d" %idx, ": ", edge_picked[idx])
        
        
    # create path from joint_init to joint_goal
    path = findpath(edge_picked, 5, 20)
    
    tcp_p = []
    for i in path:
        jt = vertexes_picked[i]
        _, _, tcp = forwardKinematics(jt)
        tcp_p.append(tcp[0:3, 3])
    viz_pts(tcp_picked, plot_path=True, path=tcp_p)
        