import math
from model.topology import Vertex

def euler_from_quaternion(x, y, z, w):
    t0 = 2.0 * (w*x + y*z)
    t1 = 1.0 - 2.0 * (x*x + y*y)
    roll_x = math.atan2(t0, t1)

    t2 = 2.0 * (w*y - z*x)

    if t2 > 1.0:
        t2 = 1.0
    elif t2 < -1.0:
        t2 = -1.0
    
    pitch_y = math.asin(t2)

    t3 = 2.0 * (w*z + x*y)
    t4 = 1.0 - 2.0 * (y*y + z*z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z

def get_distance(src: Vertex, dst: Vertex):
    src_pts = [src.x, src.y]
    dst_pts = [dst.x, dst.y]

    return math.dist(src_pts, dst_pts)