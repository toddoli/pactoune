#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################
# Constantes
####################################################################


#Paramètres de la fenêtre
largeur_fenetre = 			1024
hauteur_fenetre = 			768
taille_sprite = 			32
 
#Personnalisation de la fenêtre
titre_fenetre = 			"PacToune"
#image_icone = "images/dk_droite.png"
 
#Listes des images du jeu
image_accueil = 			"images/accueil.png"
image_fond = 				"images/fond.jpg"
image_mur = 				"images/mur.png"
image_depart = 				"images/depart.png"
image_arrivee = 			"images/arrivee.png"

#Playlist
song = 					"sounds/Fabien Cambi - Fractal Church.ogg"

#Sons
son_manger = 				"sounds/wot.ogg"
son_gagner = 				"sounds/woohoo.ogg"
son_perdu = 				"sounds/oh_non.ogg"

#Paramètres du jeu
music_on =				True
pause_before_key_repeat = 		1
key_repeat_time = 			10
vitesse = 				32 	                #en pixels
tick_speed = 				60
level = 				3	                #niveau de difficulté
choix_niveau = 				'levels/lvl1'
delta =                                 taille_sprite/vitesse   #nombre de déplacements possible dans un sprite
largeur_movesGrid=                      largeur_fenetre/vitesse
hauteur_movesGrid=                      hauteur_fenetre/vitesse
