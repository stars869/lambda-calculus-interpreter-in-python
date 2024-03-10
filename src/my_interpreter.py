from my_parser import parseFile, serilizeExpr
from my_reducer import beta_reduce, isNormalForm


if __name__ == "__main__":
    notReducedBindings = parseFile("./test.lambda")
    
    bindings = {}
    
    for (name, expr) in notReducedBindings:
        while not isNormalForm(expr, bindings, set()):
            expr = beta_reduce(expr, bindings, set())
        
        bindings[name] = expr
        
        print(f"{name} = {serilizeExpr(expr)}")
        print()
