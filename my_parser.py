import typing as t
from dataclasses import dataclass
from parser_combinator.parser_combinator import Parser, charPredPG, oneCharPG, stringPG


@dataclass
class Expr:
    # variable, abstraction, application
    value: t.Union[str, t.Tuple, list] 

class Variable(Expr): pass 

class Abstraction(Expr): pass

class Application(Expr): pass

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

if __name__ == "__main__":
    lambda_code = open("./test.lambda", "r").read()
    print(lambdaExprLazyP().parse(lambda_code))