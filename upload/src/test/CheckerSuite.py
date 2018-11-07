import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):

    def test_undeclared_procedure1(self):
        """Simple program: int main() {} """
        input = Program([FuncDecl(Id("main"),[],[],[
            CallStmt(Id("foo"),[])])])
        expect = "Undeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_undeclared_function2(self):
        """Simple program: int main() {} """
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[]))],VoidType())])
        expect = "Undeclared Function: foo"
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

    def test_unary_expression6(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                FuncDecl(Id("main"),[],[],[
                CallStmt(Id("putIntLn"),[UnaryOp("not",Id("a"))])])])
        expect  = "Type Mismatch In Expression: UnaryOp(not,Id(a))"
        self.assertTrue(TestChecker.test(input,expect,406))
    
    def test_unary_expression7(self):
        input = Program([
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                CallStmt(Id("putIntLn"),[UnaryOp("not",Id("f"))])])])
        expect  = "Type Mismatch In Expression: UnaryOp(not,Id(f))"
        self.assertTrue(TestChecker.test(input,expect,407))    
                    
    def test_unary_expression8(self):
        input = Program([
                VarDecl(Id("b"),BoolType()),
                FuncDecl(Id("main"),[],[],[
                CallStmt(Id("putIntLn"),[UnaryOp("-",Id("b"))])])])
        expect  = "Type Mismatch In Expression: UnaryOp(-,Id(b))"
        self.assertTrue(TestChecker.test(input,expect,408))   
    def test_binary_expression9(self):
        input = Program([
                VarDecl(Id("b"),BoolType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('+',IntLiteral(1),IntLiteral(4))]),
                    CallStmt(Id("putIntLn"),[BinaryOp('/',IntLiteral(1),IntLiteral(4))])])])
        expect  = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[BinaryOp(/,IntLiteral(1),IntLiteral(4))])"
        self.assertTrue(TestChecker.test(input,expect,409))  

    def test_binary_expression10(self):
        input = Program([
                VarDecl(Id("b"),BoolType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('mod',IntLiteral(1),IntLiteral(4))]),
                    CallStmt(Id("putIntLn"),[BinaryOp('<',IntLiteral(1),IntLiteral(4))])])])
        expect  = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[BinaryOp(<,IntLiteral(1),IntLiteral(4))])"
        self.assertTrue(TestChecker.test(input,expect,410))  

    def test_binary_expression11(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("b"),BoolType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('+',Id("a"),Id("b"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(+,Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,411))  

    def test_binary_expression12(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("s"),StringType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('+',Id("a"),Id("s"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(+,Id(a),Id(s))"
        self.assertTrue(TestChecker.test(input,expect,412))  

    def test_binary_expression13(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('or',Id("a"),Id("f"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(or,Id(a),Id(f))"
        self.assertTrue(TestChecker.test(input,expect,413))  

    def test_binary_expression14(self):
        input = Program([
                VarDecl(Id("b"),BoolType()),
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('-',Id("b"),Id("f"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(-,Id(b),Id(f))"
        self.assertTrue(TestChecker.test(input,expect,414))  

    def test_binary_expression15(self):
        input = Program([
                VarDecl(Id("s"),StringType()),
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('*',Id("s"),Id("f"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(*,Id(s),Id(f))"
        self.assertTrue(TestChecker.test(input,expect,415))  

    def test_binary_expression16(self):
        input = Program([
                VarDecl(Id("b1"),BoolType()),
                VarDecl(Id("b2"),BoolType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('=',Id("b1"),Id("b2"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(=,Id(b1),Id(b2))"
        self.assertTrue(TestChecker.test(input,expect,416))  

    def test_binary_expression17(self):
        input = Program([
                VarDecl(Id("b"),BoolType()),
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('+',Id("f"),Id("b"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(+,Id(f),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,417))    

    def test_binary_expression18(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('and',Id("f"),Id("a"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(and,Id(f),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,418))  

    def test_binary_expression19(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("b"),BoolType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('/',Id("b"),Id("a"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(/,Id(b),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,419))  

    def test_binary_expression20(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('div',Id("a"),Id("f"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(div,Id(a),Id(f))"
        self.assertTrue(TestChecker.test(input,expect,420)) 

    def test_binary_expression21(self):
        input = Program([
                VarDecl(Id("a"),IntType()),
                VarDecl(Id("f"),FloatType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('mod',Id("a"),Id("f"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(mod,Id(a),Id(f))"
        self.assertTrue(TestChecker.test(input,expect,421))   

    def test_binary_expression22(self):
        input = Program([
                VarDecl(Id("a1"),IntType()),
                VarDecl(Id("a2"),IntType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('and',Id("a1"),Id("a2"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(and,Id(a1),Id(a2))"
        self.assertTrue(TestChecker.test(input,expect,422))   

    def test_binary_expression23(self):
        input = Program([
                VarDecl(Id("a1"),IntType()),
                VarDecl(Id("a2"),IntType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('andthen',Id("a1"),Id("a2"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(andthen,Id(a1),Id(a2))"
        self.assertTrue(TestChecker.test(input,expect,423)) 

    def test_binary_expression24(self):
        input = Program([
                VarDecl(Id("a1"),IntType()),
                VarDecl(Id("a2"),IntType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('or',Id("a1"),Id("a2"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(or,Id(a1),Id(a2))"
        self.assertTrue(TestChecker.test(input,expect,424)) 

    def test_binary_expression25(self):
        input = Program([
                VarDecl(Id("a1"),IntType()),
                VarDecl(Id("a2"),IntType()),
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[BinaryOp('orelse',Id("a1"),Id("a2"))])])])
        expect  = "Type Mismatch In Expression: BinaryOp(orelse,Id(a1),Id(a2))"
        self.assertTrue(TestChecker.test(input,expect,425)) 

    def test_for_typemissmatch26(self):
        input = Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'main'),[],[],[For(Id(r'i'),FloatLiteral(5),IntLiteral(1),False,[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))])],VoidType())])
        expect  = "Type Mismatch In Statement: For(Id(i),FloatLiteral(5),IntLiteral(1),False,[AssignStmt(Id(i),BinaryOp(-,Id(i),IntLiteral(1)))])"
        self.assertTrue(TestChecker.test(input,expect,426))  

    def test_if_typemissmatch27(self):
        input = Program([VarDecl(Id(r'd'),IntType()),VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[If(BinaryOp("+",Id(r'a'),IntLiteral(3)),[If(BinaryOp(r'<',Id(r'a'),IntLiteral(6)),[Assign(Id(r'a'),IntLiteral(1))],[Assign(Id(r'a'),IntLiteral(3))])],[Assign(Id(r'a'),IntLiteral(6))])],VoidType())])
        expect  = "Type Mismatch In Statement: If(BinaryOp(+,Id(a),IntLiteral(3)),[If(BinaryOp(<,Id(a),IntLiteral(6)),[AssignStmt(Id(a),IntLiteral(1))],[AssignStmt(Id(a),IntLiteral(3))])],[AssignStmt(Id(a),IntLiteral(6))])"
        self.assertTrue(TestChecker.test(input,expect,427))  

    def test_while_typemissmatch28(self):
        input = Program([VarDecl(Id(r'i'),IntType()),FuncDecl(Id(r'main'),[],[],[While(BinaryOp(r'-',Id(r'i'),IntLiteral(0)),[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))])],VoidType())])
        expect  = "Type Mismatch In Statement: While(BinaryOp(-,Id(i),IntLiteral(0)),[AssignStmt(Id(i),BinaryOp(-,Id(i),IntLiteral(1)))])"
        self.assertTrue(TestChecker.test(input,expect,428))  

    def test_while_if_typemissmatch29(self):
        input = Program([VarDecl(Id(r'd'),IntType()),VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[While(BinaryOp(r'=',Id(r'a'),Id("d")),[If(BinaryOp("-",Id(r'a'),IntLiteral(15)),[Break()],[])])],VoidType())])
        expect  = "Type Mismatch In Statement: If(BinaryOp(-,Id(a),IntLiteral(15)),[Break],[])"
        self.assertTrue(TestChecker.test(input,expect,429))  
        
    def test_if_for_typemissmatch30(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'i'),FloatType()),FuncDecl(Id(r'main'),[],[],[If(BinaryOp(r'=',Id(r'a'),Id(r'i')),[For(Id(r'i'),IntLiteral(5),IntLiteral(1),False,[Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))])],[])],VoidType())])
        expect  = "Type Mismatch In Statement: For(Id(i),IntLiteral(5),IntLiteral(1),False,[AssignStmt(Id(i),BinaryOp(-,Id(i),IntLiteral(1)))])"
        self.assertTrue(TestChecker.test(input,expect,430)) 
        