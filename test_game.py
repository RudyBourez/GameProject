from entity import Boss,Monster, Knight, Paladin, Wizard
from game import Game
import pytest

@pytest.fixture
def monster_test():
    return Monster("Gobelin",20,20,5)

@pytest.fixture
def boss_test():
    return Boss("Dracula",35,35,10)

@pytest.fixture
def wizard_test():
    return Wizard("claire",50,50,4)

@pytest.fixture
def paladin_test():
    return Paladin("claire",55,55,5)

@pytest.fixture
def knight_test():
    return Knight("claire",60,60,6)

class TestGame:
    def test_initialisation(self,monkeypatch):
        monkeypatch.setattr('builtins.input', lambda x : "n")
        game_test = Game()
        assert game_test.floor == 1
        assert game_test.running == False
    def test_quit(self,paladin_test,monkeypatch):
        response = iter(["y", "claire","p", "d"])
        monkeypatch.setattr('builtins.input', lambda x: next(response))
        game_test = Game()
        assert game_test.floor == 1
        assert game_test.running == False
        assert game_test.score == 0
        assert paladin_test.character == "Paladin"

    def test_load(self, monkeypatch):
        response = iter(["l","d"])
        monkeypatch.setattr('builtins.input', lambda x: next(response))
        game_test = Game()
        assert game_test.floor == 1
        assert game_test.running == False
        assert game_test.score == 0
        response = iter(["y","claire","p","d"])
        monkeypatch.setattr('builtins.input', lambda x: next(response))
        game_test = Game()
        response = iter(["l","d"])
        monkeypatch.setattr('builtins.input', lambda x: next(response))
        game_test = Game()
        assert game_test.floor == 1
        assert game_test.running == False
        assert game_test.score == 0


    def test_fight(self, monkeypatch):
        response = iter(["t","y", "Rudy","w", "c", "a","2","1","3", "2", "1","2", "1", "1", "1", "1","1","1","d"])
        monkeypatch.setattr('builtins.input', lambda x: next(response))
        game_test = Game()
        assert game_test.floor == 2
        assert game_test.running == False
        assert game_test.score == 11

    def test_defense_s(self, monkeypatch):
        response = iter(["t","y", "Rudy","c", "a", "a","1", "1", "1","1", "2", "2", "1", "1","1","1","d"])
        monkeypatch.setattr('builtins.input', lambda x: next(response))
        game_test = Game()
        assert game_test.floor == 2
        assert game_test.running == False
        assert game_test.score == 11

