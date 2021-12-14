from Lexer import *
from Base import *
from Info import *
from Infer import *

class Parser:
    def __init__(self,lex) -> None:
        self.lex = lex
        self.graph_info = None
        self.infer = Infer()
        self.point_check = dict()
        self.line_check = dict()
        # self.info = Info()
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

    def errorMsg(self,msg):
        raise Exception(msg)

    def parse(self):
        point_list = list()
        line_list = list()
        ponl_list = list()
        while(self.currentToken.type != TokenType.EOF):
            if(self.currentToken.type == TokenType.POINT):
                lis = self.point_define()
                point_list.extend(lis)
                for p in lis:
                    self.point_check[p.name] = p
            elif(self.currentToken.type == TokenType.LINE):
                lis = self.line_define()
                for l in lis:
                    if(len(l) > 2):
                        self.errorMsg("Line Define Error, length of name must less then 2")
                    elif(l[0] in self.point_check and l[1] in self.point_check):
                        line_list.append(Line(self.point_check[l[0]],self.point_check[l[1]]))
                        self.line_check[l[0] + l[1]] = self.line_check[l[1] + l[0]] = Line(self.point_check[l[0]],self.point_check[l[1]])
                    else:
                        name = l[0] if l[1] in self.point_check else l[1]
                        self.notDefine("Point",name)
            elif(self.currentToken.type == TokenType.PONL):
                lis = self.point_on_line()
                points = lis[0:-1]
                line = lis[-1]
                for p in points:
                    ponl_list.append(Ponl(self.point_check[p],self.line_check[line]))
            elif(self.currentToken.type == TokenType.PROF):
                relation = self.prof()
                self.infer.targets.append(relation)
            elif(self.currentToken.value in relation_keywords()):
                relation = self.relation()
                self.infer.relations.append(relation)
                # print("not ready yet")
            else:
                self.error()
        self.graph_info = GraphInfo(point_list,line_list,ponl_list)
    
    def get_graph_info(self) -> GraphInfo:
        return self.graph_info

    def get_infer(self) -> Infer:
        return self.infer

    # def get_info(self) -> Info:
    #     return self.info

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
        res.append(name)
        while(self.currentToken.type == TokenType.COMMA):
            self.eat(TokenType.COMMA)
            name = self.currentToken.value
            self.eat(TokenType.ID)
            res.append(name)
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
        return Relation(tp,lis)

    def prof(self):
        self.eat(TokenType.PROF)
        rlt = self.relation()
        return rlt

