from parsec import (spaces, string, regex, generate, many, many1)
from core_expr import (Expr, Var, Lam, App)
from functools import (reduce)

lexeme = lambda p: p << spaces()

lparen = lexeme(string('('))
rparen = lexeme(string(')'))
backslash = lexeme(string('\\'))
arrow = lexeme(string('->'))

symbol = lexeme(regex(r'[_a-zA-Z][_a-zA-Z0-9]*'))

comment = regex(r'--.*')

@generate
def expr():
    e = yield app ^ abs ^ var ^ group
    return e 

@generate
def var():
    v = yield symbol 
    return Var(v)

@generate
def abs():
    yield backslash
    params = yield many1(var)
    yield arrow
    body = yield expr
    
    return reduce(
        lambda b, p: Lam(p, b), 
        reversed(params[:-1]), 
        Lam(params[-1], body)
    )

@generate 
def app():
    e1 = yield abs ^ var ^ group
    e2 = yield abs ^ var ^ group
    es = yield many(abs ^ var ^ group)
    return reduce(
        App,
        es,
        App(e1, e2)
    )

@generate
def group():
    yield lparen
    e = yield expr 
    yield rparen
    return e 

expr_parser = expr

if __name__ == '__main__':
    s = "\\x y -> a (b c)"
    print(expr.parse(s))
