# coding=utf-8
from util import *
from polynom import *

class M(object):
     def __init__(self):
            "   " 
     def __add__( self, b):
             return Plus( self, b)
     def __mul__( self, b):
             return Mult( self, b)
     def __sub__( self, b):
             return Plus( self, Opp(b))

class Opp( M):
     def __init__(self, a):
             self.a=a
     def eval( self, dico):
             return 0 - self.a.eval( dico)
     def evalsymb( self, dico):
             return Opp (self.a.evalsymb( dico))
     def topolent( self):
             #print( "Opp topolent de "+ str( self.a.topolent()))
             return nb_vect( -1, self.a.topolent())
     def derivee( self, nomvar):
             return Opp( self.a.derivee( nomvar))


class Plus(M):
     def __init__(self, a, b):
             self.a=a
             self.b=b
     def eval( self, dico):
             return self.a.eval( dico) + self.b.eval( dico)
     def evalsymb( self, dico):
             return self.a.evalsymb( dico) + self.b.evalsymb( dico)
     def topolent( self):
             return plus( self.a.topolent(), self.b.topolent())
     def derivee( self, nomvar):
             return Plus( self.a.derivee( nomvar), self.b.derivee( nomvar))

class Mult(M):
     def __init__(self, a, b):
             self.a=a
             self.b=b
     def eval( self, dico):
             return self.a.eval( dico) * self.b.eval( dico)
     def evalsymb( self, dico):
             return self.a.evalsymb( dico) * self.b.evalsymb( dico)
     def topolent( self):
             return mult( self.a.topolent(), self.b.topolent())
     def derivee( self, nomvar):
             return self.a * self.b.derivee(nomvar) + self.a.derivee(nomvar) * self.b

class Nb(M):
     def __init__(self, n):
             self.nb=n
     def eval( self, dico):
             return self.nb 
     def evalsymb( self, dico):
             return self
     def topolent( self):
             return [self.nb]
     def derivee( self, nomvar):
             return Nb( 0)

class Var(M):
     def __init__(self, nom):
             self.nom=nom
     def eval( self, dico):
             if self.nom in dico:
                  return dico[self.nom]
             else:
                  print( 'indefini: ' + str( self.nom))
                  return 1/0
     def evalsymb( self, dico):
             if self.nom in dico:
                  return dico[self.nom]
             else:
                  return self
     def topolent( self):
             if neq( self.nom, "t") :
                  print( "dans polent(), la variable doit s'appeler t, pas "+str(self.nom))
                  return [1/0]
             else :
                  return [0, 1]
     def derivee( self, nomvar):
             if self.nom == nomvar:
                  return Nb( 1)
             else:
                  return Nb(0)

'''
	x=Var('x')
	one=Nb(1)
	y=Var('y')
	cercle=Plus(Mult(x,x), Plus(Mult(y,y), Nb(-1)))
	disk= x*x+y*y+Nb(-1)
	disk.eval( { 'x' : 1, 'y': -1})
	disk= x*x+y*y-Nb(1)
	disk.eval( { 'x' : 1, 'y': -1})
	cercle.eval( { 'x' : 1, 'y': -1})
'''

def evaluer( exp, dico):
          return exp.eval( dico)

def evalsymb( exp, dico):
	return exp.evalsymb( dico)

#evaluer( cercle, { 'x' : 1, 'y': -1})

def topolent( expr):
           return expr.topolent()

