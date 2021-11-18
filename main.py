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


lex = Lexer(text)
par = Parser(lex)
par.parse()

# lis = relation_keywords()
# print(lis)