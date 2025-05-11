
from skills.mine import MineSkill
from skills.brew import BrewItemSkill
from skills.greet import GenerateGreetingSkill

def test_mine():
    result = MineSkill("Bob").run()
    assert "item" in result and result["value"] >= 0.3

def test_brew():
    result = BrewItemSkill("Alice").run()
    assert result["status"] == "minted"

def test_greet():
    result = GenerateGreetingSkill("Alice").run()
    assert "Welcome" in result["message"]
