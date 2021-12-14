from random import randint
from dataclasses import dataclass

@dataclass
class Drop:

    inventory : dict
    strength : int
    attack : int
    potion : int

    def drop_items(self):
        dict = {"EXCALIBUR" : 50, "une hâche": 20, "une épee": 15, "une dague": 8, "un cure-dent": 2}
        chance = randint(0, 100)
        values = list(self.inventory.values())
        keys = list(self.inventory.keys())
        for i in range (len(self.inventory.keys())-1, -1, -1):
            if chance < values[i]:
                if keys[i] == "Potion":
                    self.potion += 1
                    print(f'Vous avez obtenu une potion. {self.potion=}')
                else:
                    if self.attack < self.strength + dict[keys[i]]:
                        self.attack = self.strength + dict[keys[i]]
                        print(f'Vous avez obtenu {keys[i]} et votre attaque passe à {self.attack}')
                    else:
                        print(f'Vous obtenez {keys[i]} mais vous possédez déjà un meilleur équipement')
                break
        return self.attack, self.potion

drop = Drop({"une hâche" : 80, "une épee": 20}, 5, 5, 3)
print(drop.attack)