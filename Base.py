from os import name
from typing import Tuple
import math


class Point:
    def __init__(self,name: str,x: float,y: float) -> None:
        self.name = name
        self.x = x
        self.y = y

    def get_name(self):
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
    def __init__(self,a: Point,b: Point) -> None:
        self.a = a
        self.b = b
        self.A = 0
        self.B = 0
        self.C = 0
        self.get_equation()

    def get_equation(self):
        self.A = self.b.y - self.a.y
        self.B = self.a.x - self.b.x
        self.C = self.b.x * self.a.y - self.a.x * self.b.y
        self.normalizing()
    
    def normalizing(self): #TODO: 保不准有bug
        def gcd(a,b):
            if(b == 0): return a
            return b if a % b == 0 else gcd(b, a % b)
        def get_gcd(a,b,c):
            # lis = [a,b,c]
            # lis.sort()
            # l1, l2, l3 = lis[0], lis[1], lis[2]
            return gcd(gcd(a,b),c)

        if(self.A != 0):
            if(self.A < 0):
                self.A, self.B, self.C = -self.A, -self.B, -self.C
        else:
            if(self.B < 0):
                self.B, self.C = -self.B, -self.C
        t = get_gcd(abs(self.A), abs(self.B), abs(self.C))
        self.A = self.A / t #t couldnt be zero
        self.B = self.B / t
        self.C = self.C / t
                

    def get_name(self):
        return self.a.get_name() + self.b.get_name()
    
    def __str__(self):
        return 'Line from {x}({a},{b}) to {y}({c},{d}), Equation is:{A}x + {B}y + {C} = 0'.format(
                x = self.a.get_name(),a = self.a.x,b = self.a.y, 
                y = self.b.get_name(),c = self.b.x,d = self.b.y,
                A = self.A,B = self.B,C = self.C
            )

    def __eq__(self, other: object) -> bool:
        if(isinstance(other,Line)):
            if(self.a == other.a and self.b == other.b or self.a == other.b and self.b == other.a):
                return True
            else:
                return False
        else:
            raise Exception("The Type must be Line")
    


class Ponl:
    def __init__(self,point: Point,line: Line) -> None:
        self.point = point
        self.line = line
    def __str__(self):
        return 'Point {point} on line {line}'.format(point = self.point.get_name(), line = self.line.get_name())
    

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