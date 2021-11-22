from Info import *
from Token import *
from Lexer import *
from Parser import *

def start(command):
    pass

text = ""
file = open('program.txt')
while(True):
    line = file.readline()
    text += line
    if(not line):
        break
file.close()

info = Info()

lex = Lexer(text)
par = Parser(lex,info)
par.parse()
print("Info:")
for p in info.point_list:
    print(info.point_list[p].name)

# lis = relation_keywords()
# print(lis)