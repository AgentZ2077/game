
from skills.mine import MineSkill

class MinerAgent:
    def __init__(self, player_id):
        self.player_id = player_id

    def act(self):
        skill = MineSkill(self.player_id)
        return skill.run()
