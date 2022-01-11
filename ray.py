# coding=utf−8
# :set expandtab
# :set tabstop=4
import math
import random
from util import *
from polynom import *
from expr import * 
from geom import *
#import bool1D as Bool
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def vec2xyz( v ):
	assert( len( v) == 4 and v[3]==1)
	return (v[0], v[1], v[2])

def vec2abc( v ):
	assert( len( v) == 4 and v[3]==0)
	return (v[0], v[1], v[2])

def vec2abcd( v) :
	assert( len( v) == 4 )
	return (v[0], v[1], v[2], v[3])

def xyz2vec( pt ):
	(x, y, z) = pt
	return [x, y, z, 1]

def abc2vec( abc ):
	(a, b, c) = abc
	return [a, b, c, 0]

def abcd2vec( abcd):
	(a, b, c, d)=abcd
	return [a, b, c, d]

class Rayon( object):
	def __init__( self, source, dir):
		self.source=source
		self.dir=dir
	#source et dir sont 2 triplets de flottants
	# voir util.py

#Contact decrit un point d'intersection entre un rayon et un solide:
# il y a le t,  un pt: (x,y,z), un plan: (a,b,c,d), une couleur : int

class Contact( object):
	def __init__( self, t, pt, plan, color):
		self.t = t
		self.pt = pt
		self.plan = plan
		self.color = color

'''
class Clip( Contact):
	def __init__( self, t):
		self.t = t
		self.color = (0,0,0)

cmini= Clip( 0.)
cmaxi= Clip( 1e20)
'''
		

#trf est une Trfo, contact est un Contact
def transform_contact( trf, contact) :
	if is_num( contact):
		print('a nombre dans transform_contact=' + str( contact))
		return 1/0
	t_pt = vec2xyz( mat_vec( trf.direct, xyz2vec( contact.pt)))
	t_plan=vec2abcd( vec_mat( contact.plan, trf.inverse))
	return Contact( contact.t,  t_pt, t_plan, contact.color)
	
# Obj est la classe mere de tous les objets solides (=3D)
class Obj(object):
    def __init__( self):
       " "

class Camera( object):
	def __init__( self, o, ox, oy, oz, hsizeworld, hsizewin, soleil):
		self.o=o
		self.ox= ox #vers la droite du spectateur
		self.oy= oy #regard du spectateur
		self.oz= oz #vertical du spectateur
		self.hsizeworld=hsizeworld
		self.hsizewin=hsizewin
		self.soleil = normalize3( soleil)
		self.background=(100,100, 255)
		self.nom= "img"
	def generate_ray( self, x, z):
		(x0, y0, z0)= self.o
		kx = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(x))
		kz = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(z))
		return Rayon( (x0 + kx*self.ox[0] + kz*self.oz[0], 
                               y0 + kx*self.ox[1] + kz*self.oz[1], 
                               z0 + kx*self.ox[2] + kz*self.oz[2]), 
                               self.oy)  
	
'''
	def topolent( e):
		return e.topolent()
'''

def transform_ray( trf, rayon) :
	src = rayon.source
	dir = rayon.dir
	t_src = vec2xyz( mat_vec( trf.direct, xyz2vec( rayon.source )))
	t_dir = vec2abc( mat_vec( trf.direct, abc2vec( rayon.dir )))
	return Rayon( t_src, t_dir)

def transform_cam( trf, cam):
	o2= vec2xyz( mat_vec( trf.direct, xyz2vec( cam.o)))
	ox2= vec2abc( mat_vec( trf.direct, abc2vec( cam.ox)))
	oy2= vec2abc( mat_vec( trf.direct, abc2vec( cam.oy)))
	oz2= vec2abc( mat_vec( trf.direct, abc2vec( cam.oz)))
	return Camera( o2, ox2, oy2, oz2, cam.hsizeworld, cam.hsizewin, cam.soleil)

def pt_sur_rayon( rayon, t) :
	(x, y, z)= rayon.source
	(a, b, c)= rayon.dir
	return (x + t*a, y + t*b, z + t*c)
	
		
class Prim( Obj):
	def __init__( self, fonc_xyz, color):
		self.fonc=fonc_xyz
		self.color=color
	def normale( self, xyz):
		(x,y,z) = xyz
		fx=self.fonc.derivee("x") 
		fy=self.fonc.derivee("y") 
		fz=self.fonc.derivee("z") 
		dico={"x":x, "y":y, "z":z}
		(a,b,c)= ( fx.eval( dico), fy.eval( dico), fz.eval( dico))
		return normalize3( (a, b, c) )
	def creer_contact( self, rayon, t) :
		pt=pt_sur_rayon( rayon, t)
		abc=(a,b,c) = self.normale( pt)
		d= 0 - pscal3( pt, abc)
		plan= (a,b,c,d)
		return Contact( t, pt, plan, self.color)
	def two_contacts( self, rayon, t1t2):
			(t1, t2)= t1t2
			return (self.creer_contact( rayon, t1), \
				self.creer_contact( rayon, t2))
	def intersection( self, rayon):
		dico = { "x": Nb(rayon.source[0]) + Nb(rayon.dir[0])*Var("t"),
                         "y": Nb(rayon.source[1]) + Nb(rayon.dir[1])*Var("t"),
                         "z": Nb(rayon.source[2]) + Nb(rayon.dir[2])*Var("t")}
		expression_en_t=self.fonc.evalsymb( dico)
		pol_t = topolent( expression_en_t) 
		intervalles= inter_polca( 1e-4, pol_t)
		#intervalles= ... remplace: roots = racines( pol_t)
		intervals_contacts= mymap( (lambda t1t2: self.two_contacts( rayon, t1t2)), intervalles)
		return intervals_contacts	


