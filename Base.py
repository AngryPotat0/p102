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

def gen_angle_for_angle(point_list: List[Point]) -> Angle:
    a = 2 * (point_list[1].x - point_list[0].x)
    b = 2 * (point_list[1].y - point_list[0].y)
    c = point_list[1].x * point_list[1].x + point_list[1].y * point_list[1].y - point_list[0].x * point_list[0].x - point_list[0].y * point_list[0].y
    d = 2 * (point_list[2].x - point_list[1].x)
    e = 2 * (point_list[2].y - point_list[1].y)
    f = point_list[2].x * point_list[2].x + point_list[2].y * point_list[2].y - point_list[1].x * point_list[1].x - point_list[1].y * point_list[1].y
    x = (b * f - e * c) / (b * d - e * a)
    y = (d * c - a * f) / (b * d - e * a)
    R = math.sqrt((x - point_list[0].x) ** 2 + (y - point_list[0].y) ** 2)

    return gen_angle(point_list[0],point_list[2],point_list[1],x,y,R)

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
        self.angle_dict = gen_angle_for_triangle(list(self.point_set)) #name: Angle
        # self.base_angle_dict = dict()
        # self.init_base_angle_dict()#FIXME: 这东西放哪里好一点呢？

        self.simtri_name = ""
        self.contri_name = ""
    
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

        self.other_line = dict() #line_name : line_name   改名叫face_line之类的挺不错的，但是不想动了
        self.init_other_line()

        self.angle_dict = dict()
        self.init_angle_dict()

    def init_other_line(self):
        def no_same_point(la: Line, lb: Line) -> bool:
            point_set = set()
            point_set.add(la.a.get_name())
            point_set.add(la.b.get_name())
            point_set.add(lb.a.get_name())
            point_set.add(lb.b.get_name())
            return len(point_set) == 4
        line_list = [self.la, self.lb, self.lc, self.ld]
        for i in range(0,len(line_list)):
            for j in range(i + 1,len(line_list)):
                if(line_list[i].get_name() in self.other_line): continue
                # print("with line: {a} and line: {b}".format(a=line_list[i].get_name(),b=line_list[j].get_name()))
                if(no_same_point(line_list[i],line_list[j])):
                    # print("YES")
                    self.other_line[line_list[i].get_name()] = line_list[j].get_name()
                    self.other_line[line_list[j].get_name()] = line_list[i].get_name()
        # only for debug:
        # print("init_other_line for Quad {name}".format(name = self.name))
        # for k in self.other_line:
        #     print(k,self.other_line[k])

    def init_angle_dict(self):
        def get_angle(line_a: Line, line_b: Line) -> Tuple[Point]:
            side_point = set()
            mid_point = list()
            for point in [line_a.a,line_a.b,line_b.a,line_b.b]:
                if(point not in side_point):
                    side_point.add(point)
                else:
                    mid_point.append(point)
                    side_point.remove(point)
            if(len(mid_point) != 0):
                side_point = list(side_point)
                return (side_point[0],mid_point[0],side_point[1])
            return None
        line_list = [self.la,self.lb,self.lc,self.ld]
        for i in range(0,len(line_list)):
            for j in range(i + 1,len(line_list)):
                point_tuple = get_angle(line_list[i],line_list[j])
                if(point_tuple == None or point_tuple[1].get_name() in self.angle_dict): continue
                self.angle_dict[point_tuple[1].get_name()] = gen_angle_for_angle(list(point_tuple))
        #debug:
        # print("Quad {name} angle_dict:".format(name=self.name))
        # for k in self.angle_dict.keys():
        #     print(k,self.angle_dict[k].get_name())


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

    def __str__(self) -> str:
        lis = ""
        for value in self.values:
            lis = lis + value + " "
        return "{t} with {lis}".format(t=self.type,lis=lis)