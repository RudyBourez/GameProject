from entity import Player, Boss, Monster, Wizard, Paladin, Knight
from random import randint
from termcolor import colored
import time
import os
import csv
import pygame

pygame.init()


clear = lambda: os.system('cls') # clear the console

class Game:
    def __init__(self):
        self.running = True
        self.floor = 1
        self.score = 0
        self.introducing()

    def introducing(self):
        """Description of the game and beginning. Create an instance for a new player or load the last saved game."""
        print(colored('Bienvenue sur le jeu :', 'white'),colored( 'Simplon Escape !', 'red'))
        print("Le but du jeu est de sauver la princesse" ,colored("Claire","red"), "emprisonnée en haut du donjon Simplon.co. \nVous êtes le Héros de cette quête et partez à la rescousse de la princesse. \nVous aurez à affronter de nombreux ennemis au cours de votre ascension dans le donjon.")
        defi = input("-----------------------------------------\nPréférez-vous démarrer une partie ? (Y/N) ou charger votre dernière partie ? (L)")
        while self.running:
            if defi.lower() == "y":
                clear()
                print("Votre bravoure vous honore ! Et ce sacrifice quasi certain restera à jamais dans les livres d'histoire ...")
                name = input("Mais au fait, quel(le) est ton nom jeune aventurier(ère) ?    ")
                player = Player(name, 50, 50, 5)
                print(colored(f"{player.name}","blue")," dis-tu ?... Ca reviendra certainement un jour à la mode...")
                time.sleep(1)
                print("Trêve de bavardages ! Il est temps pour toi de te confronter au plus grand défi de ta vie !")
                time.sleep(1)
                print("------------------------------------------ Génération du donjon ---------------------------------------------")
                time.sleep(2)
                clear()
                self.run(player)
            elif defi.lower() == "l":
                self.load()
                break
            elif defi.lower() == "n":
                self.running = False
                print("Votre décision est lourde de conséquences. Claire restera dans son donjon pour le restant de ses jours...\n Ouste couard ! Reviens quand tu seras un peu plus valeureux !")
                break
            else:
                defi = input("Toi pas comprendre ? Y ou N ? ou L ")

    def run(self,player):
        """Start the game"""
      
        while self.running:
            choice = self.choice(player)
            if not choice:
                break
        if self.score != 0:
            with open("Scores.txt", 'a') as scores:
                scores.write(f'{player.name} =====> score = {self.score} | floor = {self.floor}\n')
                
    def choice(self, player):
        """Choice of a path giving a certain difficulty used for the spawn of the monster"""
        print(f"                           Vous arrivez à l'étage {self.floor} et votre score est de {self.score}\n")
        time.sleep(1)
        path = ""
        print("4 chemins s'offrent à vous, choisissez l'un d'entre eux ou abandonner lâchement pour le moment.")
        while path not in ["$", "a", "b", "c", "d"]:
            print("1: boutique | a: Chemin des petits joueurs (facile) | b: Route normale | c: Sentier des braves (difficile) | d: Sauvegarder et quitter")
            path = input("Quel est votre choix $ | A | B | C | D ?      ")
            time.sleep(1)
            if path == "$":
                self.buy(player)
                path = ""
            elif path.lower() in ["a","b","c"]:
                clear()
                if path.lower() == "a":
                    difficulty = 0
                elif path.lower() == "b":
                    difficulty = 0.1
                else :
                    difficulty = 0.2
                self.summon_monster(difficulty, player)
                path = ""
            elif path.lower() == "d":
                self.quit(player)
            else:
                print("Toi pas comprendre ?")
            if player.hp <= 0:
                break

    def summon_monster(self, difficulty, player):
        """Generates a monster or a boss depending of the floor"""
        if self.floor % 5 == 0:
            list_boss_name = ["Dracula", "Frankenstein", "BigTroll", "Lucifer"]
            boss_name = list_boss_name[randint(0,len(list_boss_name)-1)]
            monster = Boss(boss_name, 35, 35, 8)
        else:
            list_monster_name = ["Un gobelin", "Un troll", "Un orc", "Un zombie", "Un mimic", "Yanis: le voleur d'excalibur"]
            monster_name = list_monster_name[randint(0,len(list_monster_name)-1)]
            monster = Monster(monster_name, 20, 20, 4)
        monster.level(self.floor, difficulty)
        self.fight(player, monster)

    def fight(self, player, monster):
        """Manages the fight between the player and a monster"""
        while player.hp > 0 and monster.hp > 0:
            choice = input("1: Attaque | 2: Défendre | 3: Potion\n")
            time.sleep(1)
            if choice == "1":
                self.score, monster.hp = player.attack(monster,self.score)
            elif choice == "2":
                clear()
                player.defense = player.defend()
            elif choice == "3":
                if player.potion > 0 :
                    pygame.mixer.music.load("Assets/drink1.wav")
                    pygame.mixer.music.play()
                    time.sleep(2)
                    player.hp, player.potion = player.drink_potion()
                else:
                    print("Vous n'avez plus de potions")
            
            if monster.hp > 0 and choice in ["1", "2"]:
                player.hp = monster.attack(player)
        if player.hp <= 0 :
            self.running = player.death()
        else:
            pygame.mixer.music.load("Assets/fighting.mp3")
            pygame.mixer.music.play()
            time.sleep(1)
            if player.experience > player.exp_dict[player.level]:
                player.level_up()
            del monster
            self.floor += 1
            print(f"Votre score est de ",colored(f"{self.score}","red")," et vous passez à l'étage ",colored(f"{self.floor}","red"))
            
    def quit(self,player):
        """Allow to quit the game and save the progression"""
        self.running = False
        print(f"Vous quittez le donjon! Votre score est de {self.score} et votre étage de {self.floor}")
        with open('save.csv','w', newline='\n') as csvfile:
            save_writer = csv.writer(csvfile, delimiter ='|')
            save_writer.writerow([player.name, player.hp, player.hp_max, player.strength, player.potion, player.power, player.experience, player.level, self.score, self.floor ])

    def buy(self,player):
        print("Healing_potion(100gold) : 1 | Mana_potion(300gold) : 2 | Exit : 3")
        print(f"Vous avez {player.gold} gold")
        buying = True
        while buying:
            item = input("Que voulez-vous acheter?  ")
            if item == "1":
                number = input("Combien en voulez-vous?   ")
                try:
                    if player.gold >= int(number) * 100 and int(number) >= 0:
                        player.potion += int(number)
                        player.gold -= int(number) * 100
                        print(f"{player.gold}")
                        print(f"Vous avez maintenant {player.potion} potions")
                    else :
                        print("Vous n'avez pas assez de monnaie")
                except:
                    print("Veuillez indiquer un nombre correct")
            elif item == "2":
                number = input("Combien en voulez-vous?   ")
                try:
                    if player.gold >= int(number) * 300 and int(number) >= 0:
                        player.mana_potion += int(number)
                        player.gold -= int(number) * 300
                        print(f"{player.gold}")
                        print(f"Vous avez maintenant {player.mana_potion} potions de mana")
                    else :
                        print("Vous n'avez pas assez de monnaie")
                except:
                    print("Veuillez indiquer un nombre correct")
            elif item == "3":
                buying = False

    def load(self):
        print(f"Chargement de la partie...")
        try:
            with open('save.csv','r', newline='\n') as csvfile:
                saved_games = list(csv.reader(csvfile, delimiter = '|'))
                for saved_game in saved_games:
                    name = str(saved_game[0])
                    hp = int(saved_game[1])
                    hp_max = int(saved_game[2])
                    strength = int(saved_game[3])
                    
                    player = Player(name,hp,hp_max,strength)
                    player.potion = int(saved_game[4])
                    player.power = int(saved_game[5])
                    player.experience = float(saved_game[6])
                    player.level = int(saved_game[7])
                    self.score = int(saved_game[8])
                    self.floor = int(saved_game[9])
        except FileNotFoundError:
            print("Le fichier save.csv n'existe pas")     
        except:
            raise Exception("Erreur dans le fichier save.csv")
        self.run(player)