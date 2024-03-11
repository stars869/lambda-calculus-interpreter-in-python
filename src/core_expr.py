import typing as t
from dataclasses import dataclass

class Expr: pass 

@dataclass(frozen=True)
class Var(Expr): 
    name: str 

    def __hash__(self) -> int:
        return hash(self.name)

@dataclass(frozen=True)
class Lam(Expr): 
    param: Var
    body: Expr 

@dataclass(frozen=True)
class App(Expr): 
    func: Expr
    arg: Expr 