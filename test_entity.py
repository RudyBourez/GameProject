import pytest

from entity import Monster,Boss,Player

@pytest.fixture
def monster_test():
    return Monster("Gobelin",20,20,5)

@pytest.fixture
def boss_test():
    return Boss("Dracula",35,35,10)

class TestMonster:
    def test_init(self,monster_test):
        assert monster_test.name == "Gobelin"
        assert monster_test.hp == 20
        assert monster_test.hp_max == 20
        assert monster_test.strength == 5

    def test_level(self,monster_test):
        assert monster_test.level(3,0.2) == (15, 15, 8, 30, 25)

    def test_attack(self,monster_test, player_test):
        assert monster_test.attack(player_test) == 45
        player_test.defense = 3
        assert monster_test.attack(player_test) == 42

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
        assert boss_test.level(5,0.3) == (27, 27, 18, 63, 100)

    def test_attack(self,boss_test, player_test):
        assert boss_test.attack(player_test) == 40
        player_test.defense = 2
        assert boss_test.attack(player_test) == 33

    def test_death(self,boss_test, player_test):
        boss_test.level(5, 0.3)
        assert boss_test.death(player_test, 50) == 77

    def test_defend(self,boss_test):
        assert boss_test.defend() == 3

@pytest.fixture
def player_test():
    return Player("claire",50,50,4)
@pytest.fixture
def player_test_defense():
    player_test_defense = Player("claire",50,50,4)
    player_test_defense.defense = 2
    return player_test_defense

class Test_Player:
    def test_init(self, player_test):
        assert player_test.strength == 4
        assert player_test.name == "claire"
        
    def test_attack(self,player_test, monster_test,boss_test):
        assert player_test.attack(monster_test, 20) == (20, 15)
        monster_test.level(3, 0.2)
        monster_test.hp = 2
        assert player_test.attack(monster_test, 20) == (35, 0)
        assert player_test.attack(boss_test, 20) == (20, 30)
        boss_test.defense = 1
        assert player_test.attack(boss_test, 20) == (20, 27)
    
    
    
    
    def test_defend(self,player_test,player_test_defense):
        assert player_test.defend() == 3
        assert player_test_defense.defend() == 2
        
    def test_death(self,player_test):
        assert player_test.death() == False
        
    def test_drink_potion(self,player_test):
        assert player_test.drink_potion() == (50, 2) # 返回多个值时 需要括号
        player_test.hp = 10
        assert player_test.drink_potion() == (30, 1)
     