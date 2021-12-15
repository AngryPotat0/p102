from os import name, spawnle
from typing import List, Union
from Base import*

class Element(object):
    def __init__(self, data = None) -> None:
        self.data = data
        self.parent = -1

ElementList = List[Element]
LineList = List[Line]

class UnionFind(object):
    def __init__(self) -> None:
        self.uf = list()
        self.uf_find = dict() #name : index
        self.sizes = list()
        self.top = 0
        self.count = 0

    def get_uf(self) -> ElementList:
        return self.uf
    
    def add(self,data) -> None:
        elem = Element(data)
        elem.parent = self.top
        self.uf.append(elem)
        self.sizes.append(1)
        self.top += 1
        self.count += 1
        # return self.top - 1
        self.uf_find[data.get_name()] = self.top - 1

    def connected(self,a_name: str,b_name: str) -> bool:
        pa = self.find(a_name)
        pb = self.find(b_name)
        return pa == pb

    def union(self,a_name: str,b_name: str) -> None:
        pa = self.find(a_name)
        pb = self.find(b_name)
        if(pa == pb): return
        if(self.sizes[pa] > self.sizes[pb]):
            self.uf[pb].parent = pa
            self.sizes[pa] += self.sizes[pb]
        else:
            self.uf[pa].parent = pb
            self.sizes[pb] += self.sizes[pa]

    def find(self,name: str) -> int:
        n = self.uf_find[name]
        while(self.uf[n].parent != n):
            self.uf[n].parent = self.uf[self.uf[n].parent].parent
            n = self.uf[n].parent
        return n
    
    def find_base(self, name: str) -> Element:
        p = self.find(name)
        return self.uf[p]