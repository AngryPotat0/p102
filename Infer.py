from enum import Flag
from typing import List
from Base import *
from Info import *

graph_list = {
            "rect": "矩形",
            "paral": "平行四边形",
            "squr": "正方形"
        }

class Infer:
    def __init__(self) -> None:
        self.relations = list()
        self.targets = list()
        self.new_relations = list()
        self.graph_info = None

    def init_before_run(self) -> None:
        self.prepare_angle(self.relations)
        self.prepare_angle(self.targets)
        # self.set_relation(self.relations)

    def set_info(self,graph_info: GraphInfo) -> None:
        self.graph_info = graph_info

    def prepare_angle(self, relatino_list: List[Relation]):
        for relation in relatino_list:
            if(relation.type in ('rang', 'eqa')):
                new_values = list()
                for angle in relation.values:
                    point_a = self.graph_info.point_find[angle[0]]
                    point_b = self.graph_info.point_find[angle[1]]
                    point_c = self.graph_info.point_find[angle[2]]
                    angle = gen_angle_for_angle([point_a,point_b,point_c])
                    base_line_a = self.graph_info.info.con_line.find_base(angle.la.get_name()).data
                    base_line_b = self.graph_info.info.con_line.find_base(angle.lb.get_name()).data
                    new_values.append(Angle(base_line_a,base_line_b).get_name())
                relation.values = new_values
                    
    def set_relation(self, relation_list: List[Relation]) -> None:
        for relation in relation_list:
            relation_type = relation.type
            if(relation_type == 'eqtri'): #添加等边三角形，设置三条边相等，三个角相等
                for triangle_name in relation.values: 
                    triangle = self.graph_info.triangle_find[triangle_name]
                    self.graph_info.info.eqtri_list.add(triangle_name)#等边三角形加入set
                    # self.new_relations.append(Relation('cong',[triangle.la.get_name(),triangle.lb.get_name(),triangle.lc.get_name()]))
                    self.add_new_relations(Relation('cong',[triangle.la.get_name(),triangle.lb.get_name(),triangle.lc.get_name()]))
                    angle_list = [triangle.angle_dict[name] for name in triangle.angle_dict.keys()]
                    base_angle_list = list()
                    for angle in angle_list:
                        line_a, line_b = angle.la, angle.lb
                        base_line_a = self.graph_info.info.con_line.find_base(line_a.get_name()).data
                        base_line_b = self.graph_info.info.con_line.find_base(line_b.get_name()).data
                        base_angle_list.append(Angle(base_line_a, base_angle_b).get_name())
                    # self.new_relations.append(Relation('eqa',base_angle_list))
                    self.add_new_relations(Relation('eqa',base_angle_list))
            elif(relation_type == 'paral'):#平行四边形 对边平行且相等 对角相等  要不要加入特殊图形集合来着？
                for paral_name in relation.values:
                    paral = self.graph_info.quad_find[paral_name]
                    self.graph_info.info.paral_list.add(paral_name) #平行四边形加入特殊图形集合
                    check_set = set()
                    for k in paral.other_line:
                        line_a, line_b = k, paral.other_line[k]
                        if(line_a in check_set): continue
                        # self.new_relations.append(Relation('cong',[line_a, line_b]))
                        self.add_new_relations(Relation('cong',[line_a, line_b]))
                        # self.new_relations.append(Relation('para',[line_a, line_b]))
                        self.add_new_relations(Relation('para',[line_a, line_b]))
                        check_set.add(line_a)
                        check_set.add(line_b)
                        #TODO: 对角相等
            elif(relation_type == 'rect'):#矩形，对边平行且相等，四个角为直角
                for rect_name in relation.values:
                    rect = self.graph_info.quad_find[rect_name]
                    self.graph_info.info.rect_list.add(rect_name)
                    check_set = set()
                    for k in rect.other_line:
                        line_a, line_b = k, rect.other_line[k]
                        if(line_a in check_set): continue
                        # self.new_relations.append(Relation('cong', [line_a, line_b]))
                        self.add_new_relations(Relation('cong', [line_a, line_b]))
                        # self.new_relations.append(Relation('para', [line_a, line_b]))
                        self.add_new_relations(Relation('para', [line_a, line_b]))
                        check_set.add(line_a)
                        check_set.add(line_b)
                    #TODO: 直角
                    base_angle_list = list()
                    for k in rect.angle_dict:
                        angle = rect.angle_dict[k]
                        base_line_a = self.graph_info.info.con_line.find_base(rect.angle_dict[k].la.get_name()).data
                        base_line_b = self.graph_info.info.con_line.find_base(rect.angle_dict[k].lb.get_name()).data
                        base_angle_list.append(Angle(base_line_a, base_line_b).get_name())
                    # self.new_relations.append(Relation('rang',base_angle_list))
                    self.add_new_relations(Relation('rang',base_angle_list))
            elif(relation_type == 'rhom'): #菱形   我看谁用这个条件！！！
                pass
            elif(relation_type == 'squr'): #正方形，对边平行，四边相等，四个角为直角
                for squr_name in relation.values:
                    squr = self.graph_info.quad_find[squr_name]
                    self.graph_info.info.squar_list.add(squr_name)
                    check_set = set()
                    for k in squr.other_line:
                        line_a, line_b = k, squr.other_line[k]
                        # self.graph_info.info.para_lines.union(line_a, line_b)
                        if(line_a in check_set): continue
                        # self.new_relations.append(Relation('para',[line_a, line_b]))
                        self.add_new_relations(Relation('para',[line_a, line_b]))
                        check_set.add(line_a)
                        check_set.add(line_b)
                    # self.new_relations.append(Relation('cong',squr.la.get_name(),squr.lb.get_name(),squr.lc.get_name(),squr.ld.get_name()))
                    self.add_new_relations(Relation('cong',[squr.la.get_name(),squr.lb.get_name(),squr.lc.get_name(),squr.ld.get_name()]))
                    #TODO: 四角为直角
                    base_angle_list = list()
                    for k in squr.angle_dict:
                        angle = squr.angle_dict[k]
                        base_line_a = self.graph_info.info.con_line.find_base(squr.angle_dict[k].la.get_name()).data
                        base_line_b = self.graph_info.info.con_line.find_base(squr.angle_dict[k].lb.get_name()).data
                        base_angle_list.append(Angle(base_line_a, base_line_b).get_name())
                    # self.new_relations.append(Relation('rang',base_angle_list))
                    self.add_new_relations(Relation('rang',base_angle_list))
            elif(relation_type == 'rang'):#直角，设置角和它的反角相等
                for angle_name in relation.values:
                    angle = self.graph_info.angle_find[angle_name]
                    reversed_angle = Angle(angle.lb, angle.la)
                    self.graph_info.info.equ_angles.union(angle_name,reversed_angle.get_name())
                    self.graph_info.info.rang_list.add(angle_name)
                    self.graph_info.info.rang_list.add(reversed_angle.get_name())# 加入特殊图形集合
            elif(relation_type == 'eqa'):#等角，列表中的角相等
                for i in range(0,len(relation.values) - 1):
                    angle_a_name = relation.values[i]
                    angle_b_name = relation.values[i + 1]
                    self.graph_info.info.equ_angles.union(angle_a_name, angle_b_name)
            elif(relation_type == 'cong'): #等长，列表中的线相等
                for i in range(0,len(relation.values) - 1):
                    line_a_name = relation.values[i]
                    line_b_name = relation.values[i + 1]
                    self.graph_info.info.equ_lines.union(line_a_name, line_b_name)
            elif(relation_type == 'para'): #平行，列表中的线互相平行  平行线相关角相等   三线平行？
                para_line_list = set()
                for i in range(0,len(relation.values) - 1):
                    base_line_a = self.graph_info.info.con_line.find_base(relation.values[i]).data  #找出基准线
                    base_line_b = self.graph_info.info.con_line.find_base(relation.values[i + 1]).data
                    para_line_list.add(base_line_a)
                    para_line_list.add(base_line_b)
                    self.graph_info.info.para_lines.union(base_line_a.get_name(), base_line_b.get_name())
                #平行后设置角相等,干脆把其他所有线都加进去算了，反正平行的那些也没关系
                cross_line_list = list()
                uf = self.graph_info.info.con_line.get_uf()
                # print("Scan::")
                # print("DEBUG::para::")
                for i in range(0,len(uf)):
                    element = uf[i]
                    if(element.parent != i): continue
                    # print(element.data.get_name(),end=" ")
                    line = element.data
                    if(line in para_line_list): continue
                    cross_line_list.append(line)
                # print("sp")
                # [print(line.get_name(),end=" ") for line in cross_line_list]
                # print("END DEBUG")
                for cross_line in cross_line_list:
                    angle_list_a = list()
                    angle_list_b = list()
                    for para_line in para_line_list:
                        angle_list_a.append(Angle(cross_line,para_line).get_name())
                        angle_list_b.append(Angle(para_line,cross_line).get_name())
                    for i in range(0,len(angle_list_a) - 1):
                        # self.new_relations.append(Relation('eqa',angle_list_a))
                        self.add_new_relations(Relation('eqa',angle_list_a))
                        # self.new_relations.append(Relation('eqa',angle_list_b))
                        self.add_new_relations(Relation('eqa',angle_list_b))
                    
            elif(relation_type == 'simtri'): #相似，列表中的三角形互相相似，添加角相等, 问题:相似的三角形中存在特殊三角形怎么办
                #方法：在关系列表中，三角形名字为相似/全等序，我们生成角相等和线相等等信息，然后以字母序存储相似/全等情况
                for i in range(0,len(relation.values) - 1):
                    triangle_name_a = relation.values[i]
                    triangle_name_b = relation.values[i + 1]
                    name_a = sorted([triangle_name_a[0], triangle_name_a[1], triangle_name_a[2]])
                    name_a = "".join(name_a)
                    name_b = sorted([triangle_name_b[0], triangle_name_b[1], triangle_name_b[2]])
                    name_b = "".join(name_b)
                    triangle_a = self.graph_info.triangle_find[name_a]
                    triangle_b = self.graph_info.triangle_find[name_b]
                    #设置相似时使用基本名
                    self.graph_info.info.simtri_list.union(triangle_a.get_name(), triangle_b.get_name())
                    triangle_a.simtri_name = triangle_name_a
                    triangle_b.simtri_name = triangle_name_b
                    for i in range(0,3):#角相等信息，三角形名字长度为3
                        angle_a = triangle_a.angle_dict[triangle_name_a[i]]
                        angle_b = triangle_b.angle_dict[triangle_name_b[i]]
                        angle_a_base_la = self.graph_info.info.con_line.find_base(angle_a.la.get_name()).data
                        angle_a_base_lb = self.graph_info.info.con_line.find_base(angle_a.lb.get_name()).data
                        angle_b_base_la = self.graph_info.info.con_line.find_base(angle_b.la.get_name()).data
                        angle_b_base_lb = self.graph_info.info.con_line.find_base(angle_b.lb.get_name()).data
                        base_angle_a = Angle(angle_a_base_la,angle_a_base_lb)
                        base_angle_b = Angle(angle_b_base_la,angle_b_base_lb)
                        # self.new_relations.append(Relation('eqa',[base_angle_a.get_name(), base_angle_b.get_name()]))
                        self.add_new_relations(Relation('eqa',[base_angle_a.get_name(), base_angle_b.get_name()]))
            elif(relation_type == 'contri'): #全等，列表中的三角形互相全等，设置角相等和线相等 问题: 全等的三角形中存在特殊三角形怎么办
                for i in range(0,len(relation.values) - 1):
                    triangle_name_a = relation.values[i]
                    triangle_name_b = relation.values[i + 1]
                    name_a = "".join(sorted([triangle_name_a[0], triangle_name_a[1], triangle_name_a[2]]))
                    name_b = "".join(sorted([triangle_name_b[0], triangle_name_b[1], triangle_name_b[2]]))
                    triangle_a = self.graph_info.triangle_find[name_a]
                    triangle_b = self.graph_info.triangle_find[name_b]
                    for i in range(0,3):
                        #设置等角
                        angle_a = triangle_a.angle_dict[triangle_name_a[i]]
                        angle_b = triangle_b.angle_dict[triangle_name_b[i]]
                        angle_a_base_la = self.graph_info.info.con_line.find_base(angle_a.la.get_name()).data
                        angle_a_base_lb = self.graph_info.info.con_line.find_base(angle_a.lb.get_name()).data
                        angle_b_base_la = self.graph_info.info.con_line.find_base(angle_b.la.get_name()).data
                        angle_b_base_lb = self.graph_info.info.con_line.find_base(angle_b.lb.get_name()).data
                        base_angle_a = Angle(angle_a_base_la,angle_a_base_lb)
                        base_angle_b = Angle(angle_b_base_la,angle_b_base_lb)
                        # self.new_relations.append(Relation('eqa',[base_angle_a.get_name(), base_angle_b.get_name()]))
                        self.add_new_relations(Relation('eqa',[base_angle_a.get_name(), base_angle_b.get_name()]))
                        #设置等长
                        line_a_name = "".join(sorted([triangle_name_a[i], triangle_name_a[(i + 1) % 3]]))
                        line_b_name = "".join(sorted([triangle_name_b[i], triangle_name_b[(i + 1) % 3]]))
                        # self.graph_info.info.equ_lines.union(line_a_name,line_b_name)
                        # self.new_relations.append(Relation('cong',[line_a_name,line_b_name]))
                        self.add_new_relations(Relation('cong',[line_a_name,line_b_name]))
                    #设置全等关系时使用基本名
                    self.graph_info.info.contri_list.union(name_a, name_b)
                    triangle_a.contri_name = triangle_name_a
                    triangle_b.contri_name = triangle_name_b
            elif(relation_type == 'perp'):#垂直，元素1垂直于元素2    直角：从直角集中选出一个角，设置这两个角相等 本角加入直角集
                line_a = self.graph_info.info.con_line.find_base(relation.values[0]).data
                line_b = self.graph_info.info.con_line.find_base(relation.values[1]).data
                self.graph_info.info.equ_angles.union(Angle(line_a,line_b).get_name(),Angle(line_b,line_a).get_name)
            elif(relation_type == 'midp'): #中点，设置线相等 问题： 中点连成中线，与三角形底边平行
                point_name = relation.values[0]
                line_name = relation.values[1]
                line_a_lis = [line_name[0], point_name]
                line_b_lis = [line_name[1], point_name]
                line_a_lis.sort()
                line_b_lis.sort()
                line_a = line_a_lis[0] + line_a_lis[1]
                line_b = line_b_lis[0] + line_b_lis[1]
                self.graph_info.info.equ_lines.union(line_a, line_b)

    def check_relation(self, target_list: List[Relation]) -> None:
        ans = True
        for relation in target_list:
            relation_type = relation.type
            if(relation_type == 'eqtri'):
                for triangle_name in relation.values:
                    if(triangle_name not in self.graph_info.info.eqtri_list):
                        ans = False
            elif(relation_type == 'paral'):
                for quad_name in relation.values:
                    if(quad_name not in self.graph_info.info.paral_list):
                        ans = False
            elif(relation_type == 'rect'):
                for quad_name in relation.values:
                    if(quad_name not in self.graph_info.info.rect_list):
                        ans = False
            elif(relation_type == 'rhom'):
                pass
            elif(relation_type == 'squr'):
                for quad_name in relation.values:
                    if(quad_name not in self.graph_info.info.squar_list):
                        ans = False
            elif(relation_type == 'rang'):
                for angle_name in relation.values:
                    if(angle_name not in self.graph_info.info.rang_list):
                        ans = False
            elif(relation_type == 'eqa'): # 等角
                for i in range(0,len(relation.values) - 1):
                    angle_name_a = relation.values[i]
                    angle_name_b = relation.values[i + 1]
                    ans = self.graph_info.info.equ_angles.connected(angle_name_a,angle_name_b)
            elif(relation_type == 'cong'):# 等长
                for i in range(0,len(relation.values) - 1):
                    line_name_a = relation.values[i]
                    line_name_b = relation.values[i + 1]
                    ans = self.graph_info.info.equ_lines.connected(line_name_a, line_name_b)
            elif(relation_type == 'para'):# 平行
                for i in range(0,len(relation.values) - 1):
                    line_a_name = self.graph_info.info.con_line.find_base(relation.values[i]).data.get_name()
                    line_b_name = self.graph_info.info.con_line.find_base(relation.values[i + 1]).data.get_name()
                    ans = self.graph_info.info.para_lines.connected(line_a_name,line_b_name)
            elif(relation_type == 'simtri'):
                for i in range(0,len(relation.values) - 1):
                    triangle_name_a = "".join(sorted([relation.values[i][0],relation.values[i][1],relation.values[i][2]]))
                    triangle_name_b = "".join(sorted([relation.values[i + 1][0],relation.values[i + 1][1],relation.values[i + 1][2]]))
                    ans = self.graph_info.info.simtri_list.connected(triangle_name_a,triangle_name_b)
            elif(relation_type == 'contri'):
                for i in range(0,len(relation.values) - 1):
                    triangle_name_a = relation.values[i]
                    triangle_name_b = relation.values[i + 1]
                    name_a = "".join(sorted([triangle_name_a[0], triangle_name_a[1], triangle_name_a[2]]))
                    name_b = "".join(sorted([triangle_name_b[0], triangle_name_b[1], triangle_name_b[2]]))
                    ans = self.graph_info.info.contri_list.connected(name_a,name_b)
        return ans


    def run(self):
        flag = True
        count = 0
        # print("开始运行")
        status = "1"
        msg = ""
        while True:
            if(count > 10): break
            # print("第{v}步:".format(v=count))
            msg += "第{v}步:\n".format(v=count)
            msg += self.show_relations(self.relations)
            self.set_relation(self.relations)
            self.gen_relation()
            ans = self.check_relation(self.targets)
            # print("ANS::",ans)
            if(ans):
                # print("证明成功")
                msg += "证明成功\n"
                flag = False
                break
            count += 1
            if(len(self.new_relations) == 0): break
            self.relations = self.new_relations
            self.new_relations = []
        if(flag):
            msg += "证明失败\n"
            status = "0"
        return {'status':status,'msg':msg}
        # return msg
        

    def show_relations(self,relation_list: List[Relation]):
        ans = ""
        for relation in relation_list:
            relation_type = relation.type
            if(relation_type == 'cong' or relation_type == 'eqa'):
                ans += "=".join(relation.values)
            elif(relation_type == 'para'):
                ans += " // ".join(relation.values)
            elif(relation_type == 'contri'):
                triangle_list = ['▲' + name for name in relation.values]
                ans += " ≌  ".join(triangle_list)
                # ans += "Triangle " + ",".join(relation.values) + " is congruent triangles"
            elif(relation_type == 'simtri'):
                triangle_list = ['▲' + name for name in relation.values]
                ans += " ~  ".join(triangle_list)
                # ans += "Triangle " + ",".join(relation.values) + " is similar triangles"
            elif(relation_type == 'rang'):
                ans += '{lis} is right angle'.format(lis=",".join(relation.values))
            elif(relation_type == 'eqtri'):
                ans += '{lis} is equilateral triangle'.format(lis=",".join(relation.values))
            elif(relation_type in graph_list):
                lis = ",".join(relation.values)
                ans += "{a} is {t}".format(a=lis,t=graph_list[relation_type])
            else:
                ans += relation
            ans += '\n'
        return ans

    def add_new_relations(self, relation: Relation): #防止添加重复条件
        if(self.check_relation([relation])):
            return
        self.new_relations.append(relation)

    def gen_relation(self) -> None:
        for quad in self.graph_info.quad_list:
            if(self.is_squr(quad)):
                self.add_new_relations(Relation('squr',[quad.get_name()]))
            elif(self.is_rect(quad)):
                self.add_new_relations(Relation('rect',[quad.get_name()]))
            elif(self.is_paral(quad)):
                self.add_new_relations(Relation('paral',[quad.get_name()]))
        for i in range(0,len(self.graph_info.triangle_list)):
            for j in range(i + 1,len(self.graph_info.triangle_list)):
                triangle_a = self.graph_info.triangle_list[i]
                triangle_b = self.graph_info.triangle_list[j]
                lis = self.is_contri(triangle_a, triangle_b)
                if(lis != None): self.add_new_relations(Relation('contri', lis))
                lis = self.is_simtri(triangle_a, triangle_b)
                if(lis != None): self.add_new_relations(Relation('simtri', lis))

    def is_squr(self, quad: Quad) -> bool:
        # 有一组邻边相等且一个角是直角的平行四边形是正方形.
        # 有一组邻边相等的矩形是正方形.
        return False
        if(quad.get_name() in self.graph_info.info.squar_list): return False
        la, lb, lc, ld = quad.la, quad.lb, quad.lc, quad.ld
        ret = False
        ret = (self.graph_info.info.equ_lines.connected(la.get_name(),lb.get_name())
                    and self.graph_info.info.equ_lines.connected(lb.get_name(),lc.get_name())
                    and self.graph_info.info.equ_lines.connected(lc.get_name(),ld.get_name())
                )
        if(ret == False): return ret

    
    def is_paral(self, quad: Quad) -> bool:
        if(quad.get_name() in self.graph_info.info.paral_list): return False
        #一组对边平行，相等
        for k in quad.other_line.keys():
            line_a, line_b = k,quad.other_line[k]
            base_line_a, base_line_b = self.graph_info.info.con_line.find_base(line_a).data.get_name(),self.graph_info.info.con_line.find_base(line_b).data.get_name()
            if(self.graph_info.info.para_lines.connected(base_line_a, base_line_b) and self.graph_info.info.equ_lines.connected(base_line_a, base_line_b)):
                return True
        #两组对边平行
        flag = True
        for k in quad.other_line.keys():
            line_a, line_b = k,quad.other_line[k]
            base_line_a, base_line_b = self.graph_info.info.con_line.find_base(line_a).data.get_name(),self.graph_info.info.con_line.find_base(line_b).data.get_name()
            if(not self.graph_info.info.para_lines.connected(base_line_a, base_line_b)):
                flag = False
                break
        if(flag): return True
        #两组对边相等
        flag = True
        for k in quad.other_line.keys():
            line_a, line_b = k,quad.other_line[k]
            base_line_a, base_line_b = self.graph_info.info.con_line.find_base(line_a).data.get_name(),self.graph_info.info.con_line.find_base(line_b).data.get_name()
            if(not self.graph_info.info.equ_lines.connected(base_line_a, base_line_b)):
                flag = False
                break
        if(flag): return True
        #两组对角相等 pass
        return False
    
    def is_rect(self, quad: Quad) -> bool:
        if(not self.is_paral(quad)): return False
        for k in quad.angle_dict.keys():
            angle = quad.angle_dict[k]
            if(angle.get_name() in self.graph_info.info.rang_list):
                return True
        return False

    def is_eqtri(self, triangle: Triangle) -> bool:
        la,lb,lc = triangle.la.get_name(), triangle.lb.get_name(), triangle.lc.get_name()
        if(self.graph_info.info.equ_lines.connected(la,lb) and self.graph_info.info.equ_lines.connected(lb,lc)):
            return True
        angle_list = []
        for k in triangle.angle_dict.keys():
            angle = triangle.angle_dict[k]
            base_line_a = self.graph_info.info.con_line.find_base(angle.la.get_name()).data
            base_line_b = self.graph_info.info.con_line.find_base(angle.lb.get_name()).data
            angle_list.append(Angle(base_line_a,base_line_b).get_name())
        angle_a, angle_b, angle_c = angle_list[0],angle_list[1],angle_list[2]
        if(self.graph_info.info.equ_angles.connected(angle_a,angle_b) and self.graph_info.info.equ_angles.connected(angle_b,angle_c)):
            return True
        return False

    def is_contri(self, triangle_a: Triangle, triangle_b: Triangle) -> list:
        #ASA
        def find_con_line_for_angles(angle_a: Angle, angle_b: Angle) -> Line:
            line_list = [angle_a.la, angle_a.lb, angle_b.la, angle_b.lb]
            line_filter = set()
            for line in line_list:
                if(line not in line_filter):
                    line_filter.add(line)
                else:
                    return line
            return None
        def point_find(triangle: Triangle, point_a: str, point_b: str) -> str:
            point_list = {point_a,point_b}
            for k in triangle.angle_dict.keys():
                if k not in point_list: return k
            return None #不可能出现这种情况

        angle_filter = set()
        angle_list_a = list()
        angle_list_b = list()
        for k in triangle_a.angle_dict.keys():
            angle_a = triangle_a.angle_dict[k]
            for t in triangle_b.angle_dict.keys():
                angle_b = triangle_b.angle_dict[t]
                if(t in angle_filter): continue
                base_angle_a = Angle(self.graph_info.info.con_line.find_base(angle_a.la.get_name()).data,self.graph_info.info.con_line.find_base(angle_a.lb.get_name()).data).get_name()
                base_angle_b = Angle(self.graph_info.info.con_line.find_base(angle_b.la.get_name()).data,self.graph_info.info.con_line.find_base(angle_b.lb.get_name()).data).get_name()
                if(self.graph_info.info.equ_angles.connected(base_angle_a,base_angle_b)):
                    angle_filter.add(t)
                    angle_list_a.append(k)
                    angle_list_b.append(t)
                    break
        if(len(angle_list_a) == 2):
            i = 0
            point_l_a, point_r_a = angle_list_a[i], angle_list_a[(i + 1) % 3]
            angle_l, angle_r = triangle_a.angle_dict[point_l_a], triangle_a.angle_dict[point_r_a]
            con_line_a = find_con_line_for_angles(angle_l, angle_r)
            point_l_b, point_r_b = angle_list_b[i], angle_list_b[(i + 1) % 3]
            angle_l, angle_r = triangle_b.angle_dict[point_l_b], triangle_b.angle_dict[point_r_b]
            con_line_b = find_con_line_for_angles(angle_l, angle_r)
            if(self.graph_info.info.equ_lines.connected(con_line_a.get_name(), con_line_b.get_name())):
                contri_name_a = point_l_a + point_r_a + point_find(triangle_a,point_l_a, point_r_a)
                contri_name_b = point_l_b + point_r_b + point_find(triangle_b,point_l_b, point_r_b)
                return [contri_name_a, contri_name_b]
        if(len(angle_list_a) == 3):
            for i in range(0,3):
                point_l_a, point_r_a = angle_list_a[i], angle_list_a[(i + 1) % 3]
                angle_l, angle_r = triangle_a.angle_dict[point_l_a], triangle_a.angle_dict[point_r_a]
                con_line_a = find_con_line_for_angles(angle_l, angle_r)
                point_l_b, point_r_b = angle_list_b[i], angle_list_b[(i + 1) % 3]
                angle_l, angle_r = triangle_b.angle_dict[point_l_b], triangle_b.angle_dict[point_r_b]
                con_line_b = find_con_line_for_angles(angle_l, angle_r)
                if(self.graph_info.info.equ_lines.connected(con_line_a.get_name(), con_line_b.get_name())):
                    contri_name_a = point_l_a + point_r_a + point_find(triangle_a,point_l_a, point_r_a)
                    contri_name_b = point_l_b + point_r_b + point_find(triangle_b,point_l_b, point_r_b)
                    return [contri_name_a, contri_name_b]
        return None

    def is_simtri(self, triangle_a: Triangle, triangle_b: Triangle) -> list:
        # print("####Triangle:",triangle_a.get_name(),triangle_b.get_name())
        def point_find(triangle: Triangle, point_a: str, point_b: str) -> str:
            point_list = {point_a,point_b}
            for k in triangle.angle_dict.keys():
                if k not in point_list: return k
            return None #不可能出现这种情况
        #AAA
        angle_filter = set()
        angle_list_a = list()
        angle_list_b = list()
        for k in triangle_a.angle_dict.keys():
            angle_a = triangle_a.angle_dict[k]
            for t in triangle_b.angle_dict.keys():
                angle_b = triangle_b.angle_dict[t]
                if(t in angle_filter): continue
                base_angle_a = Angle(self.graph_info.info.con_line.find_base(angle_a.la.get_name()).data,self.graph_info.info.con_line.find_base(angle_a.lb.get_name()).data).get_name()
                base_angle_b = Angle(self.graph_info.info.con_line.find_base(angle_b.la.get_name()).data,self.graph_info.info.con_line.find_base(angle_b.lb.get_name()).data).get_name()
                if(self.graph_info.info.equ_angles.connected(base_angle_a,base_angle_b)):
                    # print("#####append::",k,t)
                    angle_filter.add(t)
                    angle_list_a.append(k)
                    angle_list_b.append(t)
                    break
        if(len(angle_list_a) == 2):
            simtri_name_a = angle_list_a[0] + angle_list_a[1] + point_find(triangle_a,angle_list_a[0],angle_list_a[1])
            simtri_name_b = angle_list_b[0] + angle_list_b[1] + point_find(triangle_b,angle_list_b[0],angle_list_b[1])
            # print("####SIMTRI 2::",[simtri_name_a, simtri_name_b])
            return [simtri_name_a, simtri_name_b]
        if(len(angle_list_a) == 3):
            simtri_name_a = angle_list_a[0] + angle_list_a[1] + angle_list_a[2]
            simtri_name_b = angle_list_b[0] + angle_list_b[1] + angle_list_b[2]
            # print("####SIMTRI 3::",[simtri_name_a, simtri_name_b])
            return [simtri_name_a, simtri_name_b]
        return None