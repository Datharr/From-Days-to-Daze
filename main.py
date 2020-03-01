import pygame
import os
import random
import time
from config import *                                              #Importation de tous les dossiers et des utilitaires
from init_card import *
from init_person import *

#Commentaire feature-mathieu
def display_text(win, text, positionX, positionY, size,R,G,B):    #Fonction texte
    font = pygame.font.SysFont("arial", size)                     #Police et taille
    font.set_bold(True)                                   
    text = font.render(text, True, (R, G, B), None)               #Couleur
    win.blit(text, (positionX, positionY))                        #Position du texte


def card_choice(cards_available):                                #Fonction choix des cartes          
    card1 = random.choice(cards_list)                            #Random sur card_list
    #print(card1)
    if card1["repetable"] == False:                              #Si la carte n'est pas répétable on la suprimme de cards_available (copie de cards_list qu'on peut modif)
        cards_available.remove(card1)                            #Supprime la carte 1 choisi
    card2 = random.choice(cards_list)         
    #print(card2)
    # while card2 == card1:
    #     card2 = random.choice(cards_list)
    if card2["repetable"] == False:                              #Si la carte n'est pas répétable on la suprimme de cards_available (copie de cards_list qu'on peut modif)
        cards_available.remove(card2)
    return card1, card2, cards_available                         #On retourne les valeurs choisi hors de la fonction


def display_card_in_system(cards):                                         #Fonction inutile qui affiche la liste des cartes entières en texte (useless)
    for a in cards:
        print("Action : " + a["name"] + " | Santé : " + str(a["health"]) + " | Nourriture : " + str(a["food"]) + " | Materiaux : " + str(a["materials"]) + " | Cohesion : " + str(a["relationship"]) + " | Puissance : " + str(a["power"]))
                                           


def wait_for_choice(card1_rect, card2_rect, card1, card2, game_stat):                        #Fonction choix de la carte avec hitbox 
    while True:
        event = pygame.event.wait()                                                               #Evenement = attendre
        # if event.type == pygame.QUIT:
        #     exit()
        if event.type == pygame.KEYDOWN:                                                         
             if event.key == pygame.K_ESCAPE:
                 exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos                                                                  #position de la souris = la position ou t'as cliqué 
            if card1_rect.collidepoint(mouse_pos):                                                 #Si tu touches la carte 1 :
                choosen_card = {}                                                                  #Initialisation d'un dico
                choosen_card["food"] = card1["food"] * game_stat["saison"]["multFood"]                  #Recopiage des stats de la carte 1 food sur la choosen_card
                choosen_card["materials"] = card1["materials"] * game_stat["saison"]["multMaterials"]   #Recopiage des stats de la carte 1 ressource sur la choosen_card
                choosen_card["health"] = card1["health"] * game_stat["saison"]["multHealth"]            #Recopiage des stats de la carte 1 santé sur la choosen_card
                choosen_card["power"] = card1["power"] * game_stat["saison"]["multPower"]               #Recopiage des stats de la carte 1 power sur la choosen_card
                choosen_card["relationship"] = card1["relationship"] * game_stat["saison"]["multRelationship"] #Recopiage des stats de la carte 1 cohésion sur la choosen_card
                game_stat["compteur_jour"] += 1
                return choosen_card, game_stat                                                              #On renvoie le dico choosen_card rempli des stats de la carte 1
            if card2_rect.collidepoint(mouse_pos):                                                 
                choosen_card = {}                                                                  #La même chose pour la carte 2
                choosen_card["food"] = card2["food"] * game_stat["saison"]["multFood"]
                choosen_card["materials"] = card2["materials"] * game_stat["saison"]["multMaterials"]
                choosen_card["health"] = card2["health"] * game_stat["saison"]["multHealth"]
                choosen_card["power"] = card2["power"]  * game_stat["saison"]["multPower"]
                choosen_card["relationship"] = card2["relationship"] * game_stat["saison"]["multRelationship"]
                game_stat["compteur_jour"] += 1
                return choosen_card, game_stat                                                                #On renvoie le dico choosen_card rempli des stats de la carte 1