def transform_interval( transfo, intervalle_contacts):
	(contact1, contact2) = intervalle_contacts
	return (transform_contact( transfo, contact1), \
		transform_contact( transfo, contact2))

class TransfObj( Obj):
	def __init__( self, transformation, obj):
		self.transfo=transformation
		self.obj=obj
	def intersection( self, rayon):
		rayon_aux = transform_ray( trf_inverse( self.transfo), rayon)
		# contacts_aux est une liste de paire de contacts:
		contacts_aux = self.obj.intersection( rayon_aux)
		contacts = mymap( (lambda ival: \
		   transform_interval( self.transfo, ival)), contacts_aux)
		return contacts
'''
class Union( Obj):
	def __init__( self, a, b) :
		self.a= a
		self.b= b
	def intersection( self, rayon):
		ia = self.a.intersection( rayon)
		ib = self.b.intersection( rayon)
		return Bool.union1D( ia, ib)

class Inter( Obj):
	def __init__( self, a, b) :
                self.a= a
                self.b= b
	def intersection( self, rayon):
		ia = self.a.intersection( rayon)
		if None==ia:
			return None
		else:
			ib = self.b.intersection( rayon)
			return Bool.inter1D( ia, ib)

class Differ( Obj):
	def __init__( self, a, b) :
		self.a= a
		self.b= b
	def intersection( self, rayon):
		ia = self.a.intersection( rayon)
		if None==ia:
			return None
		else:
			ib = self.b.intersection( rayon)
			return Bool.differ1D( ia, ib)
'''


# calcule la couleur du contact, en attenuant la color du contact en fonction
# de l'angle avec le soleil dans la camera cam
def rendering( cam, contact):
	if 1.0 == contact.t :
		#l'oeil est "dans la matiere", à l'intérieur d'une primitive
		(r,v,b)=contact.color
		return (r//2, v//2, b//2)
	(rr,vv,bb)= contact.color
	(rr,vv,bb)= (float(rr), float(vv), float(bb))
	(a,b,c,d) = contact.plan
# avec les soustractions, il peut arriver que le plan soit mal orienté, ie la normale ne pointe pas vers l'extérieur de l'objet
# si le point du contact est vu, alors pscal3( sa normale, cam.oy)<= 0  
	if pscal3( cam.oy, (a,b,c)) > 0. :
		(a,b,c,d) = (-a, -b, -c, -d)
	ps=pscal3( (a,b,c), cam.soleil)
	ps = clamp( -1., 1., ps)
	coef= interpole( -1., 0.5, 1., 1., ps)
	return (int(coef*rr), int(coef*vv), int(coef*bb))

def raycasting( cam, objet):
	img=Image.new("RGB", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255))
	for xpix in range( -cam.hsizewin, cam.hsizewin+1, 1):
		for zpix in range( -cam.hsizewin, cam.hsizewin+1, 1):
			rayon= cam.generate_ray( xpix, zpix)
			contacts = objet.intersection( rayon)
			if None==contacts:
				(r,v,b)= cam.background
			else:
				(contact1, contact2)=  hd(contacts) 
				if is_num( contact1):
					print( 'contact1 = nb '+str(contact1))
				(r, v, b) = rendering( cam, contact1) 
			img.putpixel( (xpix+cam.hsizewin, 2*cam.hsizewin-(zpix+cam.hsizewin)), (r,v,b))
	img.show()
	img.save( cam.nom + '.png')

#########################################
# ci dessous on definit qqs primitives 
#########################################


def boule( centre, r):
	(cx,cy,cz) = centre
	x=Var("x")
	y=Var("y")
	z=Var("z")
	return (x-Nb(cx))*(x-Nb(cx)) + (y-Nb(cy))*(y-Nb(cy)) + (z-Nb(cz))*(z-Nb(cz)) - Nb(r*r)

def tore( r, R):
	x=Var("x")
	y=Var("y")
	z=Var("z")
	tmp=x*x+y*y+z*z+Nb(R*R-r*r) 
	return tmp*tmp- Nb(4.*R*R)*(x*x+z*z)

def steiner2():
	x=Var("x")
	y=Var("y")
	z=Var("z")
	return (x * x * y * y - x * x * z * z + y * y * z * z - x * y * z)

