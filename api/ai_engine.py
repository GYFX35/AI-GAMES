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

class PadelAI:
    def __init__(self):
        self.state = "idle"  # Possible states: idle, serving, rallying

    def decide_action(self, game_state: str):
        """
        Decides the next action based on the game state.
        """
        if game_state == "player_serves":
            self.state = "returning"
        elif game_state == "ai_serves":
            self.state = "serving"
        elif game_state == "ball_in_play":
            self.state = "rallying"
        else:
            self.state = "idle"

        return self.get_action_in_state()

    def get_action_in_state(self):
        """
        Returns a specific action based on the current state.
        """
        if self.state == "serving":
            actions = ["serve_forehand", "serve_backhand"]
            return random.choice(actions)
        elif self.state == "returning":
            actions = ["return_forehand", "return_backhand", "lob"]
            return random.choice(actions)
        elif self.state == "rallying":
            actions = ["swing_forehand", "swing_backhand", "volley", "smash"]
            return random.choice(actions)
        else: # idle
            actions = ["move_to_position", "watch_ball"]
            return random.choice(actions)

# Example usage:
if __name__ == "__main__":
    hockey_ai = HockeyAI()

    game_state_1 = {"pock_owner": "player"}
    action_1 = hockey_ai.decide_action(game_state_1)
    print(f"Game state: {game_state_1}, AI state: {hockey_ai.state}, AI action: {action_1}")

    game_state_2 = {"pock_owner": "ai"}
    action_2 = hockey_ai.decide_action(game_state_2)
    print(f"Game state: {game_state_2}, AI state: {hockey_ai.state}, AI action: {action_2}")

    game_state_3 = {"pock_owner": "none"}
    action_3 = hockey_ai.decide_action(game_state_3)
    print(f"Game state: {game_state_3}, AI state: {hockey_ai.state}, AI action: {action_3}")

    padel_ai = PadelAI()

    padel_state_1 = "player_serves"
    padel_action_1 = padel_ai.decide_action(padel_state_1)
    print(f"Padel state: {padel_state_1}, AI action: {padel_action_1}")

    padel_state_2 = "ai_serves"
    padel_action_2 = padel_ai.decide_action(padel_state_2)
    print(f"Padel state: {padel_state_2}, AI action: {padel_action_2}")

    padel_state_3 = "ball_in_play"
    padel_action_3 = padel_ai.decide_action(padel_state_3)
    print(f"Padel state: {padel_state_3}, AI action: {padel_action_3}")
