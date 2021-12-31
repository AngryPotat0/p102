from os import linesep, name, spawnle, truncate
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
        self.con_line = UnionFind()
        self.equ_lines = UnionFind()
        self.para_lines = UnionFind()
        self.equ_angles = UnionFind()
        self.simtri_list = UnionFind()
        self.contri_list = UnionFind()

        self.eqtri_list = set() #几何对象的名字，之后通过graph_info的find查找具体对象
        self.isotri_list = set() #FIXME:
        self.paral_list = set()
        self.rect_list = set()
        self.rhom_list = set()
        self.squar_list = set()
        self.rang_list = set()
    
    def init_col_lines(self,line_list: LineList) -> None: #FIXME: 第一个愚蠢版本，就先看看效果，记得一定要改
        [self.con_line.add(line) for line in line_list]
        for i in range(0,len(line_list)):
            for j in range(i + 1,len(line_list)):
                line_i, line_j = line_list[i], line_list[j]
                if(line_i.A == line_j.A and line_i.B == line_j.B and line_i.C == line_j.C):
                    self.con_line.union(line_i.get_name(),line_j.get_name())

    def show_union_find(self, union_find: UnionFind, msg="unino_find:") -> None:
        print(msg)
        uf = union_find.get_uf()
        show_case = dict()
        for i in range(0,len(uf)):
            element = uf[i]
            parent = union_find.find(element.data.get_name())
            if(parent in show_case):
                show_case[parent].append(element.data.get_name())
            else:
                show_case[parent] = [element.data.get_name()]
        for k in show_case.keys():
            print("  ->"," ".join(show_case[k]))

    def init_equ_lines(self,line_list: LineList) -> None:
        [self.equ_lines.add(line) for line in line_list]

    def init_para_lines(self) -> None:
        elem_list = self.con_line.get_uf()
        for i in range(0,len(elem_list)):
            elem = elem_list[i]
            if(elem.parent == i): self.para_lines.add(elem.data)

    def init_equ_angles(self) -> List[Angle]: #run this after init_col_lines
        angle_list = list()
        elem_list = self.con_line.get_uf()
        base_line_list = list()
        for i in range(0,len(elem_list)):
            elem = elem_list[i]
            if(elem.parent == i): base_line_list.append(elem.data)
        
        for i in range(0,len(base_line_list)): #FIXME: 平行线问题
            for j in range(i + 1,len(base_line_list)):
                self.equ_angles.add(Angle(base_line_list[i],base_line_list[j]))
                self.equ_angles.add(Angle(base_line_list[j],base_line_list[i]))
                angle_list.append(Angle(base_line_list[i],base_line_list[j]))
                angle_list.append(Angle(base_line_list[j],base_line_list[i]))
        return angle_list
        # print("DEBUG:: angle list:")
        # [print(elem.data.get_name(),end=" ") for elem in self.equ_angles.get_uf()]
        # print()

    def init_triangle(self,triangle_list: List[Triangle]) -> None:
        for triangle in triangle_list:
            self.simtri_list.add(triangle)
            self.contri_list.add(triangle)

class GraphInfo:
    def __init__(self,point_list: list, line_list: list, ponl_list: list) -> None:
        self.info = Info()
        self.point_list = point_list
        self.point_find = dict()
        self.line_list = line_list
        self.line_find = dict()
        self.ponl_list = ponl_list

        self.triangle_list = list()
        self.triangle_find = dict()
        self.quad_list = list()
        self.quad_find = dict()#FIXME: 能不能改成Dict(str,Quad)的形式

        self.gen_lines()
        self.info.init_col_lines(self.line_list)
        self.info.init_equ_lines(self.line_list)
        self.info.init_para_lines()
        self.angle_list = self.info.init_equ_angles()#FIXME:这可实在是太TM丑了
        self.angle_find = dict()

        self.init_find()
        self.gen_graph()
        self.info.init_triangle(self.triangle_list)
        self.init_graph_find()
        # print("Triangle list:")
        # [print(triangle.get_name()) for triangle in self.triangle_list]
    
    def init_find(self):
        for p in self.point_list:
            self.point_find[p.get_name()] = p
        for line in self.line_list:
            # print("line_name_debug::",line)
            self.line_find[line.get_name()] = line
        for angle in self.angle_list:
            self.angle_find[angle.get_name()] = angle
    
    def init_graph_find(self):
        for triangle in self.triangle_list:
            self.triangle_find[triangle.get_name()] = triangle
        for quad in self.quad_list:
            self.quad_find[quad.get_name()] = quad
    
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
            # print("DEBUG:::")
            # print(bl)
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
        def point_on_line(point: Point, line: Line):
            pi,pj = line.a, line.b
            if((point.x-pi.x) * (pj.y-pi.y)==(pj.x-pi.x) * (point.y-pi.y) and min(pi.x,pj.x) <= point.x and point.x <= max(pi.x,pj.x) and min(pi.y,pj.y) <= point.y and point.y <= max(pi.y,pj.y)):
                return True
            return False
        def get_split_lines() -> list: #太慢了，肯定有更好的方式
            line_name_list = list()
            for line in self.line_list:
                flag = 1
                for point in self.point_list:
                    if(point.get_name() == line.a.get_name() or point.get_name() == line.b.get_name()): continue
                    if(point_on_line(point,line)):
                        flag = 0
                        break
                if(flag): line_name_list.append(line.get_name())
            return line_name_list
        line_name_list = get_split_lines()
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
                p = self.info.con_line.find(name)
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
                    graph_line_list.append(self.line_find[lis[0] + lis[1]])
                if(len(line_count) == 3):
                    self.triangle_list.append(Triangle(graph_line_list[0],graph_line_list[1],graph_line_list[2]))
                else:
                    self.quad_list.append(Quad(graph_line_list[0],graph_line_list[1],graph_line_list[2],graph_line_list[3]))

