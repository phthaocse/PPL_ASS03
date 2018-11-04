import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):

    def test_undeclared_function1(self):
        """Simple program: int main() {} """
        input = Program([FuncDecl(Id("main"),[],[],[
            CallStmt(Id("foo"),[])])])
        expect = "Undeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_function2(self):
        """Simple program: int main() {} """
        input = Program([FuncDecl(Id("main"),[],[],[
            CallStmt(Id("foo"),[Id("a")])])])
        expect = "Undeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_diff_numofparam_expr3(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[])])])
                        
        expect = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_redeclared_function4(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("b"),IntType()),
                VarDecl(Id("c"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[Id("a")]),
                    CallStmt(Id("putIntLn"),[Id("c")])])])
                
        expect  = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[Id(c)])"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_redeclared_function5(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("b"),IntType()),
                VarDecl(Id("c"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[Id("a")]),
                    CallStmt(Id("putIntLn"),[Id("b")])]),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[Id("a")]),
                    CallStmt(Id("putIntLn"),[Id("c")])])])
                
        expect  = "Redeclared Procedure: main"
        self.assertTrue(TestChecker.test(input,expect,405))

    
    