from os import name, spawnle
from typing import List
from Base import Line

class Element(object):
    def __init__(self, data = None) -> None:
        self.data = data
        self.parent = -1

ElementList = List[Element]
LineList = List[Line]

class UnionFind(object):
    def __init__(self) -> None:
        self.uf = list()
        self.sizes = list()
        self.top = 0
        self.count = 0

    def get_uf(self) -> ElementList:
        return self.uf
    
    def add(self,data) -> int:
        elem = Element(data)
        elem.parent = self.top
        self.uf.append(elem)
        self.sizes.append(1)
        self.top += 1
        self.count += 1
        return self.top - 1

    def connected(self,a,b) -> bool:
        pa = self.find(a)
        pb = self.find(b)
        return pa == pb

    def union(self,a,b) -> None:
        pa = self.find(a)
        pb = self.find(b)
        if(pa == pb): return
        if(self.sizes[pa] > self.sizes[pb]):
            self.uf[pb].parent = pa
            self.sizes[pa] += self.sizes[pb]
        else:
            self.uf[pa].parent = pb
            self.sizes[pb] += self.sizes[pa]

    def find(self,n):
        while(self.uf[n].parent != n):
            self.uf[n].parent = self.uf[self.uf[n].parent].parent
            n = self.uf[n].parent
        return n

class GraphInfo:
    def __init__(self,point_list: list, line_list: list, ponl_list: list) -> None:
        self.point_list = point_list
        self.line_list = line_list
        self.ponl_list = ponl_list
    
    def gen_lines(self):
        point_check = dict()
        for p in self.point_list:
            point_check[p.get_name()] = p
        base_line = dict()
        for ponl in self.ponl_list:
            p = ponl.point.get_name()
            l = ponl.line.get_name()
            if(l in base_line):
                base_line[l].append(p)
            else:
                base_line[l] = [p]

        for bl in base_line.keys():
            lis = base_line[bl]
            lis.insert(0,bl[0])
            lis.append(bl[1])
            for i in range(0,len(lis)):
                for j in range(i + 1,len(lis)):
                    if(i == 0 and j == len(lis) - 1):
                        continue
                    # self.line_list.append(Line(lis[i],lis[j]))
                    self.line_list.append(Line(point_check[lis[i]],point_check[lis[j]]))

class Info:
    def __init__(self) -> None:
        # self.point_list = dict()
        # self.line_list = list()#所有的线
        self.con_line = UnionFind()
        self.con_line_check = dict() #line_name : unionFind_index
        self.eqa_lines = None
        self.eqa_angles = None
        self.para_list = None
        self.simtri_list = None
        self.contri_list = None
        self.col_list = None
    
    def set_col_lines(self,line_list: LineList) -> None:
        for line in line_list:# add line into unionFind
            if(line.get_name() not in self.con_line_check):
                self.con_line_check[line.get_name()] = self.con_line.add(line)
            else:
                raise Exception("Line {name} exists".format(name = line.get_name()))
        #FIXME: 第一个愚蠢版本，就先看看效果，记得一定要改
        for i in range(0,len(line_list)):
            for j in range(i + 1,len(line_list)):
                line_i = line_list[i]
                line_j = line_list[j]
                if(line_i.A == line_j.A and line_i.B == line_j.B and line_i.C == line_j.C):
                    index_i = self.con_line_check[line_i.get_name()]
                    index_j = self.con_line_check[line_j.get_name()]
                    self.con_line.union(index_i,index_j)
    
    def get_col_lines(self) -> None: # Just for Test
        uf = self.con_line.get_uf()
        for i in range(0,len(uf)):
            elem = uf[i]
            if(elem.parent == i):
                print("base Line:{name}".format(name = elem.data.get_name()))
                #Ok, it's extremely stupid
                follow_line_list = list()
                base = i
                base_name = elem.data.get_name()
                for e in uf:
                    name = e.data.get_name()
                    index = self.con_line_check[name]
                    p = self.con_line.find(index)
                    if(p == base and name != base_name):
                        follow_line_list.append(name)
                if(len(follow_line_list) > 0):
                    print("----follow these line:")
                    print("--------" + " ".join(follow_line_list))



