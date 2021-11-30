from Base import Line


class Element(object):
    def __init__(self) -> None:
        self.data = None
        self.parent = -1

class UnionFind(object):
    def __init__(self) -> None:
        self.uf = list()
        self.sizes = list()
        self.top = 0
        self.count = 0
    
    def add(self,elem: Element) -> int:
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
        base_line = dict()
        for ponl in self.ponl_list:
            p = ponl.point
            l = ponl.line
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
                    self.line_list.append(Line(lis[i],lis[j]))

class Info:
    def __init__(self) -> None:
        # self.point_list = dict()
        # self.line_list = list()#所有的线
        self.con_line = UnionFind()
        self.eqa_lines = UnionFind()
        self.eqa_angles = UnionFind()
        self.para_list = UnionFind()
        self.simtri_list = UnionFind()
        self.contri_list = UnionFind()
        self.col_list = UnionFind()

