from Lexer import *
from Base import *
from Info import *

class Parser:
    def __init__(self,lex) -> None:
        self.lex = lex
        self.graph_info = None
        self.point_check = dict()
        self.info = Info()
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
        point_list = list()
        line_list = list()
        ponl_list = list()
        while(self.currentToken.type != TokenType.EOF):
            if(self.currentToken.type == TokenType.POINT):
                lis = self.point_define()
                point_list.extend(lis)
                for p in lis:
                    # print(p.name,p.x,p.y)
                    self.point_check[p.name] = 1
            elif(self.currentToken.type == TokenType.LINE):
                lis = self.line_define()
                for l in lis:
                    # print(l.a,l.b)
                    if(l.a in self.point_check and l.b in self.point_check):
                        line_list.append(l)
                    else:
                        name = l.a if l.b in self.point_check else l.b
                        self.notDefine("Point",name)
            elif(self.currentToken.type == TokenType.PONL):
                lis = self.point_on_line()
                ponl_list.extend(lis)
            elif(self.currentToken.type == TokenType.PROF):
                # self.prof()
                print("not ready yet")
            elif(self.currentToken.value in relation_keywords()):
                # rlt = self.relation()
                # print(rlt)
                print("not ready yet")
            else:
                self.error()
        self.graph_info = GraphInfo(point_list,line_list,ponl_list)
    
    def get_graph_info(self) -> GraphInfo:
        return self.graph_info

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

    def point_on_line(self):
        res = []
        self.eat(TokenType.PONL)
        res.append(self.currentToken.value)
        self.eat(TokenType.ID)
        while(self.currentToken.type == TokenType.COMMA):
            self.eat(TokenType.COMMA)
            res.append(self.currentToken.value)
            self.eat(TokenType.ID)
        point_list = res[0:-1]
        line = res[-1]
        return [Ponl(p,line) for p in point_list]

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
        return Relation((tp,lis))

    def prof(self):
        self.eat(TokenType.PROF)
        rlt = self.relation()
        return rlt

