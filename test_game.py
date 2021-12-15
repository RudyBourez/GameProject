# from entity import Player,Boss,Monster
# from game import Game
# import pytest

# @pytest.fixture
# def monster_test():
#     return Monster("Gobelin",20,20,5)

# @pytest.fixture
# def boss_test():
#     return Boss("Dracula",35,35,10)

# @pytest.fixture
# def player_test():
#     return Player("claire",50,50,4)

# class TestGame:
#     def test_initialisation(self,monkeypatch):
#         monkeypatch.setattr('builtins.input', lambda x : "n")
#         game_test = Game()
#         assert game_test.floor == 1
#         assert game_test.running == False
#     def test_quit(self,monkeypatch):
#         response = iter(["y", "Rudy", "d"])
#         monkeypatch.setattr('builtins.input', lambda x: next(response))
#         game_test = Game()
#         assert game_test.floor == 1
#         assert game_test.running == False
#         assert game_test.score == 0

#     def test_fight(self, monkeypatch):
#         response = iter(["t","y", "Rudy", "c", "a", "3", "2", "1", "1", "1", "1", "1","1","1", "b", "1", "1", "1", "1", "1", "1", "a", "1", "1", "1"])
#         monkeypatch.setattr('builtins.input', lambda x: next(response))
#         game_test = Game()
#         assert game_test.floor == 3
#         assert game_test.running == False
#         assert game_test.score == 26

#     def test_load(self, monkeypatch):
#         response = iter(["t","l", "c", "a", "3", "2", "1", "1", "1", "1", "1","1","1", "d", "1"])
#         monkeypatch.setattr('builtins.input', lambda x: next(response))
#         game_test = Game()
#         assert game_test.floor == 2
#         assert game_test.running == False
#         assert game_test.score == 13