def display_card(card, pos_card, Xcard, Ycard):
    display_text(win, card["name"], Xcard + 50, Ycard + 33, 32,0,0,0)
    display_text(win, str(card["health"] * game_stat["saison"]["multHealth"]), Xcard1 + pos_card[0], Ycard1 + 450, 30,233,56,63)
    display_text(win, str(card["food"] * game_stat["saison"]["multFood"]), Xcard1 + pos_card[1], Ycard1 + 450, 30,223, 109, 20)
    display_text(win, str(card["materials"] * game_stat["saison"]["multMaterials"]), Xcard1 + pos_card[2], Ycard1 + 450, 30,103, 113, 121)
    display_text(win, str(card["relationship"] * game_stat["saison"]["multRelationship"]), Xcard1 + pos_card[3], Ycard1 + 450, 30,205, 205, 13)
    display_text(win, str(card["power"] * game_stat["saison"]["multPower"]), Xcard1 + pos_card[4], Ycard1 + 450, 30,0,0,0)

def display_card_logo(food_logo, health_logo, relation_logo, ressource_logo, power_logo, logo_pos):
    win.blit(health_logo, (Xcard1 + logo_pos[0], Ycard1 + 380))
    win.blit(food_logo, (Xcard1 + logo_pos[1], Ycard1 + 380))
    win.blit(ressource_logo, (Xcard1 + logo_pos[2], Ycard1 + 380))
    win.blit(relation_logo, (Xcard1 + logo_pos[3], Ycard1 + 380))
    win.blit(power_logo, (Xcard1 + logo_pos[4], Ycard1 + 380))

def load_logo():
    # Chargement des logos
    food_logo = pygame.image.load("images/card_logo/food.png").convert_alpha()
    health_logo = pygame.image.load("images/card_logo/health.png").convert_alpha()
    ressource_logo = pygame.image.load("images/card_logo/ressource.png").convert_alpha()
    relation_logo = pygame.image.load("images/card_logo/relationship.png").convert_alpha()
    power_logo = pygame.image.load("images/card_logo/power.png").convert_alpha()

    # Changement des tailles des logos
    food_logo = pygame.transform.scale(food_logo, (75, 75))
    health_logo = pygame.transform.scale(health_logo, (75, 75))
    ressource_logo = pygame.transform.scale(ressource_logo, (75, 75))
    relation_logo = pygame.transform.scale(relation_logo, (75, 75))
    power_logo = pygame.transform.scale(power_logo, (75, 75))
    return food_logo, health_logo, relation_logo, ressource_logo, power_logo

def display_card_picture(card, picture_pos, picture_scale, Xcard, Ycard):
    image = pygame.image.load(card["image"]).convert()
    image = pygame.transform.scale(image, (Xcard + picture_scale[0], Ycard + picture_scale[1]))
    win.blit(image, (Xcard + picture_pos[0], Ycard + picture_pos[1]))

def display_actual_text_stat(perso_stat):
    display_text(win, str(perso_stat["FoodStart"]), 150, 490, 30,223, 109, 20)         
    display_text(win, str(perso_stat["HealthStart"]), 150, 590, 30,233,56,63)
    display_text(win, str(perso_stat["MaterialsStart"]), 150, 690, 30,103, 113, 121)
    display_text(win, str(perso_stat["RelationshipStart"]), 150, 790, 30,252, 220, 18)
    display_text(win, str(perso_stat["PowerStart"]), 150, 890, 30,0,0,0)

def display_actual_logo(food_logo, health_logo, relation_logo, ressource_logo, power_logo): # Affichage des logos des stats persos
    food_logo = pygame.transform.scale(food_logo, (100, 100))
    win.blit(food_logo, (50, 460))
    health_logo = pygame.transform.scale(health_logo, (100, 100))
    win.blit(health_logo, (50, 560))
    ressource_logo = pygame.transform.scale(ressource_logo, (100, 100))
    win.blit(ressource_logo, (50, 660))
    relation_logo = pygame.transform.scale(relation_logo, (100, 100))
    win.blit(relation_logo, (50, 760))
    power_logo = pygame.transform.scale(power_logo, (100, 100))
    win.blit(power_logo, (50, 860))

def display_season(saison):
    logo_saison = pygame.image.load(saison["image"]).convert_alpha()
    logo_saison = pygame.transform.scale(logo_saison, (100 , 100 ))
    win.blit(logo_saison, (970, 970))
    #display_text(win, saison["name"], 300, 460, 30 ,0, 0, 0)     

