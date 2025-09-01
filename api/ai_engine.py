import random

class HockeyAI:
    def __init__(self):
        self.state = "idle"  # Possible states: idle, attacking, defending

    def decide_action(self, game_state: dict):
        """
        Decides the next action based on the game state.
        For now, the game state is a simple dictionary.
        """
        puck_owner = game_state.get("puck_owner")

        if puck_owner == "player":
            self.state = "defending"
        elif puck_owner == "ai":
            self.state = "attacking"
        else:
            self.state = "idle"

        return self.get_action_in_state()

    def get_action_in_state(self):
        """
        Returns a specific action based on the current state.
        """
        if self.state == "attacking":
            actions = ["skate_forward", "pass_puck", "shoot_puck"]
            return random.choice(actions)
        elif self.state == "defending":
            actions = ["skate_back", "check_player", "block_shot"]
            return random.choice(actions)
        else: # idle
            actions = ["skate_around", "look_for_puck"]
            return random.choice(actions)

# Example usage:
if __name__ == "__main__":
    ai = HockeyAI()

    game_state_1 = {"puck_owner": "player"}
    action_1 = ai.decide_action(game_state_1)
    print(f"Game state: {game_state_1}, AI state: {ai.state}, AI action: {action_1}")

    game_state_2 = {"puck_owner": "ai"}
    action_2 = ai.decide_action(game_state_2)
    print(f"Game state: {game_state_2}, AI state: {ai.state}, AI action: {action_2}")

    game_state_3 = {"puck_owner": "none"}
    action_3 = ai.decide_action(game_state_3)
    print(f"Game state: {game_state_3}, AI state: {ai.state}, AI action: {action_3}")
