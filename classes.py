#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################
# Classes
####################################################################

import pygame, random
from pygame.locals import *
from constantes import *
 
class Niveau:
    """Classe permettant de créer un niveau"""
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0
	self.nb_pitoune = 0
	self.case_depart = []
	self.case_depart_mechant = []
	self.moved_once = False
        self.movesGrid = []
     
    def generer(self):
        """Méthode permettant de générer le niveau en fonction du fichier.
        On crée une liste générale, contenant une liste par ligne à afficher"""
        #On ouvre le fichier
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            #On parcourt les lignes du fichier
            for ligne in fichier:
                ligne_niveau = []
                #On parcourt les sprites (lettres) contenus dans le fichier
                for sprite in ligne:
                    #On ignore les "\n" de fin de ligne
                    if sprite != '\n':
                        #On ajoute le sprite à la liste de la ligne
                        ligne_niveau.append(sprite)
                #On ajoute la ligne à la liste du niveau
                structure_niveau.append(ligne_niveau)
            #On sauvegarde cette structure
            self.structure = structure_niveau
     
        #On génère une movesGrid vide
        for i in range(hauteur_movesGrid):
            self.movesGrid.append([0] * largeur_movesGrid)
     
    def afficher(self, fenetre):
        """Méthode permettant d'afficher le niveau en fonction 
        de la liste de structure renvoyée par generer()"""
        up_left_corner = pygame.image.load("images/up_left_corner.png").convert_alpha()
	up_right_corner = pygame.image.load("images/up_right_corner.png").convert_alpha()
	down_left_corner = pygame.image.load("images/down_left_corner.png").convert_alpha()
	down_right_corner = pygame.image.load("images/down_right_corner.png").convert_alpha()
	vline = pygame.image.load("images/vline.png").convert_alpha()
	hline = pygame.image.load("images/hline.png").convert_alpha()
	pitoune = pygame.image.load("images/pitoune.png").convert_alpha()
	fond = pygame.image.load("images/ingame.png").convert()
        
	#On affiche le fond
	fenetre.blit(fond, (0,0))

        #On parcourt la liste du niveau
        num_ligne = 0
        for ligne in self.structure:
            #On parcourt les listes de lignes
            num_case = 0
            for sprite in ligne:
                
                #On calcule la position réelle en pixels
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite
                if sprite == 'q' or sprite == '-' or sprite == 'e' or sprite == '|' or sprite == 'z' or sprite == 'c' : #espace non jouable
                
                    #Etablissement d'une matrice de zones jouables (espaces) ou non (murs), relatifs à la vitesse de déplacement.
                    #1 = occupé / 0 = libre
                    for i in range(delta) :
                        for j in range(delta) :
                            index_ligne = num_ligne*delta + i
                            index_case = num_case*delta + j
                            self.movesGrid[index_ligne][index_case] = 1 # espace occupé par un mur
                    if sprite == 'q':          #q = Coin haut gauche
			fenetre.blit(up_left_corner, (x,y))
                    elif sprite == '-':        #- = Ligne horizontale
			fenetre.blit(hline, (x,y))
                    elif sprite == 'e':        #e = Coin haut droit
			fenetre.blit(up_right_corner, (x,y))
                    elif sprite == '|':        #| = Ligne Verticale
			fenetre.blit(vline, (x,y))
                    elif sprite == 'z':        #z = Coin bas gauche
                        fenetre.blit(down_left_corner, (x,y))
                    elif sprite == 'c':        #c = Coin bas droit
                        fenetre.blit(down_right_corner, (x,y))
               
                else : # Espace jouable ( la matrice movesGrid est déjà à 0 donc rien à y faire ici )
                    
                    if sprite == '0':        #0 = pitoune
			fenetre.blit(pitoune, (x,y))
                    elif sprite == 'P':        #P = Depart_Perso
			self.case_depart = (num_case,num_ligne)
                    elif sprite == 'B':        #B = Méchants
			self.case_depart_mechant.append((num_case,num_ligne))
                num_case += 1
            num_ligne += 1
            
    def replace(self, case_x, case_y, value):
        """Méthode permettant de modifier le contenu d'une case"""
        self.structure[case_y][case_x] = value

    def calc_nb_pitoune(self):
        """Méthode permettant de calculer le nombre de pitounes du niveau"""
        for ligne in self.structure:
            #On parcourt les listes de lignes
            for sprite in ligne:
                #On calcule la position réelle en pixels
                if sprite == '0' :
			self.nb_pitoune += 1			

