import typing as t
from core_expr import Expr, App, Lam, Var
from parse import expr_parser
from nbe import Env, eval, readback
from serialize import serialize_expr


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
    unnormalized_bindings = parse_file("./test/test.lambda")
    
    env = Env([])
    
    for (name, expr) in unnormalized_bindings:
        print(f"{name} = {serialize_expr(expr)}")

        value = eval(env, expr)
        norm_expr = readback(value)
        print(f"{name} = {serialize_expr(norm_expr)}")
        print()

        env = env.add((name, value))
