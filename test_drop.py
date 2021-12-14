import pytest
from drop import Drop
from random import seed

@pytest.fixture
def test_drop():
    seed(1)
    return Drop({"une hâche" : 80, "une épee": 20}, 5, 5, 3)
@pytest.fixture
def test_drop2():
    seed(2)
    return Drop({"une hâche" : 70, "une épee": 20, "Potion" : 10},5, 5, 3)

class TestDrop:
    def test_initialisation(self, test_drop, test_drop2):
        assert test_drop.attack == 5
        assert test_drop.potion == 3
        assert test_drop.inventory == {"une hâche" : 80, "une épee": 20}
        assert test_drop2.potion == 3