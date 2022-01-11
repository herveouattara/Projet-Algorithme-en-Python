# coding=utf-8
from util import *

# calcul des opérations booléennes entre 2 listes d'intervalles ordonnees en 1D
# un intervalle est une paire (t1: un nombre, t2: un nombre)
# quand vos operations booleennes fonctionneront,
# changez t1 et t2 en deux contacts. Il y a un champ t dans le contact

#rend le t d'un contact, que le contact soit un nombre ou un Contact :
def tof( contact):
	if is_num( contact) : 
		return contact
	else:
		return contact.t



#pour supprimer les intervalles: (a1,a1) : purge1D( intervalles)

#pour fusionner des intervalles contigus : [a1, a2], [a3==a2, a4] en [a1, a4]
#def merge1D( intervalles):

#def simplify( intervalles) combine purge1D et merge1D


'''
def simplify1D(a):  #fonction ajouter
    if None == a:
        return None
    else:
        ((a1,a2), qa) = (hd(a), tl(a))
        if qa == None:
            if tof(a2) == tof(a1):
                return None
            else:
                return cons((a1,a2),qa) 
        else:
            ((b1,b2), qb) = (hd(qa), tl(qa))    
            if tof(a2) >= tof(b1):
                return  simplify1D(cons((a1,b2),qb))
            elif tof(a1) == tof(a2):
                return simplify1D(qa)
            else:
                return cons((a1,a2), simplify1D(qa))'''







# a et b sont 2 listes d'intervalles
# on calcule leur intersection: une liste d'intervalles
# inter(a, b)==inter(b, a)


def inter( a, b):
	if None==a or None==b :
		return None
	else:
		((a1,a2), qa) = (hd(a), tl(a))
		((b1,b2), qb) = (hd(b), tl(b))
		assert( tof( a1) <= tof( a2))
		assert( tof( b1) <= tof( b2))
		if tof( a1) > tof( b1) :
			return inter( b, a)
		elif tof( a2) < tof( b1) :
			return inter( qa, b)
		elif tof( b2) <= tof( a2) :
			return cons( (b1, b2), inter( a, qb))
		else:
			return cons( (b1, a2), inter( qa, b))
            
            

def inter1D( a, b):
	return simplify1D(  inter( a, b))
    
    
    
    

#def union1D( a, b): A ECRIRE

'''def union(a, b):   #fonction ajouter

    if a is None:
        return b
    elif b is None:
        return a
    else:
        ((ta,qa), qa) = (hd(a), tl(a))
        ((ta,qb), qb) = (hd(b), tl(b))
        (a1,a2) = ta
        (b1,b2) = tb
        assert( a1 <= a2 )
        assert( b1 <= b2)
        if (a1 > b1):
            return union(b,a)
        elif (a2 < b1):
            return (ta,union(tb, ( union(t1(a), t1(b)))))
        elif union((a1, a2), (union(t)(a), t1(b)))
            return reunion(a,qb)
        else:
            return union((a1,b2), union(t1(a), t1(B)))

def union1D( a, b):
	return simplify1D(  union( a, b))'''





'''
#def differ1D( a, b) : A ECRIRE


def differ(a, b):  #fonction ajouter
    if None == a:
        return None
    elif None==B:
        return a
    else:
        (ta,qa) = (hd(a), tl(a))
        (ta,qb) = (hd(b), tl(b))
        (a1,a2) = ta
        (b1,b2) = tb
        assert( a1 <= a2)
        assert( b1 <= b2)
        
        if (b2 <= a1):
            return differ(a,t1(b))
            
        elif (a2 < b1):
            return ta, differ(t1(a),b)
            
        elif b1 <= a1:
             if b2 <=a2:
                return differ(((b2, a2), t1(a), t1(b))
                
             else:
                return differ(t1(a), b)
                
        elif a2 <=b2:
             return (a1,b1), differ(t1(a),b)
             
        else:
            return ((a1,b1), differ(((b2,a2),t1(a)), t1(b)))
            

def differ1D( a, b):
	return simplify1D(  differ( a, b))'''











'''
	tester sur des exemples + simples !!
	écrit:
	-a ((0, 1), ((4, 6), ((20, 24), ((36, inf), None))))
	-b ((0, 2), ((7, 10), ((14, 16), ((22, 23), ((40, 50), ((100, inf), None))))))
	a union b ((1, 22), ((23, 40), ((50, 100), None)))
	a inter b= ((2, 4), ((6, 7), ((10, 14), ((16, 20), ((24, 36), None)))))
	a - b ((1, 2), ((7, 10), ((14, 16), None)))

	a=vtol( [(1, 4), (6, 20), (24, 36)])
	b=vtol( [(2, 7), (10, 14), (16, 22), (23, 40), (50, 100)])
	print( "-a", oppose1D( a))
	print( "-b", oppose1D( b))
	print( "a union b", union1D( a, b))
	print( "a inter b=", inter1D( a, b))
	print( "a - b", differ1D( a, b))
'''
