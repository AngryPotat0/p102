from Info import *
from Token import *
from Lexer import *
from Parser import *

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
# info = par.get_info()

# graph.gen_lines()
for p in graph.point_list:
    print(p)

for ponl in graph.ponl_list:
    print(ponl)

for l in graph.line_list:
    print(l)

graph.info.get_col_lines()
for triangle in graph.triangle_list:
    print(triangle)
for quad in graph.quad_list:
    print(quad)

for triangle in graph.triangle_list:
    print(triangle)
    print("angles:")
    for k in triangle.angle_dict.keys():
        print("    {name}: {l}".format(name=k,l=triangle.angle_dict[k].get_name()))
