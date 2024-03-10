import typing as t
from dataclasses import dataclass

class Expr: pass 

@dataclass
class Var(Expr): 
    value: str 

    def __hash__(self) -> int:
        return hash(self.value)

@dataclass
class Lam(Expr): 
    param: Var
    body: Expr 

@dataclass
class App(Expr): 
    func: Expr
    arg: Expr 