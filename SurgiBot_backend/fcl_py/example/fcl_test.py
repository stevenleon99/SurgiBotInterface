import numpy as np
import fcl


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


b1 = fcl.Cylinder(0.0425, 0.135)
b2 = fcl.Box(0.0585, 0.07, 0.045)


# R1 = np.array([[  0.7071068,  0.0000000,  0.7071068  ],
#               [  0.0000000,  1.0000000,  0.0000000  ],
#               [ -0.7071068,  0.0000000,  0.7071068 ]])
R1 = [ [ 0.95385867, -0.0956077 ,  0.28462747],
       [ 0.09161592,  0.99541909,  0.02733781],
       [-0.28593733,  0.        ,  0.95824832]]
p1 = np.array([0.01921235, 0.0018453 , 0.20018176 ])
tf1 = fcl.Transform(R1, p1)

R2 = np.array([[ 0.30023637, -0.85539425, -0.42208862],
               [ 0.02883701, -0.43416167,  0.90037329],
               [-0.95342884, -0.28249658, -0.10568411]])
p2 = np.array([0.09438026,  0.00906501, 0.1874638 ])
tf2 = fcl.Transform(R2, p2)

o1 = fcl.CollisionObject(b1, tf1)
o2 = fcl.CollisionObject(b2, tf2)


request = fcl.CollisionRequest()
result = fcl.CollisionResult()
ret = fcl.collide(o1, o2, request, result)
print_collision_result("o1", "o2", result)

request = fcl.DistanceRequest(enable_nearest_points=True, enable_signed_distance=True)
result = fcl.DistanceResult()
ret = fcl.distance(o1, o2, request, result)
print_distance_result("o1", "o2", result)

