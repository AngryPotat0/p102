from _typeshed import Self
from typing import List
from Base import *
from Info import *

class Infer:
    def __init__(self) -> None:
        self.relations = list()
        self.targets = list()
        self.new_relations = list()
        self.graph_info = None

    def set_info(self,graph_info: GraphInfo) -> None:
        self.graph_info = graph_info