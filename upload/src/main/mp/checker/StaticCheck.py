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
    
    def __str__(self):
        return "Mtype(" + ','.join(str(i) for i in self.partype) + "," + str(self.rettype) +")"

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + ',' + str(self.mtype) + ')'

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
        tmp = [x for x in ast.decl]
        glo = []
        for i in tmp:
            if type(i) is FuncDecl:
                glo = glo + [Symbol(i.name.name,MType([x.varType for x in i.param],i.returnType))]
            else:
                glo = glo + [Symbol(i.variable.name,i.varType)]

        res = reduce(lambda x,y: x + [self.visit(y,(x+c,glo+c))],ast.decl,[])
        mainfind = self.lookup("main",res, lambda x: x.name) 
        if mainfind == None:
            raise NoEntryPoint()
        if mainfind.mtype.partype != None or mainfind.mtype.rettype is not VoidType:
            raise NoEntryPoint()
        return res


    def visitFuncDecl(self,ast, c): 
        kind = Procedure() if type(ast.returnType) is VoidType else Function()
        param = reduce(lambda x,y: x + [self.visit(y,x)],ast.param,[])
        local = reduce(lambda x,y: x + [self.visit(y,x)],ast.local,param)
        c1 = local + c[0] #list local + list global use for check redecl 
        res = self.checkRedeclared(Symbol(ast.name.name,MType([x.varType for x in ast.param],ast.returnType)),kind,c1)
        c2 = local + c[1] #list local + list global use for check undecl
        tmp = list(map(lambda x: self.visit(x,(c2,False,ast.returnType)),ast.body)) 
        check = False
        for x in ast.body:
            if type(x) is Return:
                check = True
        if check == False:
            if type(ast.returnType) is not VoidType:
                for x in tmp:
                    if type(x) is bool:
                        if x == True:
                            check = True

                if check == False:
                    raise FunctionNotReturn(ast.name.name)     
        return res
        
    def visitVarDecl(self,ast,c):
        if type(c) is tuple:
            c = c[0]
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
        if res is None or not type(res.mtype) is MType or type(res.mtype.rettype) is VoidType:
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
        arr = self.visit(ast.arr,c)
        idx = self.visit(ast.idx,c)
        if type(idx) != IntType:
            raise TypeMismatchInExpression(ast)
        if type(arr) != ArrayType:
            raise TypeMismatchInExpression(ast)
        return arr.eleType

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
            raise TypeMismatchInStatement(ast)
        elif type(lhs) != type(exp):
            if type(lhs) is FloatType and type(exp) is IntType:
                return FloatType()
            else:
                raise TypeMismatchInStatement(ast) 
        else:
            return lhs
        
    def visitReturn(self, ast, c):
        restype = c[2]
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
            checkthen = False
            checkelse = False
            for x in ast.thenStmt:
                if type(x) is Return:
                    checkthen = True
            for x in ast.elseStmt:
                if type(x) is Return:
                    checkelse = True
            [self.visit(x,c) for x in ast.thenStmt] 
            [self.visit(x,c) for x in ast.elseStmt]
            return (checkthen and checkelse)

    def visitWhile(self,ast,c):
        exp = self.visit(ast.exp,c)            
        if type(exp) is not BoolType:
            raise TypeMismatchInStatement(ast)
        else:
            [self.visit(x,(c[0],True,c[2])) for x in ast.sl]
            return False

    def visitFor(self,ast,c):
        exp1 = self.visit(ast.expr1,c)
        exp2 = self.visit(ast.expr2,c)
        Id =  self.visit(ast.id,c)
        if True in [type(x) is not IntType for x in [Id,exp1,exp2]]:
            raise TypeMismatchInStatement(ast)
        else:
            [self.visit(x,(c[0],True,c[2])) for x in ast.loop]
    
    def visitWith(self, ast, c):
        reduce(lambda x,y: x + [self.visit(y,x)],ast.decl,[])
        [self.visit(x,c) for x in ast.stmt]
        return False

    def visitBreak(self, ast, c):
        if c[1] != True:
            raise BreakNotInLoop()
    
    def visitContinue(self,ast,c):
        if c[1] != True:
            raise ContinueNotInLoop()