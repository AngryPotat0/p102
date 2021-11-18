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
    def __init__(self,a,b,c) -> None:
        self.a = a
        self.b = b
        self.c = c

class Quad:
    def __init__(self,a,b,c,d) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d