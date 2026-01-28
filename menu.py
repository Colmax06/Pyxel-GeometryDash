import pyxel

def menu_update(game):
    pyxel.mouse(True)
    if game.game_menu == 1: #menu principale
        #Quitter
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
            #A FAIRE (SUR DE QUITTER)

        #Bouton pour game_menu = 2
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < game.x/2+16 and pyxel.mouse_x > game.x/2-16 and pyxel.mouse_y < game.y/2+16 and pyxel.mouse_y > game.y/2-16:
            game.game_menu = 2
            game.chosen_level = 1
    

    elif game.game_menu == 2:
        #Retour game_menu (croix)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            game.game_menu = 1

        #Choix niveau
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 10+16 and pyxel.mouse_x > 10 and pyxel.mouse_y < game.y/2+16 and pyxel.mouse_y > game.y/2 or pyxel.btnp(pyxel.KEY_LEFT): #gauche
            if game.chosen_level == 1:
                game.chosen_level = game.chosen_level_max
            else:
                game.chosen_level -= 1
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < game.x-10 and pyxel.mouse_x > game.x-10-16 and pyxel.mouse_y < game.y/2+16 and pyxel.mouse_y > game.y/2 or pyxel.btnp(pyxel.KEY_RIGHT): #droit
            if game.chosen_level == game.chosen_level_max:
                game.chosen_level = 1
            else:
                game.chosen_level += 1

        #Bouton cliqué ?
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < game.x/2-64+128 and pyxel.mouse_x > game.x/2-64 and pyxel.mouse_y < game.y/2-16+32 and pyxel.mouse_y > game.y/2-16 or pyxel.btnp(pyxel.KEY_RETURN):
            if game.chosen_level == 1:
                game.level1 = True
                game.current_level = 'level1'
            if game.chosen_level == 2:
                game.level2 = True
                game.current_level = 'level2'
            game.menu = False
            game.in_level = True

def menu_draw(game):
    if game.game_menu == 1: #menu principale
        pyxel.cls(1)

        #Quitter
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)

        #Bouton pour game_menu = 2
        pyxel.blt(game.x/2-16, game.y/2-16, 1, 0, 0, 32, 32,0)


    elif game.game_menu == 2: #Sélection niveaux
        pyxel.cls(1)

        #Retour game_menu (croix)
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)

        
        #Choix niveau
        pyxel.blt(10, game.y/2, 1, 32, 16, 16, 16,0) #gauche
        pyxel.blt(game.x-10-16, game.y/2, 1, 32, 0, 16, 16,0) #droit
        
        #Affichage des boutons niveaux
        if game.chosen_level == 1:
            pyxel.bltm(game.x/2-64, game.y/2-16, 0, 0, 1*32, 128, 32, 0)

        if game.chosen_level == 2:
            pyxel.bltm(game.x/2-64, game.y/2-16, 0, 0, 2*32, 128, 32, 0)