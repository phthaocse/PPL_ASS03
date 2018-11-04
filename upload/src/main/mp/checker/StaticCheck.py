
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
        tmp = list(map(lambda x: self.visit(x,(c,True)),ast.body)) 
        return res

    def visitVarDecl(self,ast,c):
        return self.checkRedeclared(Symbol(ast.variable.name,ast.varType),Variable(),c)   

    def visitCallStmt(self, ast, c): 
        at = [self.visit(x,(c[0],False)) for x in ast.param]
        
        res = self.lookup(ast.method.name,c[0],lambda x: x.name)#symbol
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
    
    def visitId(self,ast,c):
        res = self.lookup(ast.name,c[0],lambda x: x.name)
        if res:
            return res.mtype
        else:
            Undeclared(Identifier(),ast.name)
