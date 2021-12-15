from dataclasses import dataclass
from typing import ClassVar
from abc import ABCMeta, abstractmethod
from random import randint
from drop import Drop
import time, os
from termcolor import colored

clear = lambda: os.system('cls') # clear the console 

@dataclass
class Entity(metaclass = ABCMeta):
    name : str
    hp : int
    hp_max : int
    strength : int
    @abstractmethod
    def attack(self):
        pass
    @abstractmethod
    def death(self):
        pass

@dataclass
class Monster(Entity):
    points : ClassVar[int] = 10
    droprate : ClassVar[float] = 10
    exp_points : ClassVar[int] = 10
    weak_attack : ClassVar[float]
    defense : int = 0
    gold : ClassVar[int] = 10

    def level(self,floor,difficulty):
        """ This function give the force and the health points of the monster, using the floor's level and the difficulty's level."""

        self.droprate *= (((floor/10)+difficulty)+1)
        self.strength = round(self.strength * (((floor/10)+difficulty)+1))
        self.hp = round(self.hp * (((floor/10)+difficulty)+1))
        self.hp_max = self.hp
        self.gold = round(self.gold * ((floor/10)+difficulty+1))
        self.points = round(self.points * (((floor/10)+difficulty)+1))
        self.exp_points += floor * 5
        print(colored(f"           {self.name}","green"), f"s'approche de vous ! Il posséde {self.hp} points de vie et une force de {self.strength}.")
        return self.points, self.droprate, self.strength, self.hp, self.exp_points

    def attack(self,player):
        """This function takes away health points from life's player when an ennemy attacks him."""
        if player.defense_s != 0 :
            self.weak_attack = round(self.strength / 2)
            player.defense_s -= 1
            player.hp -= self.weak_attack
            print("Vous avez subi",colored(f"-{self.weak_attack}","red"), f"points de dégâts de la part de l'ennemi")

        elif player.defense != 0 :
            self.weak_attack = round(self.strength / 1.5)
            player.defense -= 1
            player.hp -= self.weak_attack
            print("Vous avez subi",colored(f"-{self.weak_attack}","red"), f"points de dégâts de la part de l'ennemi")
            
        else:    
            player.hp -= self.strength
            print("Vous avez subi",colored(f"-{self.strength}","red"), f"points de dégâts de la part de l'ennemi")

        player.mana +=1 
        print(f'{player.name} : {player.hp}/{player.hp_max} HP    |     {self.name} : {self.hp}/{self.hp_max} HP.')
        return player.hp

    def death(self, player, score):
        """"This function will delete the last summoned monster and run the drop() method"""
        print(f"Félicitations ! Vous avez réussi à vaincre l'ennemi!")
        number = randint(0,100)
        if self.droprate >= number:
            print("L'ennemi a laissé tomber quelque chose")
            item = {"une dague" : 20, "Potion": 50, "un cure-dent": 30 } 
            dropped = Drop(item,player.strength, player.power, player.potion)
            player.power, player.potion = dropped.drop_items()
        score += self.points
        player.experience += self.exp_points
        player.gold += self.gold
        clear()
        return score

class Boss(Entity):
    points : ClassVar[int] = 15
    droprate : ClassVar[float] = 30
    weak_attack : ClassVar[float]
    defense : ClassVar[int] = 0
    countdown : ClassVar[int] = 0
    exp_points : ClassVar[int] = 100
    gold : ClassVar[int] = 100

    def level(self,floor,difficulty):
        """ This function give the force and the health points of the boss, using the floor's level and the difficulty's level."""

        self.droprate *= (floor/10) + difficulty + 1
        self.strength = round(self.strength * (((floor/10)+difficulty)+1))
        self.hp = round(self.hp * (((floor/10)+difficulty)+1))
        self.hp_max = self.hp
        self.points = round(self.points * (((floor/10)+difficulty)+1))
        self.exp_points *= floor/5
        self.gold = round(self.gold * ((floor/10)+difficulty)+1)
        print(f"            {self.name} vient d'apparaître ! Un boss avec {self.hp} points de vie et avec une force de {self.strength}.")
        return self.points, self.droprate, self.strength, self.hp, self.exp_points

    def attack(self,player):
        """This function takes away health points from life's player when the Boss attacks him."""
        if self.countdown < 2 : 

            if player.defense_s != 0 :
                self.weak_attack = round(self.strength / 2)
                player.defense_s -= 1
                player.hp -= self.weak_attack
                print(f"Vous avez subi {self.weak_attack} points de dégâts de la part de l'ennemi")

            elif player.defense != 0 :
                self.weak_attack = round(self.strength / 1.5)
                player.defense -= 1
                player.hp -= self.weak_attack
                print("Vous avez subi",colored(f"-{self.weak_attack}","red"), f"points de dégâts de la part de l'ennemi")

            else:    
                player.hp -= self.strength
                print(f"Vous avez subi {self.strength} points de dégâts de la part de l'ennemi")
                time.sleep(1)
                print(f'{player.name} : {player.hp}/{player.hp_max} HP    |     {self.name} : {self.hp}/{self.hp_max} HP.')
                # Come back to the fight
            self.countdown += 1
            self.defense -= 1
            player.mana += 1

        else:
            self.defense = self.defend()
            self.countdown = 0

        return player.hp

    def death(self, player, score):
        """"This function will delete the last summoned monster and run the drop() method"""
        print(f"Félicitations ! Vous avez réussi à vaincre l'ennemi!")
        number = randint(0,100)
        if self.droprate >= number:
            print("L'ennemi a laissé tomber quelque chose")
            item = {"Excalibur" : 1, "une hâche": 49, "une épee": 30, "Potion": 20 } 
            dropped = Drop(item, player.strength, player.power, player.potion)
            player.power, player.potion = dropped.drop_items()
        score += self.points
        player.experience += self.exp_points
        player.gold += self.gold
        time.sleep(1)
        clear()
        return score
    
    def defend(self):
        """This function give a protection to the Boss during 3 turns."""
        self.defense = 3
        print(f"{self.name} vient de s'équiper d'une protection pendant 3 tours !")
        # Come back to the fight
        return self.defense

