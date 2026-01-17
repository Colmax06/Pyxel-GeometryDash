import pyxel

def menu_update(game_menu, chosen_level, level1, level2, current_level, menu, in_level, chosen_level_max, x, y):
    pyxel.mouse(True)
    if game_menu == 1: #menu principale
        #Quitter
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            #A FAIRE (SUR DE QUITTER)

        #Bouton pour game_menu = 2
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < x/2+16 and pyxel.mouse_x > x/2-16 and pyxel.mouse_y < y/2+16 and pyxel.mouse_y > y/2-16:
            game_menu = 2
            chosen_level = 1
    

    elif game_menu == 2:
        #Retour game_menu (croix)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            game_menu = 1

        #Choix niveau
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 10+16 and pyxel.mouse_x > 10 and pyxel.mouse_y < y/2+16 and pyxel.mouse_y > y/2 or pyxel.btnp(pyxel.KEY_LEFT): #gauche
            if chosen_level == 1:
                chosen_level = chosen_level_max
            else:
                chosen_level -=1
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < x-10 and pyxel.mouse_x > x-10-16 and pyxel.mouse_y < y/2+16 and pyxel.mouse_y > y/2 or pyxel.btnp(pyxel.KEY_RIGHT): #droit
            if chosen_level == chosen_level_max:
                chosen_level = 1
            else:
                chosen_level +=1

        #Bouton cliqué ?
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < x/2-64+128 and pyxel.mouse_x > x/2-64 and pyxel.mouse_y < y/2-16+32 and pyxel.mouse_y > y/2-16 or pyxel.btnp(pyxel.KEY_RETURN):
                if chosen_level == 1:
                    level1 = True
                    current_level = 'level1'
                if chosen_level == 2:
                    level2 = True
                    current_level = 'level2'
                menu = False
                in_level = True

    return game_menu, chosen_level, level1, level2, current_level, menu, in_level #valeurs modifiées

def menu_draw(game_menu, chosen_level, x, y):
    if game_menu == 1: #menu principale
        pyxel.cls(1)

        #Quitter
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)

        #Bouton pour game_menu = 2
        pyxel.blt(x/2-16, y/2-16, 1, 0, 0, 32, 32,0)


    elif game_menu == 2: #Sélection niveaux
        pyxel.cls(1)

        #Retour game_menu (croix)
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)

        
        #Choix niveau
        pyxel.blt(10, y/2, 1, 32, 16, 16, 16,0) #gauche
        pyxel.blt(x-10-16, y/2, 1, 32, 0, 16, 16,0) #droit
        
        #Affichage des boutons niveaux
        if chosen_level == 1:
            pyxel.bltm(x/2-64, y/2-16, 0, 0, 1*32, 128, 32, 0)

        if chosen_level == 2:
            pyxel.bltm(x/2-64, y/2-16, 0, 0, 2*32, 128, 32, 0)