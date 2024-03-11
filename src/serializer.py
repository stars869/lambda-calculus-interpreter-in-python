from core_expr import Expr, App, Lam, Var

def serialize_expr(expr: Expr) -> str:
    if isinstance(expr, Var):
        return expr.name 
    
    elif isinstance(expr, Lam):
        return f"\\{expr.param.name} -> {serialize_expr(expr.body)}"
    
    elif isinstance(expr, App):
        func_s = ""
        if isinstance(expr.func, Var):
            func_s = expr.func.name
        else:
            func_s = f"({serialize_expr(expr.func)})" 
        
        arg_s = ""
        if isinstance(expr.arg, Var):
            arg_s = expr.arg.name
        else:
            arg_s = f"({serialize_expr(expr.arg)})" 

        return f"{func_s} {arg_s}"
        
