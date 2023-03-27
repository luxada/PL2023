import ply.lex as lex
import re

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# ------------------------------------------------------------

# Global state variables
saldo = 0
state = 0 # 0 -> pousado, 1 -> levantado, -1 -> abortar (termina de imediato o programa)

# List of token names.   This is always required
tokens = (
   'LEVANTAR',
   'POUSAR',
   'MOEDA',
   'NUMERO',
   'ABORTAR',
)

# Token specification
t_LEVANTAR = r'LEVANTAR'
t_POUSAR = r'POUSAR'
t_ABORTAR = r'ABORTAR'

def t_MOEDA(t):
    r'MOEDA\s+((\d+(?:c|e)(?:,|\.)\s*)+)'
    # t.value vai ficar com o valor da string com as várias moedas inseridas
    t.value = re.match(r'MOEDA\s+((\d+(?:c|e)(?:,|\.)\s*)+)', t.value).group(1)
    return t

def t_NUMERO(t):
    r'T\s*=\s*(00\d+|\d{9})\s*'
    t.value = re.match(r'T\s*=\s*(00\d+|\d{9})\s*', t.value).group(1)
    return t


# Ignore whitespaces
def t_whitespace(t):
    r'\s+'
    pass

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Função auxiliar que calcula o saldo em forma de string 
def calculaSaldo():
    global saldo

    euros = str(int(saldo/100))
    cents = str(saldo)[-2:]
    return euros+"e"+cents+"c"

# Exemplo: moedas = 10c, 30c, 50c, 2e.
def trataMoedas(moedas):    
    global saldo
    valoresValidos = ['10c', '20c', '50c', '1e', '2e']

    valores = re.findall(r'(\d+(?:c|e))', moedas)
    for val in valores:
        if val in valoresValidos:
            mon = val[-1:]
            val = val[:-1] # Tira o c ou e
            if mon == 'c': # Cêntimos
                saldo += int(val) 
            else: # Euros
                saldo += int(val) * 100
        else:
            print("maq: " + val + " - moeda inválida")

    print("maq: saldo = " + calculaSaldo())


def trataNumero(numero):    
    global saldo

    if numero[:3] == "601" or numero[:3] == "641": # Chamada bloqueada
        print("maq: Desculpe, mas esse número está bloqueado neste telefone! Tente um novo número.")
    elif numero[:2] == "00": # É uma chamada internacional
        if saldo < 150:
            print("maq: Desculpe, mas não tem o saldo necessário para realizar esta chamada.")
            print("maq: Chamadas internacionais custam 1e50c.")
        else:
            saldo -= 150
            print("maq: saldo = " + calculaSaldo())
    elif numero[:1] == "2": # Chamada nacional
        if saldo < 25:
            print("maq: Desculpe, mas não tem o saldo necessário para realizar esta chamada.")
            print("maq: Chamadas nacionais custam 25c.")
        else:
            saldo -= 25
            print("maq: saldo = " + calculaSaldo()) 
    elif numero[:3] == "800": # Chamada verde
        print("maq: saldo = " + calculaSaldo()) 
    elif numero[:3] == "808": # Chamada azul
        if saldo < 10:
            print("maq: Desculpe, mas não tem o saldo necessário para realizar esta chamada.")
            print("maq: Chamadas azuis custam 10c.")
        else:
            saldo -= 10
            print("maq: saldo = " + calculaSaldo()) 

# Função principal que faz o parse de cada token
def parseToken(token):
    global state

    if token.type == 'LEVANTAR':
        if state == 0: # Telefone está pousado
            print("maq: Introduza moedas.")
            state = 1 # Telefone passa a estar levantado
        else: # O telefone já está levantado
            print("maq: O telefone já está levantado...")
    elif token.type == 'POUSAR':
        if state == 1:
            state = 0
            saldo = calculaSaldo()
            print("maq: troco=" + saldo + "; Volte sempre!")
        else:
            print("maq: Telefone já está pousado. Sem mais informações para dispor.")
    elif token.type == 'ABORTAR':
        state = 2
    elif token.type == 'MOEDA':
        if state == 1:
            trataMoedas(token.value)
        else:
            print("maq: O telefone está pousado, não posso aceitar moedas neste estado.")
    elif token.type == 'NUMERO':
        if state == 1:
            trataNumero(token.value)
        else:
            print("maq: O telefone está pousado, não posso aceitar um número neste estado.")

# Build the lexer
lexer = lex.lex()

while(True):
    inp = input(">> ")
    lexer.input(inp)
    for token in lexer:
        parseToken(token)
        
    if state == 2: # Estado de abortar
            break