from enum import Enum
class TokenType(Enum):
    LPAREN =            '('
    RPAREN =            ')'
    COMMA =             ','
    INTEGER_CONST =     'INTEGER_CONST'
    REAL_CONST =        'REAL_CONST'
    ID =                'ID'
    POINT =             'point'
    LINE =              'line'
    EQA =               'eqa'
    CONG =              'cong'
    EQR =               'eqr'
    PARA =              'para'
    PERP =              'perp'
    MIDP =              'midp'
    SIMTRI =            'simtri'
    CONTRI =            'contri'
    CYC =               'cyc'
    COL =               'col'
    LCOP =              'lcop'
    CCOP =              'ccop'
    PONL =              'ponl'
    PONC =              'ponc'
    RANG =              'rang'
    EQTRI =             'eqtri'
    ISOTRI =            'isotri'
    TRAP =              'trap'
    ISOTRAP =           'isotrap'
    RTRAP =             'rtrap'
    PARAL =             'paral'
    RECT =              'rect'
    RHOM =              'rhom'
    SQUR =              'squr'
    PROF =              'prof'
    EOF =               'EOF'

class Token():
    def __init__(self, type,value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return 'Token type:{type},value:{value}'.format(type=self.type, value=self.value)

def reserved_keywords():
    token_list = list(TokenType)
    start = token_list.index(TokenType.POINT)
    end = token_list.index(TokenType.EOF)
    reserved_keywords = {
        token_type.value : token_type
        for token_type in token_list[start:end]
    }
    return reserved_keywords

def relation_keywords():
    token_list = list(TokenType)
    start = token_list.index(TokenType.EQA)
    end = token_list.index(TokenType.PROF)
    relation_keywords = [
        token_type.value
        for token_type in token_list[start:end]
    ]
    return relation_keywords