def barre_logo(perso_stat):
    y=0
    if perso_stat["FoodStart"] >= 90 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre90.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 80 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre80.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 70 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre70.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 60 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre60.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 50 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre50.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 40 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre40.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 30 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre30.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 20 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre20.png").convert_alpha()
        y+=1
    if perso_stat["FoodStart"] >= 10 and y == 0:
        barre_saison = pygame.image.load("images/barre_logo/barre10.png").convert_alpha()
        y+=1
    barre_saison = pygame.transform.scale(barre_saison, (230, 80))
    return barre_saison
    
def display_interface(win, cards_available, perso_stat, game_stat):
    card_asset = pygame.image.load("images/interface/card2.png").convert()
    card_asset = pygame.transform.scale(card_asset, (Lcard1, Hcard1))

    # Afficher le fond avec les deux "choix"  carre

    card1, card2, cards_available = card_choice(cards_available)

    card1_rect = pygame.draw.rect(win, (0, 200, 0), (Xcard1, Ycard1, Lcard1, Hcard1))
    card2_rect = pygame.draw.rect(win, (200, 0, 0), (Xcard2, Ycard2, Lcard2, Hcard2))

    win.blit(card_asset, (Xcard1, Ycard1))
    win.blit(card_asset, (Xcard2, Ycard2))

    display_card(card1, (56, 135, 205, 290, 360), Xcard1, Ycard1)
    display_card(card2, (826, 910, 975, 1060, 1130), Xcard2, Ycard2)
                                                                                                                        
    food_logo, health_logo, relation_logo, ressource_logo, power_logo = load_logo()

    display_card_logo(food_logo, health_logo, relation_logo, ressource_logo, power_logo, (40, 115, 190, 265, 340))
    display_card_logo(food_logo, health_logo, relation_logo, ressource_logo, power_logo, (810, 885, 960, 1035, 1110))

    display_card_picture(card1, (39, 70), (-175, 15), Xcard1, Ycard1)
    display_card_picture(card2, (39, 70), (-945, 15), Xcard2, Ycard2)

    display_actual_text_stat(perso_stat)

    display_actual_logo(food_logo, health_logo, relation_logo, ressource_logo, power_logo)

    display_text(win,"Jour : "+ str(game_stat["compteur_jour"]),30, 1000, 60,0,0,0)
    display_season(game_stat["saison"])
    pygame.display.flip()
    choosen_card, game_stat = wait_for_choice(card1_rect, card2_rect, card1, card2, game_stat)
    #barre_saison = pygame.image.load("images/interface/barre 90.png").convert_alpha()
    #barre_saison = barre_logo(perso_stat)
    #barre_saison = pygame.transform.scale(logo_saison, (400 , 400 ))
    #win.blit(barre_saison, (39, 970))       #DATHARR

    

    # Affichage du texte du compteur
    perso_stat = update_ressources(win, perso_stat, choosen_card)
    return perso_stat, cards_available, game_stat

def update_ressources(win, perso_stat, choosen_card):
        perso_stat["FoodStart"] += choosen_card["food"]
        perso_stat["HealthStart"] += choosen_card["health"]
        perso_stat["MaterialsStart"] += choosen_card["materials"]
        perso_stat["PowerStart"] += choosen_card["power"]
        perso_stat["RelationshipStart"] += choosen_card["relationship"]

        if perso_stat["FoodStart"] >= 100 or perso_stat["HealthStart"] >=100 or perso_stat["MaterialsStart"] >=100 or perso_stat["RelationshipStart"] >= 100:
            while True:
                lost_img = pygame.image.load("images/fullscreen/deathfull.png").convert()
                win.blit(lost_img, (0, 0))
                pygame.display.flip()
                check_input_exit()

        if perso_stat["FoodStart"] <= 0 or perso_stat["HealthStart"] <= 0 or perso_stat["MaterialsStart"] <= 0 or perso_stat["RelationshipStart"] <= 0:
            while True:
                lost_img = pygame.image.load("images/fullscreen/deathlost.png").convert()
                win.blit(lost_img, (0, 0))
                pygame.display.flip()
                check_input_exit()
        return perso_stat

def check_input_exit():
    for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
                                                                                            
