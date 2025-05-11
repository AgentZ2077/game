
from skills.greet import GenerateGreetingSkill
from skills.brew import BrewItemSkill

class TavernkeeperAgent:
    def __init__(self, player_id):
        self.player_id = player_id

    def act(self):
        greeting = GenerateGreetingSkill(self.player_id).run()
        item = BrewItemSkill(self.player_id).run()
        return {
            "npc": "tavernkeeper",
            "responses": [greeting, item]
        }
