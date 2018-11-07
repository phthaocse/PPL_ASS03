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
        res = reduce(lambda x,y: x + [self.visit(y,x+c)],ast.decl,[])
        if self.lookup("main",res, lambda x: x.name) == None:
            raise NoEntryPoint()
        return res


    def visitFuncDecl(self,ast, c): 
        kind = Procedure() if type(ast.returnType) is VoidType else Function()
        param = reduce(lambda x,y: x + [self.visit(y,x+c)],ast.param,[])
        local = reduce(lambda x,y: x + [self.visit(y,x+c)],ast.param,param)
        c = local + c #list local + list global
        res = self.checkRedeclared(Symbol(ast.name.name,MType([x.varType for x in ast.param],ast.returnType)),kind,c)
        tmp = list(map(lambda x: self.visit(x,(c,False)),ast.body)) 
        return res
        
    def visitVarDecl(self,ast,c):
        return self.checkRedeclared(Symbol(ast.variable.name,ast.varType),Variable(),c)   

    def visitCallStmt(self, ast, c): 
        at = [self.visit(x,c) for x in ast.param]
        
        res = self.lookup(ast.method.name,c[0],lambda x: x.name)#symbol
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif len(res.mtype.partype) != len(at) or True in [type(a) != type(b) for a,b in zip(at,res.mtype.partype)]:
            raise TypeMismatchInStatement(ast)            
        else:
            return res.mtype.rettype

    def visitCallExpr(self, ast, c): 
        at = [self.visit(x,c) for x in ast.param]
        
        res = self.lookup(ast.method.name,c[0],lambda x: x.name)#symbol
        if res is None or type(res.mtype) is MType or type(res.mtype.rettype) is VoidType:
            raise Undeclared(Function(),ast.method.name)
        elif len(res.mtype.partype) != len(at) or True in [type(a) != type(b) for a,b in zip(at,res.mtype.partype)]:
            raise TypeMismatchInExpression(ast)            
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
    
    def visitArrayType(self, ast, c):
        return ArrayType(ast.lower,ast.upper,ast.eleType)

    def visitArrayCell(self,ast,c):
        return self.visit(ast.arr,c)

    def visitId(self,ast,c):
        res = self.lookup(ast.name,c[0],lambda x: x.name)
        if res:
            return res.mtype
        else:
            raise Undeclared(Identifier(),ast.name)

    def visitUnaryOp(self,ast,c):
        expr = self.visit(ast.body,c)#return type
        if type(expr) in [IntType,FloatType]:
            if ast.op == '-':
                return expr
            else:
                raise TypeMismatchInExpression(ast)
        elif type(expr) in [StringType,ArrayType]:
            raise TypeMismatchInExpression(ast)
        else: 
            if ast.op == 'not':
                return expr 
            else:
                raise TypeMismatchInExpression(ast)

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
                    raise TypeMismatchInExpression(ast)
            elif type(righttype) is FloatType:
                if ast.op in ['+','-','*','/']:
                    return FloatType()
                elif ast.op in ['<','<=','>','>=','<>','=']:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        elif type(lefttype) is FloatType:
            if type(righttype) is  IntType:
                if ast.op in ['+','-','*','/']:
                    return FloatType()
                elif ast.op in ['<','<=','>','>=','<>','=']:
                    return BoolType() 
                else: 
                    raise TypeMismatchInExpression(ast)  
            elif type(righttype) is FloatType:
                if ast.op in ['+','-','*','/']:
                    return FloatType()
                elif ast.op in ['<','<=','>','>=','<>','=']:
                    return BoolType() 
                else: 
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        elif type(lefttype) is BoolType:
            if type(righttype) is BoolType:
                if ast.op in ['and','andthen','or','orelse']:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast) 
            else:
                raise TypeMismatchInExpression(ast) 
        else:
            raise TypeMismatchInExpression(ast) 

    def visitAssign(self, ast,c):
        lhs = self.visit(ast.lhs,c)
        exp = self.visit(ast.exp,c)    
        if type(lhs) in [StringType,ArrayType]:
            raise TypeMismatchInExpression(ast)
        elif type(lhs) != type(exp):
            if type(lhs) is FloatType and type(exp) is IntType:
                return FloatType()
            else:
                raise TypeMismatchInExpression(ast) 
        else:
            return lhs
        
    def visitReturn(self, ast, c):
        restype = None
        for x in c[0]:
            if type(x.mtype) is MType:
                restype = x.mtype.restype
        if type(restype) is VoidType:
            if ast.expr:
                raise TypeMismatchInStatement(ast)
            else:
                return VoidType()
        else:
            if ast.expr:
                exp = self.visit(ast.expr,c)
                if type(exp) != type(restype):
                    if type(exp) is IntType and type(restype) is FloatType:
                        return FloatType()
                    else:
                        raise TypeMismatchInStatement(ast)                        
                else:
                    return restype
            else:
                raise TypeMismatchInStatement(ast) 


    def visitIf(self, ast, c):
        exp = self.visit(ast.expr,c)            
        if type(exp) is not BoolType:
            raise TypeMismatchInStatement(ast)
        else:
            [self.visit(x,c) for x in ast.thenStmt] 
            [self.visit(x,c) for x in ast.elseStmt]

    def visitWhile(self,ast,c):
        exp = self.visit(ast.exp,c)            
        if type(exp) is not BoolType:
            raise TypeMismatchInStatement(ast)
        else:
            [self.visit(x,(c[0],True)) for x in ast.sl]

    def visitFor(self,ast,c):
        exp1 = self.visit(ast.expr1,c)
        exp2 = self.visit(ast.expr2,c)
        Id =  self.visit(ast.id,c)
        if True in [type(x) is not IntType for x in [Id,exp1,exp2]]:
            raise TypeMismatchInStatement(ast)
        else:
            [self.visit(x,(c[0],True)) for x in ast.loop]
    
    def visitWith(self, ast, c):
        [self.visit(x,c) for x in ast.decl]
        [self.visit(x,c) for x in ast.stmt]

    def visitBreak(self, ast, c):
        if c[1] != True:
            raise BreakNotInLoop()
    
    def visitContinue(self,ast,c):
        if c[1] != True:
            raise ContinueNotInLoop()