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
        self.a = None
        self.b = None
        if(a.get_name() < b.get_name()):#FIXME: 我也不相信这段代码
            self.a, self.b = a, b
        else:
            self.a, self.b = b, a
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
    
    def __hash__(self) -> int: #FIXME: 正确性无法保证
        name = self.a.get_name() + self.b.get_name()
        return hash(name)
    


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
    def __init__(self,la: Line,lb: Line,lc: Line) -> None:
        self.la = la
        self.lb = lb
        self.lc = lc
        
    def __str__(self):
        return 'Triangle with line:{a},{b},{c}'.format(a=self.la.get_name(), b=self.lb.get_name(), c=self.lc.get_name())

class Quad:
    def __init__(self,la: Line,lb: Line,lc: Line,ld: Line) -> None:
        self.la = la
        self.lb = lb
        self.lc = lc
        self.ld = ld
    
    def __str__(self):
        return 'Quad with line:{a},{b},{c},{d}'.format(a=self.la.get_name(), b=self.lb.get_name(), c=self.lc.get_name(), d=self.ld.get_name())

class Relation:
    def __init__(self,val) -> None:
        self.val = val