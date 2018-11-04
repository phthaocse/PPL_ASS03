
"""
 * @author Phan Thao
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import *

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

class StaticChecker(BaseVisitor,Utils):

    global_envi =  [Symbol("getInt",MType([],IntType())),
    			    Symbol("putInt",MType([IntType()],VoidType())),
                    Symbol("putIntLn",MType([IntType()],VoidType())),
                    Symbol("getFloat",MType([],FloatType())),
                    Symbol("putFloat",MType([FloatType()],VoidType())),
                    Symbol("putFloatLn",MType([FloatType()],VoidType())),
                    Symbol("putBool",MType([BoolType()],VoidType())),
                    Symbol("putBoolLn",MType([BoolType()],VoidType())),
                    Symbol("putString",MType([StringType()],VoidType())),
                    Symbol("putStringLn",MType([StringType()],VoidType())),
                    Symbol("putLn",MType([],VoidType()))]
            
    
    def __init__(self,ast):
        self.ast = ast
   
    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def checkRedeclared(self,sym,kind,env):
        if self.lookup(sym.name,env, lambda x:x.name):
            raise Redeclared(kind,sym.name)
        else:
            return sym
	
    def visitProgram(self,ast, c): 
        return reduce(lambda x,y: [self.visit(y,x+c)]+x,ast.decl,[])

    def visitFuncDecl(self,ast, c): 
        kind = Procedure() if type(ast.returnType) is VoidType else Function()
        res = self.checkRedeclared(Symbol(ast.name.name,MType([x.varType for x in ast.param],ast.returnType)),kind,c)
        tmp = list(map(lambda x: self.visit(x,c),ast.body)) 
        return res

    def visitVarDecl(self,ast,c):
        return self.checkRedeclared(Symbol(ast.variable.name,ast.varType),Variable(),c)   

    def visitCallStmt(self, ast, c): 
        at = [self.visit(x,c) for x in ast.param]
        
        res = self.lookup(ast.method.name,c,lambda x: x.name)#symbol
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif len(res.mtype.partype) != len(at) or True in [type(a) != type(b) for a,b in zip(at,res.mtype.partype)]:
            raise TypeMismatchInStatement(ast)            
        else:
            return res.mtype.rettype

    def visitIntLiteral(self,ast, c): 
        return IntType()

    def visitFloatLiteral(self,ast,c):
        return FloatType()

    def visitBooleanLiteral(self,ast,c):
        return BoolType()

    def visitStringLiteral(self,ast,c):
        return StringType()    
    
    def visitArrayCell(self,ast,c):
        return ArrayType()
    

    def visitId(self,ast,c):
        res = self.lookup(ast.name,c,lambda x: x.name)
        if res:
            return res.mtype
        else:
            Undeclared(Identifier(),ast.name)

    def visitUnaryOp(self,ast,c):
        expr = self.visit(ast.body,c)#return type
        if type(expr) in [IntType,FloatType]:
            if ast.op == '-':
                return expr
            else:
                raise TypeMismatchInExpression(expr)
        elif type(expr) in [StringType,ArrayType]:
            raise TypeMismatchInExpression(expr)
        else: 
            if ast.op == 'not':
                return expr 
            else:
                raise TypeMismatchInExpression(expr)

    def visitBinaryOp(self,ast,c):
        lefttype = self.visit(ast.left,c)
        righttype = self.visit(ast.right,c)      
        if type(lefttype) is IntType:
            if type(righttype) is  IntType:
                if ast.op in ['+','-','*','div','mod']:
                    return IntType()
                elif ast.op == '/':
                    return FloatType()
                elif ast.op in ['<','<=','>','>=','<>','=']:
                    return BoolType()
                else: 
                    raise TypeMismatchInExpression(IntType())
            elif type(righttype) is FloatType:
                if ast.op in ['+','-','*','/']:
                    return FloatType()
                elif ast.op in ['<','<=','>','>=','<>','=']:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(IntType())

            
            