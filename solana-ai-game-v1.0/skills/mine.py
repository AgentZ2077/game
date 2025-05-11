
class MineSkill:
    def __init__(self, player_id):
        self.player_id = player_id

    def run(self):
        import random
        minerals = ["Iron Ore", "Silver", "Gold", "Mithril", "Platinum"]
        chosen = random.choice(minerals)
        return {
            "action": "mine_result",
            "player": self.player_id,
            "item": chosen,
            "value": round(random.uniform(0.3, 5.0), 2)
        }
