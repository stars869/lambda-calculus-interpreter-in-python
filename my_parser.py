import typing as t
from itertools import chain
from dataclasses import dataclass
from parser_combinator.parser_combinator import Parser, charPredPG, oneCharPG, stringPG


def sepBlocks(s: str) -> list[str]:
    lines = s.split('\n')
    blocks = []
    currentBlock = []

    for line in lines:
        if not line:
            continue
        if not line[0].isspace():
            blocks.append("".join(currentBlock))
            currentBlock = [line,]
        else:
            currentBlock.append(line)

    blocks.append("".join(currentBlock))

    blocks = list(filter(lambda x: x, blocks))
    blocks = list(filter(lambda x: not x.isspace(), blocks))

    return blocks

def sepBinding(s: str) -> t.Tuple[str, str]:
    result = s.split('=')
    assert(len(result) == 2)

    varname = result[0].strip() 
    expr = result[1].strip()
    assert(varname != "")
    assert(expr != "")

    return (varname, expr)

class Expr: pass 

@dataclass
class Variable(Expr): 
    value: str 

    def __hash__(self) -> int:
        return hash(self.value)
    
@dataclass
class Abstraction(Expr): 
    params: list[Variable]
    body: Expr 

    def __init__(self, value: t.Tuple[list[Variable], Expr]):
        self.params = value[0]
        self.body = value[1]

@dataclass
class Application(Expr): 
    exprs: list[Expr]

def parseExpr(s: str) -> Expr:
    alphabetP = charPredPG(lambda c: c.isalpha())
    wsP = charPredPG(lambda c: c.isspace()) ** 0
    lambdaSignP = wsP >> oneCharPG("\\") << wsP 
    arrowSignP = wsP >> stringPG("->") << wsP
    variableP = (wsP >> alphabetP ** 1 << wsP) ^ (lambda xs: Variable("".join(xs)))
    paranLP = wsP >> oneCharPG("(") << wsP
    paranRP = wsP >> oneCharPG(")") << wsP
    abstractionLazyP = lambda: ((lambdaSignP >> variableP ** 1 << arrowSignP) + lambdaExprLazyP) ^ Abstraction
    applicationLazyP = lambda: (((paranLP >> lambdaExprLazyP << paranRP) | abstractionLazyP | variableP) ** 2) ^ Application
    lambdaExprLazyP = lambda: applicationLazyP() | (paranLP >> lambdaExprLazyP << paranRP) | abstractionLazyP | variableP

    (expr, rest) = lambdaExprLazyP().parse(s)
    assert(rest == "")
    return expr

def parseFile(path: str) -> list[t.Tuple[str, Expr]]:
    file = open(path, "r")
    code = file.read()
    file.close()

    blocks = sepBlocks(code)

    bindings = []
    for block in blocks:
        (varname, exprCode) = sepBinding(block)
        expr = parseExpr(exprCode)
        bindings.append((varname, expr))
    return bindings


def serilizeExpr(expr: Expr) -> str:
    if isinstance(expr, Variable):
        return expr.value
    
    elif isinstance(expr, Abstraction):
        paramsS = " ".join(map(lambda v: v.value, expr.params))
        bodyS = serilizeExpr(expr.body)
        return f"\\{paramsS} -> {bodyS}"
    
    elif isinstance(expr, Application):
        exprsSList = []
        for e in expr.exprs:
            eS = serilizeExpr(e)
            if not isinstance(e, Variable):
                eS = '(' + eS + ')'
            exprsSList.append(eS)
        return " ".join(exprsSList)


if __name__ == "__main__":
    for (b, e) in parseFile("./test.lambda"):
        print(b)
        print(e)
        print()