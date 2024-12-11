binome Loubari chaima Boukari massilia

from ply import lex, yacc


tokens = (
    "STARTUML", "ENDUML", "COLON", "RIGHT_ARROW_1", "RIGHT_ARROW_2", "ACTOR", "ID", "AS", "USECASE", "STRING",
    "PACKAGE", "LBRACE", "RBRACE", "INHERIT", "STEREO", "INCLUDES", "EXTENDS", "ACTOR_TXT", "USE_CASE_TXT", "EOL"
)

reserved = {
    "actor": "ACTOR",
    "as": "AS",
    "usecase": "USECASE",
    "package": "PACKAGE",
    "includes": "INCLUDES",
    "extends": "EXTENDS"
}

t_STARTUML = r"@startuml"
t_ENDUML = r"@enduml"
t_COLON = r":"
t_RIGHT_ARROW_1 = r"-+>"
t_RIGHT_ARROW_2 = r"\\.+>"
t_LBRACE = r"\\{"
t_RBRACE = r"\\}"
t_INHERIT = r"<\\|--"
t_EOL = r"\\n"

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_STEREO(t):
    r"<< [a-zA-Z_][a-zA-Z_0-9]* >>"
    t.value = t.value[3:-3]
    return t

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in reserved.keys():
        t.type = reserved[t.value]
    return t

def t_ACTOR_TXT(t):
    r":[^ :\\n][^\\n:]*:"
    t.value = t.value[1:-1]
    return t

def t_USE_CASE_TXT(t):
    r"\\([^ \\\(\\n][^\\n:]*\\)"
    t.value = t.value[1:-1]
    return t

t_ignore = " \t"

def t_error(t):
    raise ValueError(f"Unexpected symbol {t.value[0]}")

def t_newline(t):
    r"\\n+"
    t.lexer.lineno += len(t.value)

lexer = lex.lex()

def p_start(p):
    '''start : STARTUML ID defs ENDUML
             | STARTUML defs ENDUML'''
    if len(p) == 5:  # With diagram name
        p[0] = {'type': 'diagram', 'name': p[2], 'definitions': p[3]}
    else:  # Without diagram name
        p[0] = {'type': 'diagram', 'name': None, 'definitions': p[2]}

def p_defs(p):
    '''defs : defs def
            | def'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_def_actor(p):
    '''def : ACTOR ACTOR_TXT
           | ACTOR ACTOR_TXT AS ID
           | ACTOR ACTOR_TXT STEREO'''
    if len(p) == 3:
        p[0] = {'type': 'actor', 'name': p[2], 'alias': None, 'stereotype': None}
    elif len(p) == 5:
        p[0] = {'type': 'actor', 'name': p[2], 'alias': p[4], 'stereotype': None}
    else:
        p[0] = {'type': 'actor', 'name': p[2], 'alias': None, 'stereotype': p[3]}

def p_def_usecase(p):
    '''def : USECASE USE_CASE_TXT
           | USECASE USE_CASE_TXT AS ID'''
    if len(p) == 3:
        p[0] = {'type': 'usecase', 'text': p[2], 'alias': None}
    else:
        p[0] = {'type': 'usecase', 'text': p[2], 'alias': p[4]}

def p_def_relation(p):
    '''def : ID RIGHT_ARROW_1 ID
           | ID INHERIT ID
           | ID COLON INCLUDES ID
           | ID COLON EXTENDS ID'''
    if len(p) == 4:
        p[0] = {'type': 'relation', 'from': p[1], 'to': p[3], 'relation_type': p[2]}
    else:
        p[0] = {'type': 'relation', 'from': p[1], 'to': p[4], 'relation_type': p[3]}

def p_def_package(p):
    'def : PACKAGE ID LBRACE defs RBRACE'
    p[0] = {'type': 'package', 'name': p[2], 'definitions': p[4]}

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error near '{p.value}'")
    else:
        print("Syntax error at end of file")

parser = yacc.yacc()

if __name__ == "__main__":
    data = '''
    @startuml
    actor :Admin:
    usecase (Login) as UC1
    :Admin: --> (Login)
    package SubSystem {
        actor :User:
        usecase (Register)
        :User: --> (Register)
    }
    @enduml
    '''

    result = parser.parse(data)
    print(result)
