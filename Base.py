from os import SEEK_CUR, name, set_inheritable
from typing import Tuple
import math
from typing import List
# from Gen_angle import *

class Point:
    def __init__(self,name: str,x: float,y: float) -> None:
        self.name = name
        self.x = x
        self.y = y

    def get_name(self) -> str:
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
    
    def __hash__(self) -> int: #FIXME: 正确性无法保证
        return hash("Point" + self.name)

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
                

    def get_name(self) -> str:
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
    def __init__(self,la: Line,lb: Line) -> None:
        self.la = la
        self.lb = lb

    def get_name(self) -> str: # just for UnionFind
        return "<" + self.la.get_name() + ", " + self.lb.get_name() + ">"
    
    def __str__(self) -> str:
        return 'Angle with line:{a},{b}'.format(a=self.la.get_name(), b=self.lb.get_name())

#TODO: 把这些代码移到其他地方去

pi = 3.14159265358979324

def gen_angle(point_a: Point, point_b: Point, mid_point: Point,x: float,y: float,R: float) -> Angle: #FIXME:
    def get_length(a: Point, b: Point):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    x1,y1 = point_a.x, point_a.y
    x2,y2 = point_b.x, point_b.y
    # mid_name = mid_point.name

    a = get_length(point_b, mid_point)
    b = get_length(point_a, mid_point)
    c = get_length(point_a, point_b)
    angleC = math.acos((a * a + b * b - c * c) / (2 * a * b))
    angleC = abs((angleC * 180) / pi)

    
    t = math.acos(((x1 - x) * (x2 - x) + (y1 - y) * (y2 - y)) / (R * R));
    if((x1 - x) * (y2 - y) - (x2 - x) * (y1 - y) < 0.0) : t += pi;
    t = (t * 180) / pi
    a = Angle(Line(point_a,mid_point),Line(point_b,mid_point))
    b = Angle(Line(point_b,mid_point),Line(point_a,mid_point))
    if(angleC > 90):
        a, b = b, a
    if(t < 180):
        return a
    return b

def gen_angle_for_triangle(point_list: List[Point]) -> dict:
    a = 2 * (point_list[1].x - point_list[0].x)
    b = 2 * (point_list[1].y - point_list[0].y)
    c = point_list[1].x * point_list[1].x + point_list[1].y * point_list[1].y - point_list[0].x * point_list[0].x - point_list[0].y * point_list[0].y
    d = 2 * (point_list[2].x - point_list[1].x)
    e = 2 * (point_list[2].y - point_list[1].y)
    f = point_list[2].x * point_list[2].x + point_list[2].y * point_list[2].y - point_list[1].x * point_list[1].x - point_list[1].y * point_list[1].y
    x = (b * f - e * c) / (b * d - e * a)
    y = (d * c - a * f) / (b * d - e * a)
    R = math.sqrt((x - point_list[0].x) ** 2 + (y - point_list[0].y) ** 2)

    # print("circle:{a},{b},{c}".format(a=x,b=y,c=R))

    angle_pair = dict()
    angle_pair[point_list[2].get_name()] = gen_angle(point_list[0],point_list[1],point_list[2],x,y,R)
    angle_pair[point_list[1].get_name()] = gen_angle(point_list[0],point_list[2],point_list[1],x,y,R)
    angle_pair[point_list[0].get_name()] = gen_angle(point_list[1],point_list[2],point_list[0],x,y,R)

    return angle_pair

class Triangle:
    def __init__(self,la: Line,lb: Line,lc: Line) -> None:
        self.la = la
        self.lb = lb
        self.lc = lc
        self.point_set = set()
        self.point_set.add(self.la.a)
        self.point_set.add(self.la.b)
        self.point_set.add(self.lb.a)
        self.point_set.add(self.lb.b)
        self.point_set.add(self.lc.a)
        self.point_set.add(self.lc.b)
        # print("Triangle test: ",self.get_name())
        lis = list(self.point_set)
        lis = [lis[0].get_name(), lis[1].get_name(), lis[2].get_name()]
        lis.sort()
        self.name = lis[0] + lis[1] + lis[2]
        self.angle_dict = gen_angle_for_triangle(list(self.point_set))
    
    def get_name(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if(isinstance(other,Triangle)):
            return self.point_set == other.point_set
        else:
            raise Exception("The Type must be Triangle")
    
    def __str__(self):
        return 'Triangle {name}'.format(name = self.name)

class Quad:
    def __init__(self,la: Line,lb: Line,lc: Line,ld: Line) -> None:
        self.la = la
        self.lb = lb
        self.lc = lc
        self.ld = ld
        self.point_set = set()
        self.point_set.add(self.la.a)
        self.point_set.add(self.la.b)
        self.point_set.add(self.lb.a)
        self.point_set.add(self.lb.b)
        self.point_set.add(self.lc.a)
        self.point_set.add(self.lc.b)
        self.point_set.add(self.ld.a)
        self.point_set.add(self.ld.b)

        lis = list(self.point_set)
        lis = [lis[0].get_name(), lis[1].get_name(), lis[2].get_name(), lis[3].get_name()]
        lis.sort()
        self.name = lis[0] + lis[1] + lis[2] + lis[3]

    def get_name(self) -> str: # just for UnionFind
        return self.name

    def __eq__(self, other: object) -> bool:
        if(isinstance(other,Quad)):
            return self.point_set == other.point_set
        else:
            raise Exception("The Type must be Quad")
    
    def __str__(self):
        return 'Quad :{name}'.format(name = self.get_name())

class Relation:
    def __init__(self, type: str, values: List[str]) -> None:
        self.type = type
        self.values = values