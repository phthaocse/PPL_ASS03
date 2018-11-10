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
        expect  = "Type Mismatch In Statement: For(Id(i)FloatLiteral(5),IntLiteral(1),False,[AssignStmt(Id(i),BinaryOp(-,Id(i),IntLiteral(1)))])"
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
        expect  = "Type Mismatch In Statement: For(Id(i)IntLiteral(5),IntLiteral(1),False,[AssignStmt(Id(i),BinaryOp(-,Id(i),IntLiteral(1)))])"
        self.assertTrue(TestChecker.test(input,expect,430)) 
        
    def test_redeclare_param31(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'i'),IntType()),
                FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'a'),FloatType())],[],
                [If(BinaryOp(r'+',Id(r'a'),Id(r'i')),[For(Id(r'i'),IntLiteral(5),IntLiteral(1),False,
                [Assign(Id(r'i'),BinaryOp(r'-',Id(r'i'),IntLiteral(1)))])],[])],VoidType())])
                
        expect  = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,431))
    
    def test_redeclare_var_param32(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[],VoidType()),
                FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),StringType())],[VarDecl(Id(r'a'),IntType())],[],IntType())])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_redeclare_var33(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[],VoidType()),
                FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),StringType())],
                [VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'i'),FloatType())],[],IntType())])
        expect = "Redeclared Variable: i"
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_redeclare_procedure34(self):
        input =  Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'd'),FloatType()),FuncDecl(Id(r'm'),[],[VarDecl(Id(r'n'),IntType())],[],VoidType()),FuncDecl(Id(r'n'),[],[VarDecl(Id(r'c'),IntType())],[],VoidType()),FuncDecl(Id(r'c'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[Return(FloatLiteral(1.0))],FloatType()),FuncDecl(Id(r'd'),[],[],[],VoidType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'm'),[]),CallStmt(Id(r'n'),[]),CallStmt(Id(r'c'),[IntLiteral(1),IntLiteral(2)]),CallStmt(Id(r'd'),[]),Return(None)],VoidType())])
        expect = "Redeclared Procedure: d"
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_redeclare_var35(self):
        input = Program([VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),FloatType()),VarDecl(Id(r'e'),BoolType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'm'),ArrayType(1,3,IntType()))],[],[With([VarDecl(Id(r'a'),ArrayType(1,5,IntType()))],[]),Return(IntLiteral(0))],IntType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'm'),ArrayType(1,3,IntType()))],[VarDecl(Id(r'c'),ArrayType(1,5,IntType()))],[Return(IntLiteral(0))],IntType()),FuncDecl(Id(r'main'),[],[VarDecl(Id(r'a'),ArrayType(1,3,IntType()))],[Assign(ArrayCell(Id(r'a'),IntLiteral(3)),CallExpr(Id(r'foo'),[IntLiteral(1),CallExpr(Id(r'foo1'),[IntLiteral(1),IntLiteral(2),Id(r'a')]),Id(r'a')])),Return(None)],VoidType())])
        expect = "Redeclared Variable: c"
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_undeclare_id36(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'funcA'),[],[VarDecl(Id(r'b'),IntType())],[Assign(Id(r'a'),IntLiteral(7)),Assign(Id(r'b'),Id(r'a'))],VoidType()),FuncDecl(Id(r'sum'),[VarDecl(Id(r'b'),IntType())],[VarDecl(Id(r'd'),IntType())],[Assign(Id(r'd'),IntLiteral(7)),Return(BinaryOp(r'+',BinaryOp(r'+',Id(r'a'),Id(r'b')),Id(r'd')))],IntType()),FuncDecl(Id(r'main'),[],[VarDecl(Id(r'm'),ArrayType(1,10,IntType()))],[Assign(ArrayCell(Id(r'm'),IntLiteral(1)),CallExpr(Id(r'sum'),[IntLiteral(3)])),CallStmt(Id(r'funcA'),[]),Assign(Id(r'a'),BinaryOp(r'+',IntLiteral(1),ArrayCell(Id(r'n'),IntLiteral(1)))),Return(None)],VoidType())])
        expect = "Undeclared Identifier: n"
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_undeclare_procedure37(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[If(BinaryOp(r'>',Id(r'a'),Id(r'b')),[Assign(Id(r'a'),BinaryOp(r'+',IntLiteral(1),Id(r'b')))],[Assign(Id(r'a'),BinaryOp(r'+',Id(r'b'),IntLiteral(2)))]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),IntType())],[Assign(Id(r'b'),IntLiteral(2)),Assign(Id(r'c'),IntLiteral(3)),If(BinaryOp(r'>',Id(r'a'),Id(r'b')),[Assign(Id(r'd'),BinaryOp(r'+',Id(r'a'),Id(r'c')))],[Assign(Id(r'd'),BinaryOp(r'+',Id(r'b'),CallExpr(Id(r'foo2'),[IntLiteral(1)])))]),Return(Id(r'd'))],IntType()),VarDecl(Id(r'b'),IntType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[While(BinaryOp(r'>',Id(r'a'),IntLiteral(5)),[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(1)))]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[CallExpr(Id(r'foo1'),[IntLiteral(1)]),CallExpr(Id(r'foo2'),[IntLiteral(2)])])),CallStmt(Id(r'funy'),[IntLiteral(4)]),Return(None)],VoidType())])
        expect = "Undeclared Procedure: funy"
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_assign38(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),FloatType()),VarDecl(Id(r'm'),ArrayType(1,10,IntType())),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'b'),BinaryOp(r'+',ArrayCell(Id(r'm'),IntLiteral(1)),UnaryOp(r'-',IntLiteral(1)))),Assign(Id(r'b'),BinaryOp(r'*',Id(r'b'),BinaryOp(r'+',FloatLiteral(1.0),IntLiteral(1)))),Assign(Id(r'b'),UnaryOp(r'not',BinaryOp(r'=',ArrayCell(Id(r'm'),IntLiteral(1)),IntLiteral(1)))),Return(None)],VoidType())])
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),UnaryOp(not,BinaryOp(=,ArrayCell(Id(m),IntLiteral(1)),IntLiteral(1))))"
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_redeclare_var39(self):
        input = Program([VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'main'),[],[],[Return(None)],VoidType())])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_redeclare_var40(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),IntType()),VarDecl(Id(r'b'),IntType()),FuncDecl(Id(r'main'),[],[],[Return(None)],VoidType())])
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_for_typemissmatch41(self):
        input = Program([FuncDecl(Id(r'main'),[],[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(10),True,[Assign(Id(r'j'),IntLiteral(2))]),For(Id(r'a'),IntLiteral(0),BinaryOp(r'=',IntLiteral(5),IntLiteral(3)),True,[Assign(Id(r'j'),IntLiteral(1))]),Return(None)],VoidType())])
        expect = "Type Mismatch In Statement: For(Id(a)IntLiteral(0),BinaryOp(=,IntLiteral(5),IntLiteral(3)),True,[AssignStmt(Id(j),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_return_typemissmatch42(self):
        input = Program([FuncDecl(Id(r'foo'),[],[],[Return(IntLiteral(1))],IntType()),FuncDecl(Id(r'foo1'),[],[],[Return(FloatLiteral(1.0))],IntType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'foo'),[]),CallStmt(Id(r'foo1'),[]),Return(None)],VoidType())])
        expect = "Type Mismatch In Statement: Return(Some(FloatLiteral(1.0)))"
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_return_typemissmatch43(self):
        input = Program([FuncDecl(Id(r'foo'),[],[],[Return(BinaryOp(r'>',IntLiteral(2),IntLiteral(1)))],BoolType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[],[Return(BinaryOp(r'=',Id(r'a'),IntLiteral(1)))],BoolType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],BoolType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'foo'),[]),CallStmt(Id(r'foo1'),[IntLiteral(1)]),CallStmt(Id(r'foo2'),[IntLiteral(2)]),Return(None)],VoidType())])
        expect = "Type Mismatch In Statement: Return(Some(Id(a)))"
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_array_typemissmatch44(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),BoolType()),VarDecl(Id(r'e'),FloatType()),VarDecl(Id(r'm'),ArrayType(1,100,IntType())),FuncDecl(Id(r'foo'),[],[],[Return(IntLiteral(0))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'b'),CallExpr(Id(r'foo'),[])),Assign(Id(r'd'),BooleanLiteral(True)),Assign(Id(r'a'),BinaryOp(r'+',ArrayCell(Id(r'm'),IntLiteral(0)),IntLiteral(1))),Assign(Id(r'c'),BinaryOp(r'+',ArrayCell(Id(r'm'),Id(r'd')),IntLiteral(1))),Return(None)],VoidType())])
        expect = "Type Mismatch In Expression: ArrayCell(Id(m),Id(d))"
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_exp_typemissmatch45(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'main'),[],[VarDecl(Id(r'd'),BoolType())],[Assign(Id(r'd'),BinaryOp(r'and',BinaryOp(r'>',Id(r'a'),Id(r'b')),BooleanLiteral(True))),Assign(Id(r'd'),BinaryOp(r'and',BinaryOp(r'>',Id(r'a'),Id(r'b')),FloatLiteral(1.0))),Return(None)],VoidType())])
        expect = "Type Mismatch In Expression: BinaryOp(and,BinaryOp(>,Id(a),Id(b)),FloatLiteral(1.0))"
        self.assertTrue(TestChecker.test(input,expect,445)) 

    def test_exp_typemissmatch46(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'm'),ArrayType(1,100,FloatType())),FuncDecl(Id(r'foo'),[],[],[Assign(Id(r'a'),UnaryOp(r'-',UnaryOp(r'-',BinaryOp(r'-',Id(r'a'),UnaryOp(r'-',IntLiteral(1))))))],VoidType()),FuncDecl(Id(r'main'),[],[],[CallStmt(Id(r'foo'),[]),Assign(Id(r'a'),UnaryOp(r'-',BinaryOp(r'>',BinaryOp(r'+',ArrayCell(Id(r'm'),IntLiteral(1)),UnaryOp(r'-',IntLiteral(1))),FloatLiteral(1.2)))),Return(None)],VoidType())])       
        expect = "Type Mismatch In Expression: UnaryOp(-,BinaryOp(>,BinaryOp(+,ArrayCell(Id(m),IntLiteral(1)),UnaryOp(-,IntLiteral(1))),FloatLiteral(1.2)))"
        self.assertTrue(TestChecker.test(input,expect,446)) 

    def test_Undeclared_Function47(self):
        input = Program([FuncDecl(Id(r'foo'),[],[VarDecl(Id(r'a'),IntType())],[Assign(Id(r'a'),IntLiteral(4)),If(BinaryOp(r'=',Id(r'a'),IntLiteral(10)),[Return(IntLiteral(1))],[]),Return(IntLiteral(10))],IntType()),FuncDecl(Id(r'main'),[],[VarDecl(Id(r'a'),IntType())],[Assign(Id(r'a'),IntLiteral(0)),If(BinaryOp(r'>',CallExpr(Id(r'foo'),[]),IntLiteral(1)),[If(BinaryOp(r'<=',CallExpr(Id(r'foo2'),[]),IntLiteral(100)),[Return(None)],[Return(None)])],[Assign(Id(r'a'),IntLiteral(2)),Return(None)])],VoidType())])
        expect = "Undeclared Function: foo2"
        self.assertTrue(TestChecker.test(input,expect,447)) 

    def test_Break_notLoop48(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'foo'),[],[],[While(BinaryOp(r'<',Id(r'a'),IntLiteral(100)),[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(1))),Break()]),Return(None)],VoidType()),FuncDecl(Id(r'main'),[],[],[While(BinaryOp(r'<',Id(r'a'),IntLiteral(100)),[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(1))),Break()]),CallStmt(Id(r'foo'),[]),If(BinaryOp(r'=',Id(r'a'),IntLiteral(100)),[Break()],[]),Return(None)],VoidType())])
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_Continue_notLoop49(self):
        input = Program([VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),FuncDecl(Id(r'foo'),[],[],[While(BinaryOp(r'<',Id(r'a'),IntLiteral(100)),[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(1))),Break()]),Return(None)],VoidType()),FuncDecl(Id(r'main'),[],[],[While(BinaryOp(r'<',Id(r'a'),IntLiteral(100)),[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(1))),Break()]),CallStmt(Id(r'foo'),[]),If(BinaryOp(r'=',Id(r'a'),IntLiteral(100)),[Continue()],[]),Return(None)],VoidType())])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_noentrypoint_program50(self):
        input = Program([FuncDecl(Id(r'foo'),[],[],[Return(BinaryOp(r'>',IntLiteral(2),IntLiteral(1)))],BoolType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],IntType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],FloatType()),FuncDecl(Id(r'maint'),[],[],[Return(None)],VoidType())])
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,450))      

    def test_noentrypoint_program51(self):
        input = Program([FuncDecl(Id(r'foo'),[],[],[Return(BinaryOp(r'>',IntLiteral(2),IntLiteral(1)))],BoolType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],IntType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],FloatType()),FuncDecl(Id(r'main'),[VarDecl(Id(r'b'),BoolType())],[],[Return(None)],VoidType())]) 
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,451)) 

    def test_noentrypoint_program52(self):
        input = Program([FuncDecl(Id(r'foo'),[],[],[Return(BinaryOp(r'>',IntLiteral(2),IntLiteral(1)))],BoolType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],IntType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],FloatType()),FuncDecl(Id(r'main'),[],[],[Return(BooleanLiteral(True))],BoolType())])
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,452)) 

    def test_Break_notLoop53(self):
        input = Program([FuncDecl(Id(r'foo'),[],[],[Return(BinaryOp(r'>',IntLiteral(2),IntLiteral(1)))],BoolType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],FloatType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Break(),Continue()],VoidType())])
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_Continue_notLoop54(self):
        input = Program([FuncDecl(Id(r'foo'),[],[],[Return(BinaryOp(r'>',IntLiteral(2),IntLiteral(1)))],BoolType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],FloatType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Continue(),Break(),Continue()],VoidType())])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_function_not_return55(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType()),VarDecl(Id(r'b'),IntType())],[],[If(BinaryOp(r'>',Id(r'a'),Id(r'b')),[Assign(Id(r'a'),BinaryOp(r'+',IntLiteral(1),Id(r'b')))],[Assign(Id(r'a'),BinaryOp(r'+',Id(r'b'),IntLiteral(2)))]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'foo1'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),IntType()),VarDecl(Id(r'd'),IntType())],[Assign(Id(r'b'),IntLiteral(2)),Assign(Id(r'c'),IntLiteral(3)),If(BinaryOp(r'>',Id(r'a'),Id(r'b')),[Assign(Id(r'd'),BinaryOp(r'+',Id(r'a'),Id(r'c')))],[Assign(Id(r'd'),BinaryOp(r'+',Id(r'b'),CallExpr(Id(r'foo2'),[IntLiteral(1)])))])],IntType()),VarDecl(Id(r'b'),IntType()),FuncDecl(Id(r'foo2'),[VarDecl(Id(r'a'),IntType())],[],[While(BinaryOp(r'>',Id(r'a'),IntLiteral(5)),[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),IntLiteral(1)))]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[CallExpr(Id(r'foo1'),[IntLiteral(1)]),CallExpr(Id(r'foo2'),[IntLiteral(2)])])),CallStmt(Id(r'funy'),[IntLiteral(4)]),Return(None)],VoidType())])
        expect = "Function foo1Not Return "
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_function_not_return56(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[],[If(BinaryOp(r'=',Id(r'a'),IntLiteral(2)),[Return(Id(r'a'))],[])],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Function fooNot Return "
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_function_not_return57(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[],[While(BinaryOp(r'=',Id(r'a'),IntLiteral(2)),[Return(Id(r'a'))])],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Function fooNot Return "
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_function_not_return58(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(10),True,[Assign(Id(r'j'),IntLiteral(2)),Assign(Id(r'a'),Id(r'j'))])],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Function fooNot Return "
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_function_not_return59(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[If(BinaryOp(r'>',Id(r'i'),IntLiteral(4)),[Return(Id(r'i'))],[If(BinaryOp(r'>',Id(r'j'),IntLiteral(4)),[Return(Id(r'j'))],[])])],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Function fooNot Return "
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_function_not_return60(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[If(BinaryOp(r'>',Id(r'i'),IntLiteral(4)),[Return(Id(r'i'))],[If(BinaryOp(r'>',Id(r'j'),IntLiteral(4)),[Return(Id(r'j'))],[While(BinaryOp(r'=',Id(r'i'),Id(r'j')),[Return(Id(r'a'))])])])],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Function fooNot Return "
        self.assertTrue(TestChecker.test(input,expect,460))

    def test_function_not_return61(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[If(BinaryOp(r'>',Id(r'i'),IntLiteral(4)),[Return(Id(r'i'))],[If(BinaryOp(r'>',Id(r'j'),IntLiteral(4)),[Return(Id(r'j'))],[For(Id(r'i'),IntLiteral(1),Id(r'j'),True,[Return(Id(r'a'))])])])],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Function fooNot Return "
        self.assertTrue(TestChecker.test(input,expect,461))   

    def test_function_not_return62(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[If(BinaryOp(r'>',Id(r'i'),IntLiteral(4)),[Return(Id(r'i'))],[If(BinaryOp(r'>',Id(r'j'),IntLiteral(4)),[Return(Id(r'j'))],[])]),With([VarDecl(Id(r'b'),IntType()),VarDecl(Id(r'c'),ArrayType(1,3,IntType()))],[Return(Id(r'a'))])],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Function fooNot Return "
        self.assertTrue(TestChecker.test(input,expect,462))    

    def test_Break_notLoop63(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(5),True,[For(Id(r'j'),IntLiteral(1),Id(r'i'),True,[If(BinaryOp(r'=',Id(r'i'),Id(r'j')),[Break()],[])])]),Break(),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_Continue_notLoop64(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(5),True,[For(Id(r'j'),IntLiteral(1),Id(r'i'),True,[If(BinaryOp(r'=',Id(r'i'),Id(r'j')),[Continue()],[])])]),Continue(),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,464))   

    def test_Break_notLoop65(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[With([VarDecl(Id(r'a'),ArrayType(1,5,IntType()))],[Break()]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_Continue_notLoop66(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[With([VarDecl(Id(r'a'),ArrayType(1,5,IntType()))],[Continue()]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,466)) 

    def test_redeclared_variable67(self):
        input = Program([FuncDecl(Id(r'main'),[],[],[],VoidType()),VarDecl(Id(r'main'),IntType())])
        expect = "Redeclared Variable: main"
        self.assertTrue(TestChecker.test(input,expect,467)) 

    def test_redeclared_variable68(self):
        input = Program([FuncDecl(Id(r'main'),[],[],[],VoidType()),VarDecl(Id(r'MAIN'),IntType())])
        expect = "Redeclared Variable: MAIN"
        self.assertTrue(TestChecker.test(input,expect,468)) 

    def test_undeclared_procedure69(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[With([VarDecl(Id(r'a'),ArrayType(1,5,IntType()))],[CallStmt(Id(r'foo1'),[Id(r'a')])]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Undeclared Procedure: foo1"
        self.assertTrue(TestChecker.test(input,expect,469)) 

    def test_undeclared_function70(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[With([VarDecl(Id(r'a'),ArrayType(1,5,IntType()))],[Assign(Id(r'a'),CallExpr(Id(r'foo1'),[Id(r'a')]))]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Undeclared Function: foo1"
        self.assertTrue(TestChecker.test(input,expect,470)) 

    def test_undeclared_procedure71(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[If(BinaryOp(r'=',Id(r'i'),Id(r'j')),[CallStmt(Id(r'Add'),[Id(r'a')])],[]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Undeclared Procedure: Add"
        self.assertTrue(TestChecker.test(input,expect,471)) 

    def test_undeclared_function72(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[If(BinaryOp(r'=',Id(r'i'),Id(r'j')),[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),CallExpr(Id(r'Add'),[Id(r'a')])))],[]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Undeclared Function: Add"
        self.assertTrue(TestChecker.test(input,expect,472)) 

    def test_undeclared_function73(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(5),True,[Assign(Id(r'a'),BinaryOp(r'+',Id(r'a'),CallExpr(Id(r'Add'),[Id(r'a')])))]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Undeclared Function: Add"
        self.assertTrue(TestChecker.test(input,expect,473)) 

    def test_undeclared_procedure74(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(5),True,[CallStmt(Id(r'Procduct'),[Id(r'a')])]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Undeclared Procedure: Procduct"
        self.assertTrue(TestChecker.test(input,expect,474)) 

    def test_undeclared_procedure75(self):
        input = Program([VarDecl(Id(r'a'),IntType()),FuncDecl(Id(r'foo'),[VarDecl(Id(r'a'),IntType())],[VarDecl(Id(r'i'),IntType()),VarDecl(Id(r'j'),IntType())],[For(Id(r'i'),IntLiteral(1),IntLiteral(5),True,[For(Id(r'i'),Id(r'j'),Id(r'a'),True,[CallStmt(Id(r'Product'),[Id(r'a')])])]),Return(Id(r'a'))],IntType()),FuncDecl(Id(r'main'),[],[],[Assign(Id(r'a'),CallExpr(Id(r'foo'),[IntLiteral(2)])),Return(None)],VoidType())])
        expect = "Undeclared Procedure: Product"
        self.assertTrue(TestChecker.test(input,expect,475)) 