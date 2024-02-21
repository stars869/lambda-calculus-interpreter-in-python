from my_parser import Expr, Variable, Abstraction, Application


class ReducerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def alpha_convert(expr: Expr, oldVar: Variable, newVar: Variable):
    if isinstance(expr, Variable):
        if expr == oldVar:
            expr = newVar

    elif isinstance(expr, Abstraction):
        if oldVar in expr.params:
            return 
        else:
            alpha_convert(expr.body, oldVar, newVar)

    elif isinstance(expr, Application):
        for e in expr.exprs:
            alpha_convert(e, oldVar, newVar)

    else:
        raise ReducerError("unexpected case")

def isNormalForm(expr: Expr, bindings: dict[str, Expr], bounds: set[Variable]) -> bool:
    if isinstance(expr, Variable):
        if expr in bounds:
            return True
        elif expr.value in bindings:
            return False 
        else:
            raise ReducerError(f"Unknown variable: {expr}")
    
    elif isinstance(expr, Abstraction):
        newBounds = bounds.copy()
        newBounds = newBounds.union(expr.params)
        return isNormalForm(expr.body, bindings, newBounds)
    
    elif isinstance(expr, Application):
        if all(map(lambda e: isNormalForm(e, bindings, bounds), expr.exprs)):
            if isinstance(expr.exprs[0], Abstraction):
                return False 
            else:
                return True
        else:
            return False 

    else:
        raise ReducerError("Unexpeced expr type")

def beta_reduce(expr: Expr, bindings: dict[str, Expr], bounds: set[Variable]) -> Expr:
    if isinstance(expr, Variable):
        if expr.value in bindings and expr not in bounds:
            return bindings[expr.value]
        else:
            return expr 

    elif isinstance(expr, Abstraction):
        # for alpha conversion
        # update bounds
        newParams = []
        for p in expr.params:
            if p in bounds:
                newp = Variable(p.value + "'")
                alpha_convert(expr.body, p, newp)
                newParams.append(newp)
            else:
                newParams.append(p)
        bounds = bounds.union(newParams)

        newBody = beta_reduce(expr.body, bindings, bounds)

        # update bounds
        for p in newParams:
            if p in bounds: 
                bounds.remove(p)
        
        return Abstraction((newParams, newBody))

    elif isinstance(expr, Application):
        newExprs = list(map(lambda e: beta_reduce(e, bindings, bounds), expr.exprs))
        first_expr = newExprs[0]

        for i in range(1, len(newExprs)):
            if isinstance(first_expr, Variable) or isinstance(first_expr, Application):
                return Application([first_expr] + newExprs[i:])
            else:
                assert(isinstance(first_expr, Abstraction))
                newBody = substitute(first_expr.body, first_expr.params[0], expr.exprs[i])
                newParams = first_expr.params[1:]
                
                if len(newParams) > 0:
                    first_expr = Abstraction((newParams, newBody))
                else:
                    first_expr = newBody
                
        # first_expr maybe a new Application, may need to continue beta_reduce, 
        return first_expr

    else:
        raise ReducerError("unexpected case")

def substitute(expr: Expr, targetVar: Variable, replacement: Expr) -> Expr:
    if isinstance(expr, Variable):
        if expr == targetVar:
            return replacement
        else: 
            return expr
        
    elif isinstance(expr, Abstraction):
        if targetVar in expr.params:
            # variable is bounded in this abstraction
            return expr 
        else:
            newBody = substitute(expr.body, targetVar, replacement)
            return Abstraction((expr.params, newBody))
        
    elif isinstance(expr, Application):
        newExprs = []
        for e in expr.exprs:
            newE = substitute(e, targetVar, replacement)
            newExprs.append(newE)
        return Application(newExprs)
    
    else:
        raise ReducerError("unexpected case")

if __name__ == "__main__":
    pass 