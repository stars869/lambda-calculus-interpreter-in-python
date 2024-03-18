from dataclasses import dataclass
from core_expr import Expr as Term, Var, Lam, App

class Neutral: pass 
class Value: pass 

class Env:
    def __init__(self, env: list[tuple[str, Value]]):
        self.__env: list[tuple[str, Value]] = env

    def __getitem__(self, name: str):
        for item in self.__env:
            if item[0] == name:
                return item[1]
        raise Exception(f"var {name} not exist in env")

    def add(self, item: tuple[str, Term]):
        new_env = self.__env.copy()
        new_env.append(item)
        return Env(new_env)

    def copy(self):
        return Env(self.__env.copy())

    def __repr__(self) -> str:
        return self.__env.__repr__()
    

# Neutral

@dataclass(frozen=True)
class NVar(Neutral): 
    name: str

@dataclass(frozen=True)
class NApp(Neutral): 
    func: Neutral
    arg: Value

# Value 
    
@dataclass(frozen=True)
class VLam(Value): 
    param: Var
    body: Value 
    env: Env

@dataclass(frozen=True)
class VNeutral(Value): 
    neutral: Neutral

# Eval

def eval(env: Env, term: Term) -> Value:
    if isinstance(term, Var):
        return env[term.name]
    
    elif isinstance(term, Lam):
        return VLam(term.param, term.body, env.copy())
    
    elif isinstance(term, App):
        return apply_value(
            eval(env, term.func), 
            eval(env, term.arg),
        )

    else:
        raise Exception("unexpected case")


def apply_value(vf: Value, va: Value) -> Value:
    if isinstance(vf, VLam):
        return eval(vf.env.add((vf.param.name, va)), vf.body)

    elif isinstance(vf, VNeutral):
        return VNeutral(NApp(vf.neutral, va))
    
    else:
        raise Exception(f"unexpected case {type(vf)}")

# readback

def fresh_name(old_name: str, name_counter: dict[str, int] = {}):
    old_name_splited = old_name.split('_')
    
    if len(old_name_splited) >= 2 and old_name_splited[-1].isdigit():
        base_name = "_".join(old_name_splited[:-1])
    else:
        base_name = old_name
    
    name_count = name_counter.get(base_name, 0) + 1
    name_counter[base_name] = name_count
    return base_name + "_" + str(name_count)


def readback(value: Value) -> Term:
    if isinstance(value, VLam):
        new_param_name = fresh_name(value.param.name)
        return Lam(Var(new_param_name), readback(apply_value(value, VNeutral(NVar(new_param_name)))))
    elif isinstance(value, VNeutral):
        return readback_neutral(value.neutral)
    else:
        raise Exception("unexcepted case")


def readback_neutral(ne: Neutral):
    if isinstance(ne, NVar):
        return Var(ne.name)
    elif isinstance(ne, NApp):
        return App(readback_neutral(ne.func), readback(ne.arg))