class Perso:

	"""Classe permettant de créer un personnage"""
	def __init__(self, droite_open, droite_closed, gauche_open, gauche_closed, haut_open, haut_closed, bas_open, bas_closed, niveau, genre):
		#Sprites du personnage
		self.droite_open = pygame.image.load(droite_open).convert_alpha()
		self.droite_closed = pygame.image.load(droite_closed).convert_alpha()
		self.gauche_open = pygame.image.load(gauche_open).convert_alpha()
		self.gauche_closed = pygame.image.load(gauche_closed).convert_alpha()
		self.haut_open = pygame.image.load(haut_open).convert_alpha()
		self.haut_closed = pygame.image.load(haut_closed).convert_alpha()
		self.bas_open = pygame.image.load(bas_open).convert_alpha()
		self.bas_closed = pygame.image.load(bas_closed).convert_alpha()
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau
		#Type de personnage (mechant ou gentil)
		self.genre = genre
		#Position du personnage par défaut
		if genre == 'gentil' :
			self.case_x = self.niveau.case_depart[0]
			self.case_y = self.niveau.case_depart[1]
		elif genre == 'mechant' :
			self.case_x = self.niveau.case_depart_mechant[0][0]
			self.case_y = self.niveau.case_depart_mechant[0][1]
			del self.niveau.case_depart_mechant[0]
		self.x = self.case_x * taille_sprite
		self.y = self.case_y * taille_sprite
		#Direction et self.is_openure par défaut
		if genre == 'gentil' :
			self.direction = self.droite_open
		elif genre == 'mechant' :
			self.direction = random.choice([self.haut_open,self.bas_open,self.gauche_open,self.droite_open])
     
	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""	

		#Flag du 1er deplacement
		self.niveau.moved_once = True
                
		#Calcul du déplacement en fonction de la direction
		deplacement = self.str2deplacement(direction)
                
                #On récupère les infos pour tester la prochaine case
                next_case = self.get_next_case(direction,deplacement)
                next_y1 = next_case['next_y1']
                next_x1 =  next_case['next_x1']
                next_y2 = next_case['next_y2']
                next_x2 = next_case['next_x2']
                #On vérifie que la destination n'est pas un mur
                if self.niveau.movesGrid[next_y1][next_x1] == 0 and  self.niveau.movesGrid[next_y2][next_x2] == 0 :
                    #Déplacement
                    self.x += deplacement[0]
                    self.y += deplacement[1]
                    #Calcul de la case actuelle
                    self.case_x = self.x / taille_sprite
                    self.case_y = self.y / taille_sprite
                    
                    if self.niveau.structure[self.case_y][self.case_x] == '0' : #Si pitoune alors manger
                        manger = pygame.mixer.Sound(son_manger)
                        self.niveau.structure[self.case_y][self.case_x] = 'x'
                        self.niveau.nb_pitoune += -1
                        manger.play()
                        
        def deplacement_auto(self, px, py):
            """Methode permettant de déplacer les mechants de manière aléatoire"""	
            
            #case du monstre
            mx = self.case_x
            my = self.case_y
            ok = False
            
	    #Calcul de la distance du Pactoune par rapport au monstre
            distance_x = px - mx
            distance_y = py - my
            
	    #Le monstre va prendre la direction de Pactoune s'il est proche en fonction de la difficulté "level"
            if ( distance_x <= level and distance_x >= 0 and distance_y==0) : #Pactoune est proche à droite
                deplacement = (vitesse,0)
                
            elif ( distance_x >= -level and distance_x <= 0  and distance_y==0) : #Pactoune est proche à gauche
                deplacement = (-vitesse,0)
                
            elif ( distance_y <= level and distance_y >= 0  and distance_x==0) : #Pactoune est proche en bas
                deplacement = (0,vitesse)
                
            elif ( distance_y >= -level and distance_y <= 0  and distance_x==0) : #Pactoune est proche en haut
                deplacement = (0,-vitesse)
                
            else : #Calcul du déplacement
                deplacement = self.calcul_deplacement()		#deplacement(x,y) avec x: nb de pixels horizontaux et y: nb de pixels verticaux
            
            #On récupère les infos pour tester la prochaine case
            next_case = self.get_next_case(self.direction2str(),deplacement)
            next_y1 = next_case['next_y1']
            next_x1 = next_case['next_x1']
            next_y2 = next_case['next_y2']
            next_x2 = next_case['next_x2']
            
            if self.niveau.movesGrid[next_y1][next_x1] == 0 and  self.niveau.movesGrid[next_y2][next_x2] == 0 :                
                       #Déplacement
                self.x += deplacement[0]
                self.y += deplacement[1]
                
                    #Calcul de la position en case
                self.case_x = self.x / taille_sprite
                self.case_y = self.y / taille_sprite
                
            else :		#Si impossible de se séplacer on change de direction
                
                    #choix aléatoire binaire				
                true = random.choice([True,False])
                if deplacement[0] == 0 : #Si je me suis déplacé à la verticale
                    if true :
                        deplacement = (-vitesse,0) #Soit gauche
						#Image dans la bonne direction
                        if self.direction == self.haut_closed or self.direction == self.bas_closed :
                            self.direction = self.gauche_open
                        elif self.direction == self.haut_open or self.direction == self.bas_open :
                            self.direction = self.gauche_closed
                    else :
                        deplacement = (vitesse,0) #Soit droite
                        if self.direction == self.haut_closed or self.direction == self.bas_closed :
                            self.direction = self.droite_open
                        elif self.direction == self.haut_open or self.direction == self.bas_open :
                            self.direction = self.droite_closed
                                
                else :	#Sinon, je me suis déplacé à l'horizontale
                    if true :
                        deplacement = (0,vitesse) #Soit bas
                        if self.direction == self.gauche_closed or self.direction == self.droite_closed :
                            self.direction = self.bas_open
                        elif self.direction == self.gauche_open or self.direction == self.droite_open :
                            self.direction = self.bas_closed
                    else :
                        deplacement = (0,-vitesse) #Soit haut
                        if self.direction == self.gauche_closed or self.direction == self.droite_closed :
                            self.direction = self.haut_open
                        elif self.direction == self.gauche_open or self.direction == self.droite_open :
                            self.direction = self.haut_closed

		#Si case pactoune = case monstre alors on perd
                if px == self.case_x and py == self.case_y : #Si pactoune est plus a droite
                    perdu = pygame.mixer.Sound(son_perdu)
                    perdu.play()
                    return True
		else :
                    return False

        def get_next_case(self, direction, deplacement) :
                """On calcule les bonnes limites à utiliser pour comparer les cases en prévision du déplacement"""
                if direction == 'gauche' :
                    next_y1 = (self.y + deplacement[1]) / vitesse
                    next_x1 = (self.x + deplacement[0]) / vitesse
                    next_y2 = next_y1 + delta -1
                    next_x2 = next_x1
                elif direction == 'droite' :
                    next_y1 = ((self.y + deplacement[1]) / vitesse ) 
                    next_x1 = ((self.x + deplacement[0] + taille_sprite - 1) / vitesse )
                    next_y2 = next_y1 + delta -1
                    next_x2 = next_x1
                elif direction == 'haut' :
                    next_y1 = (self.y + deplacement[1]) / vitesse
                    next_x1 = (self.x + deplacement[0]) / vitesse
                    next_y2 = next_y1
                    next_x2 = next_x1 + delta -1
                elif direction == 'bas' :
                    next_y1 = ((self.y + deplacement[1] + taille_sprite - 1) / vitesse )
                    next_x1 = ((self.x + deplacement[0]) / vitesse ) 
                    next_y2 = next_y1
                    next_x2 = next_x1 + delta -1
                return {'next_x1': next_x1,'next_y1': next_y1,'next_x2': next_x2,'next_y2': next_y2}

	def calcul_deplacement(self)  :
		"""Calcul du déplacement en fonction de la direction"""
		self.open_close_animation()
		if self.direction == self.droite_open or self.direction == self.droite_closed :
			return (vitesse,0)

		elif self.direction == self.gauche_open or self.direction == self.gauche_closed :
			return (-vitesse,0)

		elif self.direction == self.haut_open or self.direction == self.haut_closed :
			return (0,-vitesse)

		elif self.direction == self.bas_open or self.direction == self.bas_closed :
			return (0,vitesse)

	def str2deplacement(self, direction)  :
		"""Calcul du déplacement en fonction de la direction"""
		if direction == 'droite' :
			if self.direction == self.droite_closed or self.direction == self.gauche_closed or self.direction == self.bas_closed or self.direction == self.haut_closed :
				self.direction = self.droite_open
			else :
				self.direction = self.droite_closed
			return (vitesse,0)

		elif direction == 'gauche' :
			if self.direction == self.droite_closed or self.direction == self.gauche_closed or self.direction == self.bas_closed or self.direction == self.haut_closed :
				self.direction = self.gauche_open
			else :
				self.direction = self.gauche_closed
			return (-vitesse,0)

		elif direction == 'haut' :
			if self.direction == self.droite_closed or self.direction == self.gauche_closed or self.direction == self.bas_closed or self.direction == self.haut_closed :
				self.direction = self.haut_open
			else :
				self.direction = self.haut_closed
			return (0,-vitesse)

		elif direction == 'bas' :
			if self.direction == self.droite_closed or self.direction == self.gauche_closed or self.direction == self.bas_closed or self.direction == self.haut_closed :
				self.direction = self.bas_open
			else :
				self.direction = self.bas_closed
			return (0,vitesse)

        def direction2str(self)  :
		"""Calcul du déplacement en fonction de la direction"""
		if self.direction == self.haut_closed or self.direction == self.haut_open:
                    return 'haut'
                elif self.direction == self.bas_closed or self.direction == self.bas_open:
                    return 'bas'
                if self.direction == self.gauche_closed or self.direction == self.gauche_open:
                    return 'gauche'
                if self.direction == self.droite_closed or self.direction == self.droite_open:
                    return 'droite'

	def open_close_animation(self):
		"""Methode permettant de remettre le personnage dans la bonne direction et le faire s'animer"""	

		if self.direction == self.droite_open :
			self.direction = self.droite_closed

		elif self.direction == self.droite_closed:
			self.direction = self.droite_open

		elif self.direction == self.gauche_open :
			self.direction = self.gauche_closed

		elif self.direction == self.gauche_closed:
			self.direction = self.gauche_open

		elif self.direction == self.haut_open :
			self.direction = self.haut_closed

		elif self.direction == self.haut_closed:
			self.direction = self.haut_open

		elif self.direction == self.bas_open :
			self.direction = self.bas_closed

		elif self.direction == self.bas_closed:
			self.direction = self.bas_open
