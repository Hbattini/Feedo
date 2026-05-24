"""MVP rules engine constants."""

RULE_VERSION = "rules_v1"

SCORES = {
    "life_stage_match": 40,
    "condition_support": 30,
    "preferred_protein": 15,
    "preferred_texture": 10,
    "bowl_finished": 8,
    "bowl_ignored": -50,
    "vomited_after": -100,
}

EXPLOITATION_RATIO = 0.80
EXPLORATION_RATIO = 0.20
MAX_SCORE = 100
HARD_EXCLUSION_EVENT_TYPES = {"explicit_negative", "vomited_after"}
