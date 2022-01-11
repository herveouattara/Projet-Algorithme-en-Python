# coding=utf−8
import math
infini=float("inf")

def is_num( v):
	return (type( v) is float) or (type( v) is int)

def neq( a, b):
	return not( a==b)

def eq( a, b):
	return a==b

#les listes
def cons( t, q):
	return (t, q)

def hd( liste):
	assert( neq( None, liste))
	(t, q) = liste #definit t et q
	return t

def tl( liste):
	   assert( neq( None, liste))
	   (t, q) = liste #definit t et q
	   return q

# foldl( +, 0, (1, (2, (3, None)))) rend la somme des elts de la liste
def foldl( operation, silistevide, liste):
	if None==liste :
		return silistevide
	else:
		return foldl( operation, operation( silistevide, hd( liste)), tl( liste))

#longueur d'une liste:
def lgr( liste):
	return foldl( (lambda n, li : n+1), 0, liste)

#on supprime les elts en tete de liste qui ne satisfont pas pred
def eteter( predicat_keep, l):
	if None==l or predicat_keep( hd(l)):
		return l
	else:
		return eteter( predicat_keep, tl( l))

def filtrage( tokeep, l):
	if None==l:
		return None
	elif tokeep( hd( l)):
		return cons( hd( l), filtrage( tokeep, tl( l)))
	else:
		return filtrage( tokeep, tl( l))
	
#renverse une liste
def reverse( l):
	pile=None
	while neq( None, l) :
			pile=cons( hd(l), pile)
			l= tl( l)
	return pile

def mymap( f, l):
	if None==l:
		return None
	else:
		return cons( f( hd( l)), mymap( f, tl( l)))

# convertit une liste en vecteur
def ltov( liste) :
	n= lgr( liste)
	v= [None]*n
	for i in range( 0, n) :
		v[i]= hd( liste)
		liste= tl( liste)
	return  v
	
# convertit un vecteur en liste
def vtol( tab):
	if 0==len( tab):
		return None
	else:
		l = None
		for i in range( len( tab)-1, -1, -1) :
			l= cons( tab[i], l)
		return l


#somme des fi( i) pour i de i1 a i2
def sigma( i1, i2, fi):
	if i1==i2:
		return fi( i1)
	else:
		return fi( i1 ) + sigma( i1+1, i2, fi)

# cree un vecteur
def vecteur( n, f):
	return [ f(i) for i in range( 0, n) ]


def matrice( nl, nc, f):
        return vecteur( nl, (lambda l : vecteur( nc, (lambda c: f( l, c)))))

def pscal3( pt1, pt2):
        (x1,y1,z1)=pt1
        (x2,y2,z2)=pt2
        return x1*x2 + y1*y2 + z1*z2
def clamp( mi, ma, v):
        return min( ma, max( mi, v))


def norm3 (abc):
        (a,b,c)= abc
        (a,b,c)=(float(a),float(b),float(c))
        n=math.sqrt(a*a+b*b+c*c)
        return n

def normalize3( abc):
        (a,b,c)= abc
        (a,b,c)=(float(a),float(b),float(c))
        n=norm3 ((a,b,c))
        if 0.==n:
                return (0.,0.,0.)
        else:
                return (a/n, b/n, c/n)

def nb_vect( k, v):
	return vecteur( len(v), (lambda i : k*v[i]))

#interpolation lineaire
def interpole( x1, y1, x2, y2, x) :
        # x=x1 -> y=y1
        # x=x2 -> y=y2
        x1, y1, x2, y2, x= float(x1), float(y1), float( x2), float(y2), float(x)
        return (x-x2)/(x1-x2)*y1 + (x-x1)/(x2-x1)*y2

