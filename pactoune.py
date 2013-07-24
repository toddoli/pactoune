#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################
# MY GAME
####################################################################

#import de fonctions externes
import pygame, threading
from pygame.locals import *

from classes import *
from constantes import *

#Variables
continue_menu 	= True
continue_game 	= False
mechants	= []	#Liste des mechants
rect_list 	= []	#Liste des rectangles à afficher


#Initialisation de pygame
pygame.init()

#Initialisation des Paramètres
fenetre = 	pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.key.set_repeat(pause_before_key_repeat,key_repeat_time)

#Ouverture des images
image_title = 		pygame.image.load("images/title.png").convert()
fond = 			pygame.image.load("images/ingame.png").convert()
pitoune = 		pygame.image.load("images/pitoune.png").convert_alpha()
#Sprites des 4 monstres de couleur
monsters_sprites = 	[]
monsters_sprites.append(("images/monster_open_orange.png","images/monster_closed_orange.png"))
monsters_sprites.append(("images/monster_open_green.png","images/monster_closed_green.png"))
monsters_sprites.append(("images/monster_open_blue.png","images/monster_closed_blue.png"))
monsters_sprites.append(("images/monster_open_pink.png","images/monster_closed_pink.png"))	

music_loaded = 1

#Initialisation du son
gagner = pygame.mixer.Sound(son_gagner)

#Demarrage du menu
while continue_menu:
	fenetre.blit(image_title, (0,0))
	pygame.display.update(image_title.get_rect())
	
	#on réinitialise la liste de méchants
	mechants = []

	#Chargement de la musique
	if music_loaded and music_on:
		pygame.mixer.music.load(song)
		pygame.mixer.music.play()
		music_loaded = 	False

	for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
		if event.type == KEYDOWN :
			if event.key == K_RETURN:     #Si ENTER, on démarre le jeu
				"""Initialisation de la partie"""
				continue_game = True
				#Génération d'un niveau à partir d'un fichier
				niveau = Niveau(choix_niveau)
				niveau.generer()
				niveau.calc_nb_pitoune()
				niveau.afficher(fenetre)
				#Génération de PacToune
				pactoune = Perso("images/pacman_open_right.png", "images/pacman_closed_right.png", "images/pacman_open_left.png", "images/pacman_closed_left.png", "images/pacman_open_up.png", "images/pacman_closed_up.png", "images/pacman_open_down.png", "images/pacman_closed_down.png", niveau, 'gentil')				
				for i in  range(0,4) :			
					mechants.append(Perso(monsters_sprites[i][0], monsters_sprites[i][1], monsters_sprites[i][0], monsters_sprites[i][1], monsters_sprites[i][0], monsters_sprites[i][1], monsters_sprites[i][0], monsters_sprites[i][1], niveau, 'mechant'))
				#Affichage des personnages
				fenetre.blit(pactoune.direction, (pactoune.x,pactoune.y))
				niveau.replace(pactoune.case_x,pactoune.case_y,'x')
				for mechant in mechants :
					fenetre.blit(mechant.direction, (mechant.x,mechant.y))
					niveau.replace(mechant.case_x,mechant.case_y,'x')
				pygame.display.update(Rect(0,0,1024,768))

			elif event.key == K_ESCAPE:     #Si un de ces événements est de type QUIT
				continue_menu = False
				continue_game = False

		#Début de la partie
		while continue_game:

			#Limitation de la vitesse du Jeu
			pygame.time.Clock().tick(tick_speed)
			rect_list = []
			
			if niveau.moved_once : #Si on a commencé à bouger on lance les monstres
				""" ANIMATION DES MONSTRES """
				#On enregistre les rectangles à supprimer
				for mechant in mechants :
					rect_list.append(Rect(mechant.x,mechant.y,taille_sprite,taille_sprite))
					#On efface le mechant et on reblit soit un pitoune soit rien
					if niveau.structure[mechant.case_y][mechant.case_x] == '0' :
						fenetre.blit(fond, (mechant.x,mechant.y), Rect(mechant.x,mechant.y,taille_sprite,taille_sprite))
						fenetre.blit(pitoune, (mechant.x,mechant.y))
					else :
						fenetre.blit(fond, (mechant.x,mechant.y), Rect(mechant.x,mechant.y,taille_sprite,taille_sprite))
					#On déplace le monstre par rapport au pactoune et on perd si on se fait manger
					if mechant.deplacement_auto(pactoune.case_x,pactoune.case_y) :
						continue_game = False
					#On affiche les monstres à leur nouvelle position
					fenetre.blit(mechant.direction, (mechant.x,mechant.y))
					rect_list.append(Rect(mechant.x,mechant.y,taille_sprite,taille_sprite))

			#On parcours la liste de tous les événements reçus
			for event in pygame.event.get():   

				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continue_game = False      #On arrête la boucle

				elif event.type == KEYDOWN :  #Si on appuie sur une touche
					if event.key == K_ESCAPE :	#Si ECHAP
						continue_game = False			
					if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT :
						""" ANIMATION DU PACTOUNE """
						#On efface l'image présente du personnage	
						fenetre.blit(fond, (pactoune.x,pactoune.y), Rect(pactoune.x,pactoune.y,taille_sprite,taille_sprite))
						rect_list.append(Rect(pactoune.x,pactoune.y,taille_sprite,taille_sprite))
						if event.key == K_UP :
							pactoune.deplacer('haut')
						elif event.key == K_DOWN :
							pactoune.deplacer('bas')
						elif event.key == K_LEFT :
							pactoune.deplacer('gauche')
						elif event.key == K_RIGHT :
							pactoune.deplacer('droite')
						#On affiche le perso a la nouvelle position
						fenetre.blit(pactoune.direction, (pactoune.x,pactoune.y))
						rect_list.append(Rect(pactoune.x,pactoune.y,taille_sprite,taille_sprite))
				
					if niveau.nb_pitoune == 0 :
						gagner.play()
						continue_game = False
			#On met à jour l'affichage à chaque rectangle de rect_list
			pygame.display.update(rect_list)

