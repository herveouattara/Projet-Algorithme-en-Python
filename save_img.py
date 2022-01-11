'''
pour les gens qui n'arrivent pas à installer pyx ou pillow
il est possible de calculer l'image, de la sauver dans une matrice de
(r, v, b)  et de la sauver sur disque au format .ppm
Ensuite il est possible de la convertir au format .png 50 fois + compact
puis de creer une animation à partir des fichiers .png

pour afficher l'image, vous pouvez lancer une commande en python:

import os
os.system('gnome-open roue0008.ppm') ou ce qui va bien sur votre machine
'''

# coding=utf−8

#sauve img[x][y] au format ppm:  portable picture format (image couleur)
def save_img( nom, img) :
        (xs, ys) = (len( img), len( img[0]))
        fichier=open(nom + '.ppm', "w")
        fichier.write('P3\n')
        fichier.write("# Le P3 signifie que les couleurs sont en ASCII, et qu'elles sont en RGB.")
        fichier.write( "# nb colonnes et nb lignes : \n")
        fichier.write( ' ' + str(xs) + ' ' + str(ys) + '\n')
        fichier.write( "# Ayant 255 pour valeur maximum : \n")
        fichier.write('255 \n')
        for y in range(ys-1, -1, -1):
                for x in range(0, xs) :
                        (r,v,b)=img[x][y]
                        # CHAQUE VALEUR DE r v b DOIT ETRE PRECEDEE 
			# ET SUIVIE D'UN ESPACE !!!
                        fichier.write( ' ' + str(r) + ' ' + str(v) + ' ' + str(b) + '\n')
        fichier.close()

