import typing as t
from core_expr import Expr, App, Lam, Var
from my_parser import expr_parser
from my_reducer import beta_reduce
from serializer import serialize_expr


def sep_code_blocks(s: str) -> list[str]:
    lines = s.split('\n')
    blocks = []
    currentBlock = []

    for line in lines:
        if not line:
            continue
        if line.strip().startswith("--"):
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

def sep_binding(s: str) -> t.Tuple[str, str]:
    result = s.split('=')
    assert(len(result) == 2)

    varname = result[0].strip() 
    expr = result[1].strip()
    assert(varname != "")
    assert(expr != "")

    return (varname, expr)

def parse_file(path: str) -> list[t.Tuple[str, Expr]]:
    file = open(path, "r")
    code = file.read()
    file.close()

    blocks = sep_code_blocks(code)

    bindings = []
    for block in blocks:
        (varname, exprCode) = sep_binding(block)
        expr = expr_parser.parse(exprCode)
        bindings.append((varname, expr))
    return bindings


if __name__ == "__main__":
    notReducedBindings = parse_file("./test/test.lambda")
    
    bindings = {}
    
    for (name, expr) in notReducedBindings:
        print(f"{name} = {serialize_expr(expr)}")

        norm_expr = beta_reduce(expr, bindings, set())
        print(f"{name} = {serialize_expr(norm_expr)}")
        print()

        bindings[name] = norm_expr
