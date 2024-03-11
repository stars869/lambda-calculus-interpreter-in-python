from core_expr import Expr, Var, Lam, App
from serializer import serialize_expr
import logging

logging.basicConfig(level=logging.INFO)


class ReducerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def alpha_convert(expr: Expr, old_var: Var, new_var: Var) -> Expr:
    logging.debug("alpha_convert")
    logging.debug(f"expr: {serialize_expr(expr)}")
    logging.debug(f"old_var: {serialize_expr(old_var)}")
    logging.debug(f"new_var: {serialize_expr(new_var)}")
    logging.debug("")

    if isinstance(expr, Var):
        if expr == old_var:
            return new_var
        else:
            return expr

    elif isinstance(expr, Lam):
        if old_var == expr.param:
            return expr 
        else:
            return Lam(expr.param, alpha_convert(expr.body, old_var, new_var))

    elif isinstance(expr, App):
        return App(
            alpha_convert(expr.func, old_var, new_var),
            alpha_convert(expr.arg, old_var, new_var)
        ) 

    else:
        raise ReducerError("unexpected case")

# def isNormalForm(expr: Expr, bindings: dict[str, Expr], bounds: set[Var]) -> bool:
#     if isinstance(expr, Var):
#         if expr in bounds:
#             return True
#         elif expr.name in bindings:
#             return False 
#         else:
#             raise ReducerError(f"Unknown variable: {expr}")
    
#     elif isinstance(expr, Lam):
#         newBounds = bounds.copy()
#         newBounds = newBounds.union(expr.params)
#         return isNormalForm(expr.body, bindings, newBounds)
    
#     elif isinstance(expr, App):
#         if all(map(lambda e: isNormalForm(e, bindings, bounds), expr.exprs)):
#             if isinstance(expr.exprs[0], Lam):
#                 return False 
#             else:
#                 return True
#         else:
#             return False 

#     else:
#         raise ReducerError("Unexpeced expr type")

def get_new_var_name(old_name: str, name_counter: dict[str, int] = {}):
    old_name_splited = old_name.split('_')
    
    if len(old_name_splited) >= 2 and old_name_splited[-1].isdigit():
        base_name = "_".join(old_name_splited[:-1])
    else:
        base_name = old_name
    
    name_count = name_counter.get(base_name, 0) + 1
    name_counter[base_name] = name_count
    return base_name + "_" + str(name_count)


def beta_reduce(expr: Expr, bindings: dict[str, Expr], bounds: set[Var]) -> Expr:
    logging.debug("beta_reduce")
    logging.debug(f"expr: {serialize_expr(expr)}")
    logging.debug("")

    if isinstance(expr, Var):
        if expr.name in bindings and expr not in bounds:
            return bindings[expr.name]
        else:
            return expr 

    elif isinstance(expr, Lam):
        if expr.param not in bounds:
            bounds.add(expr.param)
            new_lam = Lam(expr.param, beta_reduce(expr.body, bindings, bounds))
            bounds.remove(expr.param)
            return new_lam
        else:
            new_param = Var(get_new_var_name(expr.param.name))
            new_body = alpha_convert(expr.body, expr.param, new_param)
            
            bounds.add(new_param)
            new_lam = Lam(new_param, beta_reduce(new_body, bindings, bounds))
            bounds.remove(new_param)

            return new_lam

    elif isinstance(expr, App):
        return do_apply(
            beta_reduce(expr.func, bindings, bounds), 
            beta_reduce(expr.arg, bindings, bounds), 
            bindings, bounds
        )

    else:
        raise ReducerError("unexpected case")

def do_apply(func: Expr, arg: Expr, bindings: dict[str, Expr], bounds: set[Var]):
    logging.debug("do_apply")
    logging.debug(f"func: {serialize_expr(func)}")
    logging.debug(f"arg: {serialize_expr(arg)}")
    logging.debug("")

    if isinstance(func, Var) or isinstance(func, App):
        return App(func, arg)
    
    elif isinstance(func, Lam):
        if func.param not in bounds:
            bounds.add(func.param)
            result = substitute(func.body, func.param, arg, bindings, bounds)
            bounds.remove(func.param)
            return result
        else:
            new_param = Var(get_new_var_name(func.param.name))
            new_body = alpha_convert(func.body, func.param, new_param)
            
            bounds.add(new_param)
            result = substitute(new_body, new_param, arg)
            bounds.remove(new_param)
            return result
    else: 
        raise ReducerError("unexpected case")

    
def substitute(expr: Expr, targetVar: Var, replacement: Expr, bindings: dict[str, Expr], bounds: set[Var]) -> Expr:
    logging.debug("substitute")
    logging.debug(f"expr: {serialize_expr(expr)}")
    logging.debug(f"targetVar: {serialize_expr(targetVar)}")
    logging.debug(f"replacement: {serialize_expr(replacement)}")
    logging.debug(f"")

    if isinstance(expr, Var):
        if expr == targetVar:
            return replacement
        else: 
            return expr
        
    elif isinstance(expr, Lam):
        if expr.param not in bounds:
            bounds.add(expr.param)
            result = substitute(expr.body, targetVar, replacement, bindings, bounds)
            bounds.remove(expr.param)
            return Lam(expr.param, result)
        else:
            new_param = Var(get_new_var_name(expr.param.name))
            new_body = alpha_convert(expr.body, expr.param, new_param)

            bounds.add(new_param)
            result = substitute(new_body, targetVar, replacement, bindings, bounds)
            bounds.remove(new_param)
            return Lam(new_param, result)
            
    elif isinstance(expr, App):
        new_func = substitute(expr.func, targetVar, replacement, bindings, bounds)
        new_arg = substitute(expr.arg, targetVar, replacement, bindings, bounds)
        return beta_reduce(App(new_func, new_arg), bindings, bounds)

    else:
        raise ReducerError("unexcepted case")
        

if __name__ == "__main__":
    pass 