import re
import ply.lex as lex

tokens = [
    'COMENTARIOMULTI',
    'COMENTARIOLINHA',
    'VARIAVEL',
    'TIPO',
    'MAIN',
    'OPERADORES',
    'OPERADORESLOGICOS',
    'LISTA',
    'ARRAY',
    'FUNC',
    'NUM'
]
def t_MAIN(t):
    r'program\s\w+'
    return t
literals = '{;}(),[].'

t_ignore =' \t'

t_COMENTARIOMULTI = r'\/\*(?:[^(\*\/)]+)\*\/'
def t_COMENTARIOLINHA(t): 
    r'\/\/.+'
    return t
def t_FUNC(t):
    r'print|fact|while|for|\bin\b|if'
    return t
t_OPERADORES=r'\*|\-|\+|\/'
t_OPERADORESLOGICOS= r'\=|\<|\>' 
t_NUM= r'\d+'
t_LISTA=   r'\[\d+\.\.\d+\]'
t_ARRAY=   r'\{(?:\d+,?)*\}'

def t_TIPO(t):
    r'int|float|char|double'
    return t
def t_VARIAVEL(t):
    r'[_a-zA-Z]\w*'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()

data="""/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/
int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};
// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}"""

lexer.input(data)

while True:
    tok = lexer.token()
    print(tok)
    if not tok: 
        break      # No more input
    

lexer.token()
