from os import get_terminal_size
from Info import *
from Token import *
from Lexer import *
from Parser import *
from Infer import *

text = ""
file = open('program.txt')
while(True):
    line = file.readline()
    text += line
    if(not line):
        break
file.close()

lex = Lexer(text)
par = Parser(lex)
par.parse()
graph = par.get_graph_info()
infer = par.get_infer()
infer.set_info(graph)
infer.init_before_run()

# graph.info.show_col_lines()
# graph.info.show_union_find(graph.info.con_line)
graph.info.show_union_find(graph.info.para_lines, "para_lines:")
graph.info.show_union_find(graph.info.equ_angles, "equ_angles:")
# graph.info.show_union_find(graph.info.equ_lines,"equ_lines:")
# graph.info.show_union_find(graph.info.contri_list,"contri_list:")
# graph.info.show_union_find(graph.info.simtri_list, "simtri_list:")
# graph.info.show_union_find(graph.info.para_lines,"para_lines:")
# for k in graph.angle_find.keys():
#     print(k,graph.angle_find[k])

# info = par.get_info()

# graph.gen_lines()
# for p in graph.point_list:
#     print(p)

# for ponl in graph.ponl_list:
#     print(ponl)

# for l in graph.line_list:
#     print(l)

# graph.info.get_col_lines()
# for triangle in graph.triangle_list:
#     print(triangle)
# for quad in graph.quad_list:
#     print(quad)

# for triangle in graph.triangle_list:
#     print(triangle)
#     print("angles:")
#     for k in triangle.angle_dict.keys():
#         print("    {name}: {l}".format(name=k,l=triangle.angle_dict[k].get_name()))

# for relation in infer.relations:
#     print(relation)

# print("target:")

# for target in infer.targets:
#     print(target)
