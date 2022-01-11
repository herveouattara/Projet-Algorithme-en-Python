# coding=utf-8
from util import *

# produit de 2 polynomes uni-varies
def mult( a, b):
	if 0==len(a) or 0==len(b):
		return []
	else:
		dA= len(a) - 1
		dB= len(b) - 1
		return vecteur( dA+dB+1, \
			   (lambda d: sigma( max(0, d-dB), min( d, dA),  \
							 (lambda i: a[i]*b[d-i]))))

	'''
	#TEST
	#print( sigma( 1, 4,  (lambda i: i)))
	print( vecteur( 10, (lambda i: 10*i)))
	print( mult( [1, 2], [1, 2]))
	print( mult( [1, 2], [1, -2]))
	print( mult( [1, 2, 3], [1, 2, 3, 4, 5]))
	'''

# acces au coeff d'un polynome univarie represente par un vecteur
# si indice <0 ou trop grand, rend 0
def  get_coef( pol, i):
	if i < 0 or i >= len( pol):
		return 0
	else:
		return pol[i]

# produit de 2 polynomes uni-varies, representes par des vecteurs
def plus( a, b):
	return vecteur( max( len(a), len( b)), \
		   lambda i: get_coef( a, i) + get_coef( b, i))

# oppose d'un polynome uni-varie, represente par un vecteur
def opp( pol):
	return vecteur( len( pol), (lambda i: 0 - pol[i]))

# a - b avec a et b deux polynomes uni-varies, representes par des vecteurs
def moins( a, b):
	return plus( a, opp( b))

def milieux( polber):
	assert( 0 < len( polber)) 
	return vecteur( len(polber) - 1, \
			(lambda i : ((float( polber[i]) + float( polber[i+1]))) / 2. ))

def pyramide( liste):
	if None==liste:
		return []
	else:
		(t,q)=liste
		if 1==len( t):
			return ltov( reverse( liste))	
		else:
			return pyramide( (milieux( t), liste) )

def casteljau( polber):
	n= len( polber)
	couches= pyramide( cons( polber, None) )
	return (vecteur( n, (lambda i : couches[i][0])), \
		vecteur( n, (lambda i : couches[n-i-1][i])) )

#nb de facons de choisir k elements parmi n, ou coef binomial
def choice( k, n):
	if k < 0 or n < k :
		return 0
	elif 0==k:
		return 1
	elif k > n-k :
		return choice( n-k, n)
	else:
		return (choice( k-1, n) * (n-k+1)) / k  

def binomial( k, n):
	return float( choice( k, n))

# convertir polca dans la base canonique
def tobernstein( polca):
	n=len( polca)
	degre=n-1
	return vecteur( n, \
                (lambda i: \
		  sigma( 0, degre, \
                   (lambda k: binomial( k, i) / binomial( k, degre) * float( polca[k])))))

'''
	tobernstein( [10., 0., 0. ])
	tobernstein( [0., 10., 0. ])
	tobernstein( [0., 0., 10. ])
'''

def mintab( tab):
	assert( 0 < len( tab))
	mi=tab[0]
	for i in range( 0, len( tab)):
		mi=min( mi, tab[i])
	return mi

def maxtab( tab):
        assert( 0 < len( tab))
        ma=tab[0]
        for i in range( 0, len( tab)):
                ma= max( ma, tab[i])
        return ma

def inter_constant( epsilon, polca):
	assert( 1==len(polca))
	if polca[ 0] <= 0 :
		return cons( (epsilon, 1.), None)
	else:
		return None

def inter_lineaire( epsilon, polca):
	assert( 2==len(polca))
	a=polca[1]
	b=polca[0]
	if 0.==a :
		return inter_constant( epsilon,  [b] )
	else:
		y0=b 
		y1=a+b
		cas = y0 * y1
		if cas > 0 :
			if y0 <= 0. :
				return cons( (epsilon, 1.), None)
			else:
				return None
		else :			
			#il y a une racine:
			rac= (0.-b) / float(a)
			if y1 <= 0. :
				return cons( (rac, 1.), None)
			else:
				return cons( (epsilon, rac), None)

'''
polca est un polynome dans la base canonique
on retourne [0, 1] inter { x | polca(x) <= 0} : c'est une liste d'intervalles (un intervalle est une paire: (a: un nombre, b: un nombre >= a) tq polca est négatif dans ces intervalles)
'''

# kons est un cons special pour study_interval : 
# on fusionne le premier intervalle (t1, t2) et le suivant (t3, t4) dans la liste si t2==t3
def kons( t1t2, liste):
	(t1, t2)=t1t2
	if None==liste:
		return cons( (t1, t2), liste)
	else:
		((t3, t4), q) = (hd( liste), tl( liste))
		if t2==t3:
			return cons( (t1,t4), q)
		else:
			return cons( (t1, t2), liste)

def study_interval( epsilon, polbe, t1, t2, liste_a_droite) :
	(mi, ma)= (mintab( polbe), maxtab( polbe))
	if 0. < mi : # polynome > 0. donc vide
		return liste_a_droite
	elif ma <= 0. :
		return kons( (t1, t2), liste_a_droite) 
	else:
		dt = t2 - t1
		tm = (t1+t2)/2.
		if dt < epsilon :
			return kons( (t1, t2), liste_a_droite)
		(pol1, pol2)= casteljau( polbe)
		return study_interval( epsilon, pol1, t1, tm, \
			study_interval( epsilon, pol2, tm, t2, liste_a_droite))

# intervalle (t1, t2) dans [0, 1] --> (1/t2, 1/t1)
def inverse_interval( t1t2): 
	(t1,t2) = t1t2
	if 0.== t1:
		return (1./t2, 1e20)
	return (1./t2, 1./t1)
	
# inter_polca_01 rend une liste d'intervalle dans [0, 1] où polca est négatif :
def inter_polca_01( epsilon,  polca):
	#on elimine les coefficients nuls de bas degre
	polca= ltov( eteter( (lambda coeff: abs( coeff) >= 1e-6), vtol( polca)))
	n=len( polca)
	if 0==n : # polynome identiquement nul
		return cons( (epsilon, 1.), None)
	elif 1==n: # cas polynome constant
		return inter_constant( epsilon, polca)
	elif 2==n : # cas polynome degre 1: a*t+b
		return inter_lineaire( epsilon, polca)
	else:
		polbe= tobernstein( polca)
		ivals = study_interval( epsilon, polbe, 0., 1., None)
		return ivals

def inter_polca( epsilon,  polca):
	n=len( polca)
	polinv = [polca[n-i-1] for i in range( 0, n)]
	ivals=inter_polca_01( epsilon,  polinv)
	#les racines sont dans (0, 1), on les inverse :
	ivals = reverse( ivals) # car 1/x est decroissant
	return mymap( inverse_interval, ivals)

