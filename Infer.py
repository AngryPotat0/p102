from typing import List
from Base import *
from Info import *

class Infer:
    def __init__(self) -> None:
        self.relations = list()
        self.targets = list()
        self.new_relations = list()
        self.graph_info = None

    def init_before_run(self) -> None:
        self.prepare_angle(self.relations)
        self.prepare_angle(self.targets)
        self.set_relation(self.relations)

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
                    self.graph_info.info.equ_lines.union(triangle.la.get_name(), triangle.lb.get_name())# 设置三边相等
                    self.graph_info.info.equ_lines.union(triangle.lc.get_name(), triangle.lb.get_name())
                    angle_list = [triangle.angle_dict[name] for name in triangle.angle_dict.keys()]
                    self.graph_info.info.equ_angles.union(angle_list[0].get_name(), angle_list[1].get_name())
                    self.graph_info.info.equ_angles.union(angle_list[2].get_name(), angle_list[1].get_name())
            elif(relation_type == 'paral'):#平行四边形 对边平行且相等 对角相等  要不要加入特殊图形集合来着？
                for paral_name in relation.values:
                    paral = self.graph_info.quad_find[paral_name]
                    for k in paral.other_line:
                        line_a, line_b = k, paral.other_line[k]
                        self.graph_info.info.equ_lines.union(line_a, line_b)
                        self.graph_info.info.para_lines.union(line_a, line_b)
                        #TODO: 对角相等
            elif(relation_type == 'rect'):#长方形，对边平行且相等，四个角为直角
                for rect_name in relation.values:
                    rect = self.graph_info.quad_find[rect_name]
                    for k in rect.other_line:
                        line_a, line_b = k, paral.other_line[k]
                        self.graph_info.info.equ_lines.union(line_a, line_b)
                        self.graph_info.info.para_lines.union(line_a, line_b)
                        #TODO: 直角
            elif(relation_type == 'rhom'): #菱形   我看谁用这个条件！！！
                pass
            elif(relation_type == 'squr'): #正方形，对边平行，四边相等，四个角为直角
                for squr_name in relation.values:
                    squr = self.graph_info.quad_find[squr_name]
                    for k in squr.other_line:
                        line_a, line_b = k, squr.other_line[k]
                        self.graph_info.info.para_lines.union(line_a, line_b)
                    self.graph_info.info.equ_lines.union(squr.la.get_name(), squr.lb.get_name())
                    self.graph_info.info.equ_lines.union(squr.lb.get_name(), squr.lc.get_name())
                    self.graph_info.info.equ_lines.union(squr.lc.get_name(), squr.ld.get_name())
                    self.graph_info.info.equ_lines.union(squr.la.get_name(), squr.ld.get_name())
                    #TODO: 四角为直角，特殊图形集合？
            elif(relation_type == 'rang'):#直角，设置角和它的反角相等
                for angle_name in relation.values:
                    angle = self.graph_info.angle_find[angle_name]
                    reversed_angle = Angle(angle.la, angle.lb)
                    self.graph_info.info.equ_angles.union(angle, reversed_angle)
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
                for i in range(0,len(relation.values) - 1):
                    base_line_a_name = self.graph_info.info.con_line.find_base(relation.values[i]).data.get_name()  #找出基准线
                    base_line_b_name = self.graph_info.info.con_line.find_base(relation.values[i + 1]).data.get_name()
                    self.graph_info.info.para_lines.union(base_line_a_name, base_line_b_name)
            elif(relation_type == 'simtri'): #相似，列表中的三角形互相相似，添加角相等, 问题:相似的三角形中存在特殊三角形怎么办
                pass
            elif(relation_type == 'contri'): #全等，列表中的三角形互相全等，设置角相等和线相等 问题: 全等的三角形中存在特殊三角形怎么办
                pass
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


    def run(self):
        pass