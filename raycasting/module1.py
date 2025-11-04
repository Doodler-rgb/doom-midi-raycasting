import math #pour les calculs
import pygame #pour le jeu
import sys #pour fermer le programme

# === Carte 5*5 avec murs colorés ===
carte = [
    "11111",
    "B000B", #chaque chiffre est a peu pres un cube de 2m
    "B000B",
    "B000B",
    "11111"
]

couleurs_murs = {
    '1': (180, 180, 180),  # Gris clair
    'A': (200, 50, 50),    # Rouge
    'B': (50, 50, 200),    # Bleu
}

# === Joueur ===
joueur_X = 2 #place les coordonnees initiales du joueur 
joueur_Y = 2
angle_central = 0  #Pour tourner l'angle_central de 180° il faut ajour=ter la valeur décimal de pi soit 3.14 et pour angle_central = 0  il regarde donc vers l'est de la map
vitesse = 0.05 #en avant
vitesse_rotation = math.radians(3) #l'angle avec lequel il tourne sur la gauche a chaque tick en radians
#math.radians(x) : x en degre obtient sa valeur en radians

# === Vision ===
champ_de_vision = math.radians(60) #donne l'angle de son champ de vision en radians (60 est en degres)
nombre_de_rayons = 200 #influe sur la transparence des murs
interval_entre_rayon = champ_de_vision / nombre_de_rayons #calcul de l'intervale entre chaque rayon

# === Pygame ===
pygame.init() #demarre pygame
screen_width = (640) #largeur de l'écran
screen_height = (480) #hauteur de l'écran
#plus ces deux valeurs sont petites plus les murs paraissent complet car la largeur des rayons est tjr la meme en pixels mais il y a moins de pixels a combler
#Si les valeurs sont trop petites les rayons se chevauchent et l'affichage est moins fluidde visuellement
screen = pygame.display.set_mode((screen_width, screen_height)) #creer une fenetre : c'est une surface sur laquelle on va afficher des choses
pygame.display.set_caption("Fausse 3D - Salle 5x5") #defini letexte afficher dans la barre de titre de la fenetre qui s'affiche

clock = pygame.time.Clock() #créer une horloge pygame afin de gérer le nombre de frame plus tard

def envoi_rayon(angle_rayon): #defini la fonction qui calcule la longueur de chaque rayon : c'est a dire la distance entre le joueur et le mur
    rayon_X = joueur_X #definie ici l'abscisse initiale du rayon en effet le rayon part du joueur
    rayon_Y = joueur_Y #definie ici l'ordonne initiale du rayon en effet le rayon part du joueur
    pas = 0.01 # cette variable gere la precision des rayon : en gros plus valeur est elevee moins la distance mesuree est precise on alors un mur en palier non lineaire car des nombreux rayons ont mesure la meme valeur
    #si pas est trop grand on a un effet de "sphere" et on n'arrive plus a s'imaginer la fausse 3d
    distance = 0 #definie la distance initiale : 0 car le rayon part du joueur

    while distance < 10: #distance doit etre inferieur a une distance aberante comme ca on evite les boucles infinies
        #Néanmoins si on met une condition trop petite on aura une vue limitee en distance et les murs apparaitraient au fur et a mesure lorsue nous nous rapprocherions : effet de "brouillard"
        rayon_X += math.cos(angle_rayon) * pas #calcul de la distance horizontale du rayon : au rayon precedent qui n'a rien atteint au ajoute la composante horizontale du pas (pas est colinéaire au rayon)
        rayon_Y += math.sin(angle_rayon) * pas #calcul de la distance verticale du rayon : au rayon precedent qui n'a rien atteint au ajoute la composante verticale du pas (pas est colinéaire au rayon)
        distance += pas 

        coord_X = int(rayon_X) #rayon_X est une valeur a virgule; int(..) converti cette valeur en entier en tronquant vers le nombre inférieur (vers zero); cela permet de trouver la case de la carte dans laquelle se trouve le rayon à ce moment-là.
        coord_Y = int(rayon_Y) #rayon_Y est une valeur a virgule; int(..) converti cette valeur en entier en tronquant vers le nombre inférieur (vers zero); cela permet de trouver la case de la carte dans laquelle se trouve le rayon à ce moment-là.

        if coord_X < 0 or coord_X >= len(carte[0]) or coord_Y < 0 or coord_Y >= len(carte): #vérifient si les coordonnées calculées sortent des limites de la carte, et dans ce cas, elles arrêtent la recherche du rayon.
            return float('inf'), '0' #renvoie : ne rien afficher

        case = carte[coord_Y][coord_X] #cette ligne permet de récupérer la valeur (ex : 1; A; B...) du mur dans la carte
        if case != '0': #vérifie que cette valeur est différente de 0; car sinon le rayon est dans le vide; il doit donc afficher du vide
            return distance, case #on renvoie la distance parcourue jusqu'à l'obstacle (distance) ainsi que le type d'obstacle rencontré (ex 1; B; A)

    return float('inf'), '0' # si distance est devenue supérieur à 10, on renvoie une distance infinie ("inf") ainsi qu'une case vide "0"


