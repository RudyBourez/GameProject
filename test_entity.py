import pytest

from entity import Monster,Boss, Wizard, Paladin, Knight

@pytest.fixture
def monster_test():
    return Monster("Gobelin",20,20,5)

@pytest.fixture
def boss_test():
    return Boss("Dracula",35,35,10)

@pytest.fixture
def player_test():
    return Knight("Boris", 60, 60, 6)

class TestMonster:
    def test_init(self,monster_test):
        assert monster_test.name == "Gobelin"
        assert monster_test.hp == 20
        assert monster_test.hp_max == 20
        assert monster_test.strength == 5

    def test_level(self,monster_test):
        assert monster_test.level(3,0.2) == (15, 15, 8, 30, 25)

    def test_attack(self,monster_test, player_test):
        assert monster_test.attack(player_test) == 55
        player_test.defense = 3
        assert monster_test.attack(player_test) == 52
        player_test.defense_s = 2
        assert monster_test.attack(player_test) == 50

    def test_death(self,monster_test, player_test):
        monster_test.level(3, 0.2)
        assert monster_test.death(player_test, 10) == 25


class TestBoss :
    def test_init(self,boss_test):
        assert boss_test.name == "Dracula"
        assert boss_test.hp == 35
        assert boss_test.hp_max == 35
        assert boss_test.strength == 10

    def test_level(self,boss_test):
        assert boss_test.level(5,0.3) == (27, 54.0, 18, 63, 100)

    def test_attack(self,boss_test, player_test):
        assert boss_test.attack(player_test) == 50
        player_test.defense = 2
        assert boss_test.attack(player_test) == 43

    def test_death(self,boss_test, player_test):
        boss_test.level(5, 0.3)
        assert boss_test.death(player_test, 50) == 77

    def test_defend(self,boss_test):
        assert boss_test.defend() == 3

@pytest.fixture
def wizard_test():
    return Wizard("claire",50,50,4)

class TestWizard:
        def test_init(self, wizard_test):
            assert wizard_test.character == "Wizard"
            assert wizard_test.shield == 3
            assert wizard_test.power_d == 2.5
            assert wizard_test.classic_attack == "Sort de base"
            assert wizard_test.special_defense == "Incantation divine"
        def test_attack_special(self,wizard_test,monster_test,boss_test):
            assert wizard_test.attack_special(monster_test, 20) == (20, 10, -2)
            monster_test.level(3, 0.2)
            monster_test.hp = 2
            assert wizard_test.attack_special(monster_test, 20) == (35, 0, -10)
            assert wizard_test.attack_special(boss_test, 20) == (20, 25, -18)
            boss_test.defense = 1
            assert wizard_test.attack_special(boss_test, 20) == (20, 22, -26)

        def test_buy(self, player_test, monkeypatch):
            player_test.gold = 300
            response = iter(["1","4","2","1","a","1","2","3"])
            monkeypatch.setattr('builtins.input', lambda x: next(response))
            player_test.buy()
            assert player_test.gold == 0
            assert player_test.potion == 7
            assert player_test.mana_potion == 2



@pytest.fixture
def paladin_test():
    return Paladin("claire",55,55,5)

class TestPaladin:
        def test_init(self, paladin_test):
            assert paladin_test.character == "Paladin"
            assert paladin_test.shield == 2
            assert paladin_test.power_d == 2
            assert paladin_test.classic_attack == "Attaque classique"
            assert paladin_test.special_defense == "Defense ultime"
        def test_attack_special(self,paladin_test,monster_test,boss_test):
            assert paladin_test.attack_special(monster_test, 20) == (20, 10, -2)
            monster_test.level(3, 0.2)
            monster_test.hp = 2
            assert paladin_test.attack_special(monster_test, 20) == (35, 0, -10)
            assert paladin_test.attack_special(boss_test, 20) == (20, 25, -18)
            boss_test.defense = 1
            assert paladin_test.attack_special(boss_test, 20) == (20, 22, -26)
    
        def test_defend(self,paladin_test):
            assert paladin_test.defend() == 2
        
        def test_defend_special(self,paladin_test):
            assert paladin_test.defend_special() == 4
        
        def test_death(self,paladin_test):
            assert paladin_test.death() == False 
        
        def test_drink_hp_potion(self, paladin_test):
            assert paladin_test.drink_hp_potion() == (55, 2)
            paladin_test.hp = 20
            assert paladin_test.drink_hp_potion() == (50, 1)

        def test_drink_mana_potion(self,paladin_test):
            assert paladin_test.drink_mana_potion() == (12, 0)
            paladin_test.mana = 1
            assert paladin_test.drink_mana_potion() == (7, -1)

        def test_level_up(self, paladin_test):
            paladin_test.experience = 40
            paladin_test.level_up()
            assert paladin_test.level == 2
            assert paladin_test.strength == 7
            assert paladin_test.hp == 65

        def test_attack(self, paladin_test, monster_test):
            assert paladin_test.attack(monster_test, 50) == (50, 15)
            monster_test.hp = 3
            assert paladin_test.attack(monster_test, 50) == (60, 0)


     