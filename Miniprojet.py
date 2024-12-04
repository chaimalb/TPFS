#Binome : Loubari Chaima et Boukari Massilia 
import ply.lex as lex

tokens = [
    'STARTUML', 'ENDUML', 'ACTOR', 'USECASE', 'PACKAGE', 'AS', 'INHERIT', 'STEREO', 'ID', 'RIGHT_ARROW_1', 'RIGHT_ARROW_2', 'LBRACE', 'RBRACE', 'COLON', 'STRING'
]

t_ignore = ' \t'

def t_STARTUML(t):
    r'@startuml'
    return t
 
def t_ENDUML(t):
    r'@enduml'
    return t

def t_ACTOR(t):
    r'actor'
    return t

def t_USECASE(t):
    r'usecase'
    return t

def t_PACKAGE(t):
    r'package'
    return t

def t_AS(t):
    r'as'
    return t

def t_INHERIT(t):
    r'<\|--'
    return t

def t_RIGHT_ARROW_1(t):
    r'-->'
    return t

def t_RIGHT_ARROW_2(t):
    r'\.>'
    return t

def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACE(t):
    r'\}'
    return t

def t_COLON(t):
    r':'
    return t

def t_STRING(t):
    r'\".*?\"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