def steiner4():
	x=Var("x")
	y=Var("y")
	z=Var("z")
	return y * y - Nb( 2.) * x * y * y - x * z * z + x * x * y * y + x * x * z * z - z * z * z * z


def hyperboloide_2nappes():
	x=Var("x")
	y=Var("y")
	z=Var("z")
	return Nb(0.) - (z * z - (x * x + y * y + Nb(0.1)))

def hyperboloide_1nappe():
	x=Var("x")
	y=Var("y")
	z=Var("z")
	return Nb(0.)-(z * z - (x * x + y * y - Nb(0.1)))

def roman():
	x=Var("x")
	y=Var("y")
	z=Var("z")
	return ( x * x * y * y + x * x * z * z + y * y * z * z - Nb(2.) *  x * y * z)


def demo():
	oeil=(0.001,-4.,0.003)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.nom="boule"
	raycasting( camera, Prim( boule( (0., 2., -0.5), 1.), (255,255,255)))

	camera.nom="tore"
	raycasting( camera, Prim( tore(0.45, 1.), (255,200, 255)))

	camera.hsizeworld=10.
	raycasting( camera, Prim( steiner2(), (255,200, 255)))

	camera.hsizeworld=1.5
	camera.nom="roman"
	raycasting( camera, Prim( roman(), (255,200, 255)))

	camera.nom="hyper1"
	raycasting( camera, Prim( hyperboloide_1nappe(), (255,200, 255)))

	camera.nom="hyper2"
	raycasting( camera, Prim( hyperboloide_2nappes(), (255,200, 255)))

	camera.nom="steiner2"
	raycasting( camera, Prim( steiner2(), (255,200, 255)))

	camera.nom="steiner4"
	raycasting( camera, Prim( steiner4(), (255,200, 255)))

def essai_scale():
	oeil=(0.001,-4.,0.003)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.nom="scaledtorus"
	raycasting( camera, TransfObj( trf_affinite( 0.5, 1., 1.), \
                               Prim( tore(0.45, 1.), (255,200, 255))))


def essai_rotaz():
	oeil=(0.001,-4.,0.003)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.nom="rotatedtorus"
	raycasting( camera, TransfObj( trf_rota_Oz( math.pi/3.), \
		Prim( boule(0.45, 1.), (255,200, 255))))
       # Prim( tore(0.45, 1.), (255,200, 255))))

def essai_trans():
	oeil=(0.001,-4.,0.003)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.nom="translatedtorus"
	raycasting( camera, TransfObj( trf_trans( 0.75, 0., 0.2), \
			       Prim( tore(0.45, 1.), (255,200, 255))))



def essai_tore():
	oeil=(0.001,-4.,0.003)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.nom="tore"
	raycasting( camera, Prim( tore( 0.4, 1), (255,200, 255)))

#essai_scale()
#essai_rotaz()
#essai_trans()

'''def essai_inter():
	oeil=(0.001,-4.,0.003)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.nom="inter"
	raycasting( camera, \
	Inter( Prim( boule( (-0.5,0.,0.), 1), (255,0,0)),
	       Prim( boule( (0.5, 0.,0.), 1), (0,255,255))))

def essai_union():
        oeil=(0.001,-4.,0.003)
        droite=  (1.,0.,0.)
        regard=  (0.,1.,0.)
        vertical=(0.,0.,1.)
        camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)))
        camera.nom="union"
        raycasting( camera, \
        Union( Prim( boule( (-0.5,0.,0.), 1), (255,0,0)),
               Prim( boule( (0.5, 0.,0.), 1), (0,255,255))))

def essai_differ():
        oeil=(0.001,-4.,0.003)
        droite=  (1.,0.,0.)
        regard=  (0.,1.,0.)
        vertical=(0.,0.,1.)
        camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)))
        camera.nom="differ"
        raycasting( camera, \
        Differ( Prim( boule( (-0.5,0.,0.), 1), (255,0,0)),
               Prim( boule( (0.5, 0.,0.), 1), (0,255,255))))'''

def essai_inside():
        oeil=(0,-1.6,0)
        droite=  (1.,0.,0.)
        regard=  (0.,1.,0.)
        vertical=(0.,0.,1.)
        camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)))
        camera.nom="inside"
        #raycasting( camera, Prim( tore( (0., 0.,0.), 1), (0,255,255)))
        raycasting( camera, Prim( roman(), (0,255,255)))

#essai_inter()
#essai_union()
#essai_differ()
essai_inside()

'''
oeil=(0,-1.3,0)
droite=  (1.,0.,0.)
regard=  (0.,1.,0.)
vertical=(0.,0.,1.)
camera=Camera( oeil, droite, regard, vertical, 1.5, 50, normalize3((0., -1., 2.)))
camera.nom="inside"
rayon= camera.generate_ray( 0, 0)
prim= Prim( boule( (0., 0.,0.), 1), (0,255,255))
iv=prim.intersection( rayon)
(c1,c2)= hd( iv)
'''