pistolet = pygame.image.load("pistolet.png").convert_alpha() #cette ligne charge l'image et "convert alpha" permet de conserver les zones transparentes de l'image


def afficher_pistolet(screen, image, offset_y=30): #screen est la taille de la fenetre pygame, image la taille de l'image, offset est le decallage vers le bas la valeur ici pour le moment est arbitraire et sans importance 
    screen_width, screen_height = screen.get_size() #recupere la hauteur et la largeur de la fenetre
    pw, ph = image.get_size() #recupere la hauteur et la largeur de l'image

    x = (screen_width - pw) // 2 #on centre l'image
    y = screen_height - ph + offset_y  # on centre l'image et on la décale vers le bas

    screen.blit(image, (x, y)) # on affiche l'image aux bonnes coordonnees


# === Boucle principale ===
while True:
    # === Événements ===
    for event in pygame.event.get(): #récupère tout ce que fait l’utilisateur (fermer la fenêtre, appuyer sur une touche, cliquer, etc.). "event": On boucle sur chaque événement de cette liste (défini après) pour le traiter un par un.
        if event.type == pygame.QUIT: #si on clique sur la fenêtre croix; ici c'est le seul événement "event" controlé
            pygame.quit() #ferme tous les éléments en lien avec pygame, cette ligne est très importante sans ca on ne peut pas fermer la fenêtre
            sys.exit() #arrête tous le programme python ( car sinon la boucle while true continuerait à être vrai, ce qui affiche donc une erreur )

    # === Touches pressées ===
    touches = pygame.key.get_pressed() #"pygame.key.get_pressed()" est tableau comportant chaque touche du clavier (ex K_LEFT est la flèche de gauche) associer à son état pressée (true) ou relachée (false)
    if touches[pygame.K_LEFT]: #vérifie si la flèche de gauche est pressée
        angle_central -= vitesse_rotation #on diminue la valeur de l'angle central, on change la direction dans laquelle on regarde. Et vitesse_rotation est la vitesse de rotation (en radians par frame).
    if touches[pygame.K_RIGHT]: #vérifie si la flèche de droite est pressé
        angle_central += vitesse_rotation #on augment la valeur de l'angle central, on change la direction dans laquelle on regarde. Et vitesse_rotation est la vitesse de rotation (en radians par frame).
    if touches[pygame.K_UP]: #vérifie si la flèche du haut est pressé
        joueur_X += math.cos(angle_central) * vitesse #on ajoute le déplacement sur l'axe des x
        #"vitesse" est la distance parcourue par frame
        joueur_Y += math.sin(angle_central) * vitesse #on ajoute le déplacement sur l'axe des y
    if touches[pygame.K_DOWN]: #vérifie si la flèche du bas est pressé
        joueur_X -= math.cos(angle_central) * vitesse #on soustrait le déplacement sur l'axe des x
        #"vitesse" est la distance parcourue par frame
        joueur_Y -= math.sin(angle_central) * vitesse #on soustrait le déplacement sur l'axe des y

    # === Rendu ===
    screen.fill((0, 0, 0)) #"screen" on travaille sur la fenêtre ouvert en haut, "fill" on remplie la fenêtre d'une certaine couleur, "(0;0;0)" on remplie la fenêtre de noir, en gros en s'assure de nettoyer la fenêtre
    #cette action n'est pas nécessaire mais évite les bugs

    # Dessiner le plafond (haut)
    pygame.draw.rect(screen, (100, 100, 255), (0, 0, screen_width, screen_height // 2)) #on dessine un rectangle; "screen" on le dessine sur la fenêtre screen, (100, 100, 250) est la couleur bleu clair,
            #"(0,0) sont les coordonnées x et y en haut a gauche du rectangle; "screen_width" est la largeur du rectangle, ici la largueur de la fenêtre
            #enfin  "screen_height // 2"  est la hauteur, ici la moitié de la hauteur de la fenêtre
    # Dessiner le sol (bas)
    pygame.draw.rect(screen, (50, 30, 10), (0, screen_height // 2, screen_width, screen_height // 2))#on dessine un rectangle; "screen" on le dessine sur la fenêtre screen, (50, 30, 10) est la couleur marron sombre,
            #"(0, screen_height // 2) sont les coordonnées x et y en haut a gauche du rectangle, ici le rectangle est dans la moitié inférieur de la fenêtre;
            #"screen_width" est la largeur du rectangle, ici la largueur de la fenêtre
            #enfin  "screen_height // 2"  est la hauteur, ici la moitié de la hauteur de la fenê

    angle_de_depart = angle_central - (champ_de_vision / 2) #a l'instant t calcul l'angle en radian du rayon le plus à gauche du champ de vision

    for i in range(nombre_de_rayons): #on va diviser le champ de vision en rayons, ainsi on doit répéter le calcul puis l'affiche d'un rayon, autant de fois qu'il y a de raypn
        angle_rayon = angle_de_depart + i * interval_entre_rayon #on calcul ici l'angle que l'on s'apprête à afficher dans l' "action" en cours. Cela permet de balayer le champ de vision avec des rayons régulièrement écartés
        distance, type_mur = envoi_rayon(angle_rayon) #on applique la fonction envoi_rayon précédemment définie puis on récupère les deux valeurs qui sont renvoyées

        # Correction du fisheye
        corrected_distance = distance * math.cos(angle_rayon - angle_central)
        #Sans correction, les murs sur les côtés du champ de vision apparaissent étirés ou incurvés,
        #car les rayons qui vont sur les bords parcourent des distances plus longue car ils partent du sujet,
        #or tous les rayons doivent être colinéaire sur une  mème ligne et non partir du sujet
        #on corrige donc la distance des rayons en ne guardant que la composante "qui est parallèle au rayon centrale
        #cf https://gamedev.stackexchange.com/questions/97574/how-can-i-fix-the-fisheye-distortion-in-my-raycast-renderer


        if not math.isfinite(corrected_distance) or corrected_distance <= 0: #"not math.isfinite" renvoie vraie si la valeur est infini
            continue #si la distance est une distance invalide (trop grande ou inférieur à zéro alors on ignore la valeur et on continue

        wall_height = screen_height / corrected_distance #calcul de la hauteur du mur
        wall_height = min(screen_height, wall_height) #On s’assure que la hauteur du mur ne dépasse pas la hauteur totale de l’écran. car sin on serait trop proche il pourrait y avoir des problèmes d'affichage

        x = int(i * (screen_width / nombre_de_rayons)) #calcul la coordonnée x du rayon ( i étant l'indice du rayon, que l'on multiplie par la largueur d'un rayon
        y1 = int((screen_height / 2) - (wall_height / 2)) #on calcul ici la coordonnée y du haut du mur : on part de la coordonnée du milieu de l'écran puis on soustrait la moitié de la hauteur du mur
        y2 = int((screen_height / 2) + (wall_height / 2)) #on calcul ici la coordonnée y du bas du mur : on part de la coordonnée du milieu de l'écran puis on ajoute la moitié de la hauteur du mur #ne marche pas si on s'amuse a changer les valeurs

        # Couleur du mur selon son type
        couleur = couleurs_murs.get(type_mur, (255, 255, 255))  # On recupere ici la couleur du mur, si on a aucune valeur on evite les erreurs en ajoutant une valeur par defaut soit le blanc (255, 255, 255)

        # Effet d’ombre selon distance
        facteur = 255 / (1 + corrected_distance ** 2 * 0.0002) #plus on est proche, plus la valeur est tres proche de 255 donc de la couleur de base (grace on rapport futur), la couleur est donc clair car inchangee 
        facteur = max(0, min(255, facteur)) #on elimine les valeurs aberantes
        ombre = tuple(int(c * facteur / 255) for c in couleur) # la fonction tuple permet de travailler sur les trois composantes de la couleur avec une seule variable 
        #en fonction de l'eloignement ou non du rayon on assombris les couleurs du mur 

        pygame.draw.line(screen, ombre, (x, y1), (x, y2)) # on dessine ici une ligne qui correspond au rayon du mur, screen est la zone de dessin, et ombre est la couleur finale du mur 

    afficher_pistolet(screen, pistolet, offset_y=30) # on affiche le pistolet (fonction expliquee prededemment) 30 est choisi de maniere empirique 



    pygame.display.flip() #met a jour l'affichage de l'ecran
    clock.tick(60) #limite le jeu a 60 images par seconde, fonction d'attente de 1/60 de seconde


