
class GenerateGreetingSkill:
    def __init__(self, player_id):
        self.player_id = player_id

    def run(self):
        from datetime import datetime
        hour = datetime.now().hour
        greeting = "Good evening" if hour >= 18 else "Good day"
        return {
            "action": "greeting",
            "message": f"{greeting}, {self.player_id}! Welcome back."
        }
