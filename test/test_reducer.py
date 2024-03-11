import unittest

import sys 
sys.path.append("../src")
from core_expr import Lam, App, Var, Expr
from my_reducer import alpha_convert, do_apply


class TestAlphaConvert(unittest.TestCase):
    def test_alpha_convert_1(self):
        expr = Lam(Var('x'), Lam(Var('y'), Var('y')))
        result_expr = alpha_convert(expr, Var('x_1'), Var('x_2'))
        expected_expr = Lam(Var('x'), Lam(Var('y'), Var('y')))
        assert(result_expr == expected_expr)

    def test_alpha_convert_2(self):
        expr = Lam(Var('x'), Lam(Var('y'), Var('y')))
        result_expr = alpha_convert(expr, Var('x'), Var('x_2'))
        expected_expr = Lam(Var('x'), Lam(Var('y'), Var('y')))
        assert(result_expr == expected_expr)

    def test_alpha_convert_3(self):
        expr = Lam(Var('x'), Lam(Var('y'), Var('x')))
        result_expr = alpha_convert(expr, Var('x'), Var('x_2'))
        expected_expr = Lam(Var('x'), Lam(Var('y'), Var('x')))
        assert(result_expr == expected_expr)

# class TestBetaReduce(unittest.TestCase):
#     def test_beta_reduce_1():

class TestDoApply(unittest.TestCase):
    def test_do_apply_1(self):
        expr1 = Lam(Var("x_1"), Lam(Var("y"), Var("x_1")))
        expr2 = Lam(Var("x_2"), Lam(Var("y"), Var("y")))
        expected = Lam(Var("y"), Lam(Var("x_2"), Lam(Var("y"), Var("y"))))
        result = do_apply(expr1, expr2, {}, set())
        print(result)
        assert(expected == result)

if __name__ == '__main__':
    unittest.main()