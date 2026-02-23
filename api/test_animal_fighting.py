import pytest
from api.ai_engine import AnimalFightingAI

def test_animal_fighting_ai_ready():
    ai = AnimalFightingAI()
    action = ai.decide_action("ready", "lion", "tiger")
    assert "lion" in action.lower()
    assert "tiger" in action.lower()
    assert "ready to strike" in action.lower()

def test_animal_fighting_ai_attacking_lion():
    ai = AnimalFightingAI()
    action = ai.decide_action("attacking", "lion", "tiger")
    assert "AI Tip: Use" in action
    # Check if one of the lion's actions is in the response
    lion_actions = ["Powerful Paw Swipe", "Crushing Bite", "Intimidating Roar"]
    assert any(la in action for la in lion_actions)

def test_animal_fighting_ai_attacking_tiger():
    ai = AnimalFightingAI()
    action = ai.decide_action("attacking", "tiger", "lion")
    assert "AI Tip: Use" in action
    # Check if one of the tiger's actions is in the response
    tiger_actions = ["Ambush Strike", "Precision Clawing", "Quick Leap"]
    assert any(ta in action for ta in tiger_actions)

def test_animal_fighting_ai_defending():
    ai = AnimalFightingAI()
    action = ai.decide_action("defending", "lion", "tiger")
    assert "AI Tip:" in action
    defending_actions = ["Dodge", "Counter-attack", "Block with Paws"]
    assert any(da in action for da in defending_actions)

def test_animal_fighting_ai_near_victory():
    ai = AnimalFightingAI()
    action = ai.decide_action("near_victory", "lion", "tiger")
    assert "tiger" in action.lower()
    assert "final blow" in action.lower()
