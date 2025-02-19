'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from .ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from .notch import Notch
from OCC.Core.gp import (gp_Vec, gp_Pnt, gp_Trsf, gp_OX, gp_OY,
                         gp_OZ, gp_XYZ, gp_Ax2, gp_Dir, gp_GTrsf, gp_Mat)
"""
                          ^ v
                              |
            c2                .                c1
     ---    +-----------------|-----------------+     ---
      ^     |                 .                 |      ^
      | T   |                 |                 |      |
      v     |                 .                 |      |
     ---    +------------+    |    +------------+      |
            b2         a2|         | a1         b1     |
                         |    t    |                   |
                         |<------->|                   |
                         |    |    |                   |
                         |    .    |                   |D
                         |    |O   |                   |
    -- -- -- -- -- -- -- -- --.-- -- -- -- -- -- -- -- |-- -- -> u
                         |    |    |                   |
                         |    .    |                   |
                         |    |    |                   |
                         |    .    |                   |
             b3        a3|    |    |a4          b4     |
             +-----------+    .    +------------+      |
             |                |                 |      |
             |                .                 |      |
             |                |                 |      v
             +----------------.-----------------+     ---
             c3               B                 c4
             |<-------------------------------->|

"""

class ISection(object):
    '''


    '''

    def __init__(self, B, T, D, t, R1, R2, alpha, length, notchObj):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.alpha = alpha
        self.length = length
        self.clearDist = 20
        self.notchObj = notchObj
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])

        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin + (self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b1 = self.sec_origin + (self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.c1 = self.sec_origin + (self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b2 = self.sec_origin + (-self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.c2 = self.sec_origin + (-self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a3 = self.sec_origin + (-self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.b3 = self.sec_origin + (-self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.c3 = self.sec_origin + (-self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.b4 = self.sec_origin + (self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.c4 = self.sec_origin + (self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        self.points = [self.a1, self.b1, self.c1,
                       self.c2, self.b2, self.a2,
                       self.a3, self.b3, self.c3,
                       self.c4, self.b4, self.a4]
        # self.points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

    def create_model(self):

        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.length * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)

        if self.notchObj is not None:
            uDir = numpy.array([-1.0, 0.0, 0])
            wDir = numpy.array([0.0, 1.0, 0.0])
            shiftOri = self.D / 2.0 * self.vDir + self.notchObj.width / 2.0 * self.wDir + self.B / 2.0 * -self.uDir  # + self.notchObj.width* self.wDir + self.T/2.0 * -self.uDir
            origin2 = self.sec_origin + shiftOri

            self.notchObj.place(origin2, uDir, wDir)

            notchModel = self.notchObj.create_model()
            prism = BRepAlgoAPI_Cut(prism, notchModel).Shape()

        return prism


if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    B = 40
    T = 3
    D = 50
    t = 2
    R1 = 5
    R2 = 5
    alpha = 1
    length = 200
    width = 10
    hight = 10
    notchObj = Notch(R1, hight, width, length)

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,1.,0.])

    ISec = ISection(B, T, D, t, R1, R2, alpha, length, notchObj)
    _place = ISec.place(origin, uDir, shaftDir)
    point = ISec.compute_params()
    prism = ISec.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
