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

class InvestigativeAI:
    def __init__(self):
        self.state = "idle"  # Possible states: idle, investigating, analyzing, secure_scene

    def decide_action(self, game_state: str):
        """
        Decides the next action based on the investigation state.
        """
        if game_state == "clue_found":
            self.state = "analyzing"
        elif game_state == "suspect_spotted":
            self.state = "chasing"
        elif game_state == "scene_entered":
            self.state = "investigating"
        elif game_state == "threat_detected":
            self.state = "secure_scene"
        else:
            self.state = "idle"

        return self.get_action_in_state()

    def get_action_in_state(self):
        """
        Returns a specific action based on the current investigation state.
        """
        if self.state == "investigating":
            actions = ["search_for_fingerprints", "take_photos", "collect_dna_sample"]
            return random.choice(actions)
        elif self.state == "analyzing":
            actions = ["run_ballistics", "cross_reference_database", "decrypt_files"]
            return random.choice(actions)
        elif self.state == "chasing":
            actions = ["pursue_suspect", "call_for_backup", "deploy_drone"]
            return random.choice(actions)
        elif self.state == "secure_scene":
            actions = ["establish_perimeter", "interview_witnesses", "check_surveillance"]
            return random.choice(actions)
        else: # idle
            actions = ["patrol_area", "review_case_files"]
            return random.choice(actions)

class ShovelMasterAI:
    """
    Stateless AI engine for Shovel Master game.
    """
    def decide_action(self, game_state: str):
        """
        Decides the next action based on the shoveling state.
        Now stateless - state is passed in and returned in the action description.
        """
        if game_state in ["shovel_ready", "shoveling"]:
            actions = ["dig_dirt", "lift_shovel", "balance_load"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} (State: Shoveling)"
        elif game_state in ["shovel_full", "dumping"]:
            actions = ["move_to_truck", "tilt_shovel", "empty_shovel"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} (State: Dumping)"
        elif game_state == "truck_full":
            actions = ["celebrate", "signal_next_truck", "rest"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} (State: Truck Full)"
        else:
            actions = ["wait_for_truck", "sharpen_shovel", "check_surroundings"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} (State: Idle)"

class AnimalRunningAI:
    """
    Stateless AI engine for Animal Running Competition game.
    """
    def decide_action(self, game_state: str, animal_type: str):
        """
        Decides the next action based on the running state and animal type.
        """
        if game_state == "running":
            actions = ["sprint", "conserve_energy", "check_competitors"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} ({animal_type} is running)"
        elif game_state == "obstacle_ahead":
            if animal_type == "lion":
                actions = ["jump_over", "roar_to_clear", "sidestep"]
            elif animal_type == "tiger":
                actions = ["pounce_over", "stealth_around", "climb_over"]
            else:
                actions = ["jump", "dodge", "brake"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} ({animal_type} encountered an obstacle)"
        elif game_state == "finish_line_near":
            actions = ["final_burst", "block_competitor", "maintain_speed"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} ({animal_type} is near the finish line)"
        else:
            actions = ["stretch", "focus", "wait_for_signal"]
            recommendation = random.choice(actions)
            return f"Action: {recommendation} ({animal_type} is ready)"

class TreePlantingAI:
    """
    AI engine for Tree Planting AR game.
    """
    def decide_action(self, game_state: str, area: str):
        """
        Decides the next action based on the planting state and area.
        """
        if game_state == "choosing_tree":
            if area == "forest":
                actions = ["Plant Oak for longevity", "Plant Pine for fast growth", "Ensure enough spacing"]
            elif area == "desert":
                actions = ["Plant Cactus to conserve water", "Plant Palm near oases", "Use drought-resistant seeds"]
            elif area == "city":
                actions = ["Plant Oak for shade", "Use planters for limited space", "Choose trees that filter pollution"]
            else:
                actions = ["Select a tree", "Check soil quality", "Look for sunlight"]

            recommendation = random.choice(actions)
            return f"AI Tip: {recommendation} (Area: {area})"

        elif game_state == "planting":
            actions = ["Dig a deep hole", "Water the sapling", "Add compost"]
            recommendation = random.choice(actions)
            return f"AI Guidance: {recommendation}"

        else:
            return "AI: Ready to help you reforest!"

class PapayaPeelingAI:
    """
    AI engine for Papaya Peeling AR game.
    """
    def decide_action(self, game_state: str, peeling_quality: float):
        """
        Decides the next action based on the peeling state and quality.
        """
        if game_state == "peeling":
            if peeling_quality > 0.8:
                return "AI Tip: Perfect technique! Keep going."
            elif peeling_quality > 0.5:
                return "AI Tip: Good progress, but watch your depth."
            else:
                return "AI Tip: Be careful not to waste too much fruit!"
        elif game_state == "serving":
            return "AI Tip: Place it gently on the table for the perfect presentation."
        else:
            return "AI: Ready to help you peel the perfect papaya!"

class MoneyClimbingAI:
    """
    AI engine for Money Jumping and Climbing AR game.
    """
    def decide_action(self, game_state: str, height: float, money_collected: int):
        """
        Decides the next action based on the climbing state, current height, and money collected.
        """
        if game_state == "climbing":
            if height > 50:
                actions = ["Watch your step, it's getting high!", "Look for a stable branch", "The air is thin, take a breather"]
            elif height > 20:
                actions = ["Nice climb! Keep going.", "Check for money on the side branches", "You're halfway there!"]
            else:
                actions = ["Start your ascent!", "Look for the easiest path up", "Don't forget to collect money"]

            recommendation = random.choice(actions)
            return f"AI Climbing Tip: {recommendation} (Height: {height}m)"

        elif game_state == "jumping":
            if money_collected > 100:
                actions = ["You're a money magnet!", "Try a double jump for higher coins", "Keep that momentum!"]
            else:
                actions = ["Jump higher to reach more money!", "Timing is everything", "Aim for the golden coins"]

            recommendation = random.choice(actions)
            return f"AI Jumping Tip: {recommendation} (Money: ${money_collected})"

        else:
            return "AI: Ready to help you climb and jump to wealth!"

class AnimalFightingAI:
    """
    Stateless AI engine for Animal Fighting AR game.
    """
    def decide_action(self, game_state: str, animal_type: str, opponent_type: str):
        """
        Decides the next action based on the fighting state and animal types.
        """
        if game_state == "ready":
            return f"AI: The {animal_type} is sizing up the {opponent_type}. Ready to strike!"

        if game_state == "attacking":
            if animal_type == "lion":
                actions = ["Powerful Paw Swipe", "Crushing Bite", "Intimidating Roar"]
            elif animal_type == "tiger":
                actions = ["Ambush Strike", "Precision Clawing", "Quick Leap"]
            else:
                actions = ["Basic Attack", "Charge", "Bite"]
            recommendation = random.choice(actions)
            return f"AI Tip: Use {recommendation}!"

        if game_state == "defending":
            actions = ["Dodge", "Counter-attack", "Block with Paws"]
            recommendation = random.choice(actions)
            return f"AI Tip: {recommendation} now!"

        if game_state == "near_victory":
            return f"AI: The {opponent_type} is weakening! Deliver the final blow!"

        return f"AI: Stay focused and watch the {opponent_type}'s movements."

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
