from Info import *
from Token import *
from Lexer import *
from Parser import *
from Infer import *

class Runner:
    def run(self, text: str):
        lex = Lexer(text)
        par = Parser(lex)
        par.parse()
        graph = par.get_graph_info()
        infer = par.get_infer()
        infer.set_info(graph)
        infer.init_before_run()
        ret = infer.run()
        return ret