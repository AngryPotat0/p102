class Point:
    def __init__(self,name,x,y) -> None:
        self.name = name
        self.x = x
        self.y = y

class Line:
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b

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