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


'''def essai_differ():
        oeil=(0,-4.,0)
        droite=  (1.,0.,0.)
        regard=  (0.,1.,0.)
        vertical=(0.,0.,1.)
        camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)))
        camera.nom="differ"
        anim( camera,  \
		Differ( Prim( boule( (0,0.,0.), 1), (255,0,0)), \
                        Prim( boule( (0.5, 0.,0.), 1), (0,255,255))), \
			20, "IMG/test_differ")

essai_differ()'''




def essai_inside:
        oeil=(0,-1.6,0)
        droite=  (1.,0.,0.)
        regard=  (0.,1.,0.)
        vertical=(0.,0.,1.)
        camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)))
        camera.nom="ARCHI/archi"
        anim( camera, Prim( tore( (0., 0.,0.), 1), (255,255,255),20,"ARCHI/archi"))
        
essai_inside()     
        
      

