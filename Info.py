from os import linesep, name, spawnle
from typing import List, Union
from Base import*
from UnionFInd import*

def find_graph(lis: list) -> list[str]:
    circs_list = list()

    def find_circs_starts_with(G,length,path):
        l, last = len(path), path[-1]
        cnt = 0
        if (l == length - 1):
            for i in G[last]:
                if ((i > path[1]) and (i not in path) and (path[0] in G[i])):
                    # print(path + [i])
                    ret = path + [i]
                    circs_list.append(ret[:])
                    cnt += 1
        else:
            for i in G[last]:
                if(i > path[0] and i not in path):
                    cnt += find_circs_starts_with(G,length, path + [i])
        return cnt

    def find_cirs_of_length(G,n,length):
        cnt = 0
        for i in range(1,n - length + 2):
            cnt += find_circs_starts_with(G,length,[i])
        return cnt

    def find_all_cirs(G,n):
        cnt = 0
        for i in range(3,n + 1):
            cnt += find_cirs_of_length(G,n,i)
        return cnt

    # find_all_cirs(G,5)

    # lis = list()
    # n = int(input())
    # for i in range(0,n):
    #     lis.append(input())

    line_map = dict()
    for line in lis:
        start = ord(line[0]) - ord('a') + 1
        dist = ord(line[1]) - ord('a') + 1
        if(start in line_map):
            line_map[start].add(dist)
        else:
            line_map[start] = {dist}
        if(dist in line_map):
            line_map[dist].add(start)
        else:
            line_map[dist] = {start}

    # print(line_map,len(line_map))
    find_all_cirs(line_map,len(line_map))
    # print(circs_list)

    graph_list = [[] for i in range(0,len(circs_list))]

    for i in range(0,len(graph_list)):
        for j in range(0,len(circs_list[i])):
            graph_list[i].append(chr(circs_list[i][j] + ord('a') - 1))

    return graph_list


class Info:
    def __init__(self) -> None:
        # self.point_list = dict()
        # self.line_list = list()#所有的线
        self.con_line = UnionFind()
        self.con_line_check = dict() #line_name : unionFind_index
        self.eqa_lines = UnionFind()
        self.para_lines = UnionFind()
        self.eqa_angles = None
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

class GraphInfo:
    def __init__(self,point_list: list, line_list: list, ponl_list: list) -> None:
        self.info = Info()
        self.point_list = point_list
        self.point_find = dict()
        self.line_list = line_list
        self.line_find = dict()
        self.ponl_list = ponl_list

        self.triangle_list = list()
        self.quad_list = list()

        self.gen_lines()
        self.info.set_col_lines(self.line_list)
        self.init_find()
        self.gen_graph()
    
    def init_find(self):
        for p in self.point_list:
            self.point_find[p.get_name()] = p
        for line in self.line_list:
            # print("line_name_debug::",line)
            self.line_find[line.get_name()] = line
    
    def gen_lines(self) -> None:
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
    
    def gen_graph(self) -> None:#run after gen_line
        line_filter = set()
        line_name_list = list()
        for ponl in self.ponl_list:
            line_name = ponl.line.get_name()
            line_filter.add(line_name)
        for line in self.line_list:
            line_name = line.get_name()
            if(line_name in line_filter):
                continue
            else:
                line_name_list.append(line_name)
        # print("++++++++++++++++++++++++++++++++++")
        # print(line_name_list)
        # print("++++++++++++++++++++++++++++++++++")
        graph_list = find_graph(line_name_list)
        # print("gen_graph+++++++++++++++++++++++++++++++++++++")
        # print(graph_list)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++")
        self.set_graph(graph_list)

    def set_graph(self,graph_list) -> None:
        def find_end_point(lis:list) -> list:
            # print("DEBUG::find_end_point:",lis)
            if(len(lis) == 1):
                return [lis[0][0],lis[0][1]]
            ret = list()
            point_count = dict()
            line = "".join(lis)
            for p in line:
                if(p in point_count):
                    point_count[p] += 1
                else:
                    point_count[p] = 1
            for k in line:
                if(point_count[k] == 1):
                    ret.append(k)
            return ret

        for graph in graph_list:
            # print("**GRAPH debug:",graph)
            line_count = dict()
            for i in range(0,len(graph)):
                lis = [graph[i],graph[(i+1) % len(graph)]]
                lis.sort()
                name = lis[0] + lis[1]
                p = self.info.con_line.find(self.info.con_line_check[name])
                if(p in line_count):
                    line_count[p].append(name)
                else:
                    line_count[p] = [name]

            if(len(line_count) <= 4):
                graph_line_list = list()
                for k in line_count.keys():
                    lis = find_end_point(line_count[k])
                    if(len(lis) != 2):#FIXME: WHY???
                        raise Exception("find_end_point Error,lis={a}".format(a = lis))
                    lis.sort()
                    # line_name = lis[0] + lis[1]
                    graph_line_list.append(self.line_find[lis[0] + lis[1]])
                if(len(line_count) == 3):
                    self.triangle_list.append(Triangle(graph_line_list[0],graph_line_list[1],graph_line_list[2]))
                else:
                    self.quad_list.append(Quad(graph_line_list[0],graph_line_list[1],graph_line_list[2],graph_line_list[3]))

