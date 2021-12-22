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
    PONL =              'ponl'
    EQA =               'eqa'
    CONG =              'cong'
    PARA =              'para'
    PERP =              'perp'
    MIDP =              'midp'
    SIMTRI =            'simtri'
    CONTRI =            'contri'
    COL =               'col'
    LCOP =              'lcop'
    RANG =              'rang'
    EQTRI =             'eqtri'
    ISOTRI =            'isotri'
    PARAL =             'paral'
    RECT =              'rect'
    RHOM =              'rhom'
    SQUR =              'squr'
    PROVE =             'prove'
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
    end = token_list.index(TokenType.PROVE)
    relation_keywords = [
        token_type.value
        for token_type in token_list[start:end]
    ]
    return relation_keywords
