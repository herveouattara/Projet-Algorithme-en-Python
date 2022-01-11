
# coding=utf-8

from ray import *
import math
pi = 4. * math.atan(1.)
import ray
import anim

def cylindre_Oz( z0, z1, radius, coul):
	assert( z0 <= z1)
	x=Var('x')
	y=Var('y')
	z=Var('z')
	equation=x*x + y*y - Nb( radius*radius)
	return Inter( Prim( equation, coul), \
		Inter( Prim( z-Nb(z1), coul), Prim( Nb(z0)-z, coul)))

def cylindre_Ox( x0, x1, radius, coul):
	assert( x0 <= x1)
	x=Var('x')
	y=Var('y')
	z=Var('z')
	equation= y*y + z*z -Nb( radius*radius)
	return Inter( Prim( equation, coul), \
                Inter( Prim( x-Nb(x1), coul), Prim( Nb(x0)-x, coul)))

def cylindre_Oy( y0, y1, radius, coul):
        assert( y0 <= y1)
        x=Var('x')
        y=Var('y')
        z=Var('z')
        equation= x*x + z*z -Nb( radius*radius)
        return Inter( Prim( equation, coul), \
                Inter( Prim( y-Nb(y1), coul), Prim( Nb(y0)-y, coul)))


def bloc( x1x2, y1y2, z1z2, coul):
	(x1,x2)=x1x2
	(y1,y2)=y1y2
	(z1,z2)=z1z2
	x=Var('x')
	y=Var('y')
	z=Var('z')
	return  Inter( Prim( x-Nb(x2), coul),  \
		Inter( Prim( y-Nb(y2), coul),  \
		Inter( Prim( z-Nb(z2), coul),  \
		Inter( Prim( Nb(x1)-x, coul),  \
		Inter( Prim( Nb(y1)-y, coul),  \
		       Prim( Nb(z1)-z, coul))))))

def camera_std():
	oeil=(0.001,-2.001,0.001)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)))
	camera.nom="image"
	return camera

def voutes():
	maille=10.
	hsize=3*maille/2.
	radius=maille/2.
	epais=0.5
	gradius=radius+epais
	sradius=radius-epais
	coul=(255,255,0)
	hauteur=maille*1.414
	toit= Differ( \
                 Union( cylindre_Ox( -hsize-epais, hsize+epais, gradius, coul), \
			cylindre_Oy( -hsize-epais, hsize+epais, gradius, coul)), \
		 Union( bloc( (-1.2*hsize,1.2*hsize), (-1.2*hsize,1.2*hsize), (-1.2*hsize,0), coul), \
		 	Union( cylindre_Ox( -hsize-1, hsize+1, sradius, coul), \
			       cylindre_Oy( -hsize-1, hsize+1, sradius, coul))))
	poteau= cylindre_Oz( -hauteur, 0, epais, coul)
	delta= maille/2.
	poteau0= TransfObj( trf_trans( -delta, -delta, 0.), poteau)
	piles = None
	for xx in range(-1,3):
		for yy in range(-1,3):
			if (xx-0.5)*(xx-0.5) + (yy-0.5)*(yy-0.5) < 2.7:
				piles= cons( TransfObj( trf_trans( xx*maille, yy*maille, 0), poteau0), piles)
	les_piliers= foldl( (lambda accu, obj: Union( accu, obj)), hd( piles), tl( piles)) 
	archi= Union( toit, les_piliers)	
	archi= Union( archi, bloc( (-3.*maille,3.*maille), (-3.*maille,3.*maille), (-2*hauteur, -hauteur), (150, 75, 75)))
	return archi


camera= camera_std()
#camera.nom="cylindre_Oz"
#raycasting( camera, cylindre_Oz( 0, 1, 0.3, (255,255,2555)))
camera.nom="tmpimg"
camera.o=(0., -50., 0.)
camera.hsizeworld=25.
#raycasting( camera, bloc( (-0.2,0.2), (0,1), (-0.5, 0.75), (255,255,0)))
camera.hsizewin=100
#pour voir le dessus du toit :
camera=transform_cam( trf_rota_Ox( -math.pi/10.), camera)
nbimages=36
anim.anim( camera, voutes(), nbimages, "ARCHI/archi")
