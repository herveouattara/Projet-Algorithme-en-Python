#object_name = Roman/roman.split('/')[0]

#if not os.path.exits('./'+object_name):
#os.makedirs(object_name)

# coding=utf-8

from ray import *
import math
pi = 4. * math.atan(1.)
#math.pi

def rotaz( pt, theta):
	c= math.cos( theta)
	s= math.sin( theta)
	(x, y, z) = pt
	x2= c*x - s*y
	y2= s*x + c*y
	z2= z
	return (x2,y2,z2)

def string_of_int( n, nbch):
	tabstr=[0]*nbch
	for i in range( nbch-1, -1, -1) :
		tabstr[i] = n % 10
		n = n // 10
	ch=""
	for i in range( 0, nbch):
		ch = ch + str( tabstr[i])  # ch += str( tabstr[i])
	return ch

def anim( cam, obj, nb, nom):
	for i in range( 0, nb):
		theta= 2. * pi * float( i) / float( nb)
		o2 = rotaz( cam.o, theta)
		ox2 = rotaz( cam.ox, theta)		
		oy2 = rotaz( cam.oy, theta)		
		oz2 = rotaz( cam.oz, theta)		
		cam2 = Camera( o2, ox2, oy2, oz2, cam.hsizeworld, cam.hsizewin, cam.soleil)
		nom2 = nom + string_of_int( i, 10)
		cam2.nom = nom2
		raycasting( cam2, obj)

def tester_anim():
	oeil=(0.0011,-4.001,0.003)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.nom="IMG/roue"
    
	#anim( camera, Prim( tore(0.45, 1.), (255,255,255)), 15, "IMG/roue")
	anim( camera, Prim( roman(), (255,255, 0)), 20, "ROMAN/roman")


tester_anim()
