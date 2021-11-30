from os import name
from typing import Tuple


class Point:
    def __init__(self,name,x,y) -> None:
        self.name = name
        self.x = x
        self.y = y

    def name(self):
        return self.name
    
    def __str__(self):
        return 'Point {name} at x={x},y={y}'.format(name = self.name, x = self.x, y = self.y)

    def __eq__(self, other: object) -> bool:
        if(isinstance(other,Point)):
            if(self.name == other.name):
                return True
            else:
                return False
        else:
            raise Exception("The Type must be Point")

class Line:
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b
        self.A = 0
        self.B = 0
        self.C = 0

    def name(self):
        return self.a + self.b
    
    def __str__(self):
        return 'Line from {x} to {y}'.format(x = self.a, y = self.b)

    def __eq__(self, other: object) -> bool:
        if(isinstance(other,Line)):
            if(self.a == other.a and self.b == other.b or self.a == other.b and self.b == other.a):
                return True
            else:
                return False
        else:
            raise Exception("The Type must be Line")
    


class Ponl:
    def __init__(self,point,line) -> None:
        self.point = point
        self.line = line
    def __str__(self):
        return 'Point {point} on line {line}'.format(point = self.point, line = self.line)
    

class Angle:
    def __init__(self,la,lb) -> None:
        self.la = la
        self.lb = lb

class Triangle:
    def __init__(self,la,lb,lc) -> None:
        self.la = la
        self.lb = lb
        self.lc = lc

class Quad:
    def __init__(self,la,lb,lc,ld) -> None:
        self.la = la
        self.lb = lb
        self.lc = lc
        self.ld = ld

class Relation:
    def __init__(self,val) -> None:
        self.val = val