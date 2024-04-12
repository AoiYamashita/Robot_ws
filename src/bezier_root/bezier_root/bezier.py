import numpy as np
import rclpy
from rclpy.node import Node
from coordinate_msg.msg import Coordinate

def calcbesier(points):#points as ndarray
    Vector = [np.array([0,0])]
    Scale = 0.2
    timeSep = 30
    for i in range(1,points.shape[0]-1):
        vec0 = points[i]-points[i-1]
        vec1 = points[i+1]-points[i]
        Vector.append(vec0+vec1)
    Vector.append(np.array([0,0]))
    Vector = np.array(Vector)*Scale
    root = []
    ver = []
    p = [0,0]
    for i in range(Vector.shape[0]-1):
        for q in range(timeSep):
            t = q/timeSep
            v = points[i]*(1-t)**3+ 3*(points[i]+Vector[i])*t*(1-t)**2+3*(points[i+1]-Vector[i+1])*(1-t)*t**2+points[i+1]*t**3 - p
            p = points[i]*(1-t)**3+ 3*(points[i]+Vector[i])*t*(1-t)**2+3*(points[i+1]-Vector[i+1])*(1-t)*t**2+points[i+1]*t**3
            ver.append(v*5)
            root.append(p)
    return np.array(root),np.array(ver)

class Bezier(Node):
    def __init__(self):
        super().__init__("bezier")
        self.subscription = self.create_subscription(Coordinate,"CheckPoint",self.cb,10)
        self.publisher = self.create_publisher(Coordinate,"Root",10)
    def cb(self,data):
        x = np.array(data.x[:])
        y = np.array(data.y[:])
        coordData = np.array([x[:],y[:]]).T
        root,vec = calcbesier(coordData)
        RootData = Coordinate()
        RootData.x = list(root.T[0])
        RootData.y = list(root.T[1])
        self.publisher.publish(RootData)

def main():
    rclpy.init()
    besier = Bezier()
    #try:
    rclpy.spin(besier)
