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
                    

    def run(self):
        pass