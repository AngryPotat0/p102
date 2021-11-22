from Lexer import *
from Base import *
from Info import *

class Parser:
    def __init__(self,lex,info) -> None:
        self.lex = lex
        self.info = info
        self.currentToken = lex.get_next_token()

    def eat(self,expect_type):
        # print(self.currentToken)
        if(self.currentToken.type != expect_type):
            self.error()
        self.currentToken = self.lex.get_next_token()
    
    def error(self):
        raise Exception('Unexpected Token{token}'.format(token = self.currentToken))
    
    def notDefine(self,gtype,name):
        raise Exception('Not define {gt} {nm}'.format(gt = gtype,nm = name))

    def parse(self):
        while(self.currentToken.type != TokenType.EOF):
            if(self.currentToken.type == TokenType.POINT):
                lis = self.point_define()
                for p in lis:
                    print(p.name,p.x,p.y)
                    self.info.point_list[p.name] = p
            elif(self.currentToken.type == TokenType.LINE):
                lis = self.line_define()
                for l in lis:
                    print(l.a,l.b)
                    if(l.a in self.info.point_list and l.b in self.info.point_list):
                        self.info.line_list[l.a + l.b] = l
                        self.info.line_list[l.b + l.a] = l
                    else:
                        name = l.a if l.b in self.info.point_list else l.b
                        self.notDefine("Point",name)
            elif(self.currentToken.type == TokenType.PROF):
                self.prof()
            elif(self.currentToken.value in relation_keywords()):
                rlt = self.relation()
                print(rlt)
            else:
                self.error()

    def point(self):
        name = self.currentToken.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        x = self.currentToken.value
        self.eat(TokenType.INTEGER_CONST)
        self.eat(TokenType.COMMA)
        y = self.currentToken.value
        self.eat(TokenType.INTEGER_CONST)
        self.eat(TokenType.RPAREN)
        return (name,x,y)

    def point_define(self):
        res = []
        self.eat(TokenType.POINT)
        pt = self.point()
        res.append(Point(pt[0],pt[1],pt[2]))
        while(self.currentToken.type == TokenType.COMMA):
            self.eat(TokenType.COMMA)
            pt = self.point()
            res.append(Point(pt[0],pt[1],pt[2]))
        return res

    def line_define(self):
        res = []
        self.eat(TokenType.LINE)
        name = self.currentToken.value
        self.eat(TokenType.ID)
        res.append(Line(name[0],name[1]))
        while(self.currentToken.type == TokenType.COMMA):
            self.eat(TokenType.COMMA)
            name = self.currentToken.value
            self.eat(TokenType.ID)
            res.append(Line(name[0],name[1]))
        return res

    def relation(self):
        lis = []
        tp = self.currentToken.type
        self.eat(self.currentToken.type)
        name = self.currentToken.value
        self.eat(TokenType.ID)
        lis.append(name)
        while(self.currentToken.type == TokenType.COMMA):
            self.eat(TokenType.COMMA)
            name = self.currentToken.value
            self.eat(TokenType.ID)
            lis.append(name)
        return (tp,lis)

    def prof(self):
        self.eat(TokenType.PROF)
        rlt = self.relation()
        return rlt

