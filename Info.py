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

class Info:
    def __init__(self) -> None:
        self.point_list = dict()
        self.line_list = dict()
        self.eqa_lines = UnionFind()
        self.eqa_angles = UnionFind()
        self.para_list = UnionFind()
        self.simtri_list = UnionFind()
        self.contri_list = UnionFind()
        self.col_list = UnionFind()

