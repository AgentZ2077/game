
class BrewItemSkill:
    def __init__(self, player_id, item_name="elven_wine"):
        self.player_id = player_id
        self.item_name = item_name

    def run(self):
        return {
            "action": "brew_result",
            "player": self.player_id,
            "item": self.item_name,
            "status": "minted",
            "nft_id": f"nft_{self.player_id}_{self.item_name}"
        }