@dataclass
class Player(Entity):   
    potion : ClassVar[int] = 3
    mana_potion : ClassVar[int] = 1
    defense : ClassVar[int] = 0
    experience : ClassVar[int] = 0
    exp_dict : ClassVar[dict] = {1: 30, 2: 120, 3: 250, 4: 420, 5: 620, 6: 870, 7: 1160, 8: 1490, 9: 1860, 10: 2270}
    level : ClassVar[int] = 1
    gold : ClassVar[int] = 0
    mana : ClassVar[int] = 6
    defense_s : ClassVar[int] = 0
        
    def attack(self,monster,score):
        """This function takes away health points from life's ennemy when the player attacks."""
        if monster.hp <= self.power:
            score = monster.death(self, score)
            monster.hp = 0
        else:
            if monster.defense <= 0:
                monster.hp -= self.power
            else:
                monster.hp -= round(self.power/1.5)
            clear()
            print("L'ennemi a subi",colored(f"-{self.power}", "blue")," points de dégats")
            # Retour sur combat
        return score, monster.hp

    def level_up(self):
        """This function boosts base stats of the player when the player reaches a certain exeperience"""
        self.experience -= self.exp_dict[self.level]
        self.level += 1
        self.strength += 2
        self.power += 2
        self.hp_max += 10
        self.hp += 10
        print(f"Votre personnage est passé niveau {self.level}")
        print(f"Attack +2 => {self.strength} | HP +10 => {self.hp}/{self.hp_max}")

    def death(self):
        """This function allow to finish the game when the player is dead"""
        print(colored("Votre ennemi vient malheureusement de vous porter un coup fatal ! \nVous gisez à terre en souffrant le martyre... \nEt dans un dernier râle d'agonie, vous succombez à vos blessures en vous demandant si ça valait vraiment la peine d'être venu...","red"))
        return False
    
    def defend(self):
        """This function give a shield to the player during 3 turns."""
        self.defense = self.shield
        print("Te voilà équipé d'un bouclier pendant 3 tours !")
        return self.defense
            
    def drink_potion(self):
        """This function gives back 30 HP to the player in battle."""
        if self.hp < self.hp_max -30:
            self.hp += 30
        else:
            self.hp = self.hp_max
        self.potion -= 1
        print(f'-------Vous avez maintenant {self.potion} potions et {self.hp}PV')
        # Retour sur combat
        return self.hp, self.potion

    def defend_special(self):
        if self.defense !=0 or self.defense_s !=0:
                print("Tu as déjà un bouclier !")
        else:
            self.defense_s = self.defense_number
            print(f"Te voilà équipé d'un bouclier pendant {self.defense_number} tours !")
            self.mana -= 8
            # Retour sur combat
        return self.defense_s 

    def attack_special(self, monster, score):
        if monster.hp <= round(self.power * self.power_d):
                score = monster.death(self, score)
                monster.hp = 0
        else:
            if monster.defense <= 0:
                monster.hp -= round(self.power * self.power_d)
            else:
                monster.hp -= round(self.power/1.5)
        self.mana -= 8
        clear()
        print("L'ennemi a subi",colored(f"-{round(self.power * self.power_d)}", "blue")," points de dégats")
        # Retour sur combat
        return score, monster.hp, self.mana

@dataclass
class Wizard(Player):

    character : ClassVar[str] = "Wizard"
    power : ClassVar[int] = 4
    shield : ClassVar[int] = 3
    defense_number : ClassVar[int] = 3
    power_d : ClassVar[float] = 2.5
    classic_attack : ClassVar[str] = "Sort de base"
    special_attack : ClassVar[str] = "Fléau démoniaque"
    classic_defense : ClassVar[str] = "Aura protectrice"
    special_defense : ClassVar[str] = "Incantation divine"

@dataclass
class Paladin(Player):

    character : ClassVar[str] = "Paladin"
    power : ClassVar[int] = 5
    shield : ClassVar[int] = 2
    defense_number : ClassVar[int] = 4
    power_d : ClassVar[float] = 2
    classic_attack : ClassVar[str] = "Attaque classique "
    special_attack : ClassVar[str] = "One Punch Paladin"
    classic_defense : ClassVar[str] = "Protection normale"
    special_defense : ClassVar[str] = "Defense ultime"

@dataclass
class Knight(Player):

    character : ClassVar[str] = "Knight"
    power : ClassVar[int] = 6
    shield : ClassVar[int] = 3
    defense_number : ClassVar[int] = 3
    power_d : ClassVar[float] = 1.5
    classic_attack : ClassVar[str] = "Sauvagerie modérée"
    special_attack : ClassVar[str] = "Berserk Knight"
    classic_defense : ClassVar[str] = "Ecu de bois"
    special_defense : ClassVar[str] =  "Bouclier titanesque"