def arc_saison(compteur_jour, game_stat):
    if compteur_jour == 10:
        current_saison = random.choice(saison_list)
    elif compteur_jour < 10:
        current_saison = saison_list[0]
    else:
        return game_stat["saison"]
    return current_saison

def perso_choice():
    a = 0
    screen_choice = pygame.image.load("images/perso_choice.png").convert()
    screen_choice = pygame.transform.scale(screen_choice, (1920, 1080))                     ############################################################
    while a == 0:
        win.blit(screen_choice, (0, 0))
        perso1_rect = pygame.draw.rect(win, (0, 200, 0), (286,  39, 204, 242))
        perso2_rect = pygame.draw.rect(win, (200, 0, 0), (494, 39, 204, 242))
        perso3_rect = pygame.draw.rect(win, (0, 0, 200), (708, 39, 204, 242))
        perso4_rect = pygame.draw.rect(win, (200, 0, 200), (930, 39, 204, 242))
        perso5_rect = pygame.draw.rect(win, (200, 0, 0), (1146, 39, 204, 242))
        win.blit(screen_choice, (0, 0))
        while a == 0:
            event = pygame.event.wait()                                                               #Evenement = attendre
            if event.type == pygame.KEYDOWN:                                                         
                if event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos                                                                  #position de la souris = la position ou t'as cliqué 
                if perso1_rect.collidepoint(mouse_pos): 
                    print("1")        
                    perso_stat = perso_list[0]
                    a = 1
                    return perso_stat
                if perso2_rect.collidepoint(mouse_pos): 
                    print("2")        
                    perso_stat = perso_list[1]
                    a = 1
                    return perso_stat
                if perso3_rect.collidepoint(mouse_pos): 
                    print("3")        
                    perso_stat = perso_list[2]
                    a = 1
                    return perso_stat
                if perso4_rect.collidepoint(mouse_pos): 
                    print("4")        
                    perso_stat = perso_list[3]
                    a = 1
                    return perso_stat
                if perso5_rect.collidepoint(mouse_pos):
                    print("5")     
                    perso_stat = perso_list[4]
                    a = 1
                    return perso_stat
            
            pygame.display.flip()
            check_input_exit()

if __name__ == "__main__":
    perso_stat = perso_list[0]
    cards_available = cards_list
    game_stat = {"saison": saison_list[0],"compteur_jour": 0}
    pygame.init()
    win = pygame.display.set_mode((Xsize, Ysize), pygame.FULLSCREEN)
    perso_stat = perso_choice()
   
    background_img = pygame.image.load("images/interface/background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (Xsize, Ysize))                  

    hud_img = pygame.image.load("images/interface/hud.jpg").convert()
    hud_img = pygame.transform.scale(hud_img, (HUDXsize, HUDYsize))

    survivor_img = pygame.image.load(perso_stat["image"]).convert()
    survivor_img = pygame.transform.scale(survivor_img, (HUDXsize - 40, 400))

    paint_img = pygame.image.load("images/interface/paint.jpg").convert()
    paint_img = pygame.transform.scale(paint_img, (HUDXsize-40, 550))
    pygame.display.flip()

    slot_img = pygame.image.load("images/interface/slot.png").convert()  
    slot_img = pygame.transform.scale(slot_img, (HUDXsize+50, 100))

    pillier_img = pygame.image.load("images/interface/pillier.png").convert_alpha()  
    pillier_img = pygame.transform.scale(pillier_img, (200, 1400))

    #display_card(cards_list)
    while True:
        barre_saison_food = barre_logo(perso_stat)       
        win.blit(background_img, (0, 0))
        win.blit(hud_img, (0, 0))
        win.blit(paint_img, (20, 440))
        win.blit(survivor_img, (20, 20))
        win.blit(slot_img, (950, 970))
        win.blit(pillier_img, (348, -158))
        win.blit(barre_saison_food, (135, 468))
        
        
        
        # pygame.display.flip()
        # event = pygame.event.wait()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         display_board(win, background)
        #         time.sleep(1)
        #         break

        game_stat["saison"] = arc_saison(game_stat["compteur_jour"], game_stat)

        # Selection de personnages
        perso_stat, cards_available, game_stat= display_interface(win, cards_available, perso_stat, game_stat) # rempalace saison et compteur jour par game stat ( ne pas oublier de return game stat)

        check_input_exit()
