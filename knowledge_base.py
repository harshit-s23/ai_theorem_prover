"""
knowledge_base.py

This module represents the KNOWLEDGE BASE component of the
Knowledge-Based AI Theorem Proving Assistant.

AI Concept: KNOWLEDGE BASE
---------------------------
In a Knowledge-Based Agent, the Knowledge Base (KB) is a structured
store of facts and rules about the domain (here: elementary number
theory). The Inference Engine queries this Knowledge Base to decide
which rule to apply at each stage of reasoning.

Important design principle: the Knowledge Base contains ONLY
declarative knowledge (facts and rules). It contains NO control logic
(no "how to reason" code) -- that responsibility belongs entirely to
the Inference Engine (inference_engine.py). This separation is a core
idea taught for Knowledge-Based Agents.
"""

from typing import List, Dict, Optional


# ---------------------------------------------------------------------
# DEFINITION RULES
# These rules define what it means for a number to be EVEN or ODD.
# They correspond to first-order logic rules of the form:
#     EVEN(x) -> x = 2k
#     ODD(x)  -> x = 2k + 1
# ---------------------------------------------------------------------
DEFINITION_RULES: Dict[str, Dict] = {
    "EVEN": {
        "name": "DEF-EVEN",
        "rule": "EVEN(x) -> x = 2k",
        "description": "An even number can always be written in the form "
                        "2k, where k is an integer.",
    },
    "ODD": {
        "name": "DEF-ODD",
        "rule": "ODD(x) -> x = 2k + 1",
        "description": "An odd number can always be written in the form "
                        "2k + 1, where k is an integer.",
    },
}


# ---------------------------------------------------------------------
# COMBINATION RULES
# These rules capture how the parity (EVEN/ODD) of a result depends on
# the parity of its operands, for the two operations used in this
# prototype: addition (+) and multiplication (x).
# ---------------------------------------------------------------------
COMBINATION_RULES: List[Dict] = [
    {
        "id": "R1",
        "name": "EVEN + EVEN -> EVEN",
        "condition": ("EVEN", "+", "EVEN"),
        "conclusion": "EVEN",
        "rule": "EVEN + EVEN -> EVEN",
        "description": "The sum of two even numbers is always even.",
    },
    {
        "id": "R2",
        "name": "ODD + ODD -> EVEN",
        "condition": ("ODD", "+", "ODD"),
        "conclusion": "EVEN",
        "rule": "ODD + ODD -> EVEN",
        "description": "The sum of two odd numbers is always even.",
    },
    {
        "id": "R3",
        "name": "EVEN + ODD -> ODD",
        "condition": ("EVEN", "+", "ODD"),
        "conclusion": "ODD",
        "rule": "EVEN + ODD -> ODD",
        "description": "The sum of an even number and an odd number is "
                        "always odd.",
    },
    {
        "id": "R4",
        "name": "EVEN x INTEGER -> EVEN",
        "condition": ("EVEN", "x", "INTEGER"),
        "conclusion": "EVEN",
        "rule": "EVEN x INTEGER -> EVEN",
        "description": "The product of an even number and any integer is "
                        "always even.",
    },
    {
        "id": "R5",
        "name": "ODD x ODD -> ODD",
        "condition": ("ODD", "x", "ODD"),
        "conclusion": "ODD",
        "rule": "ODD x ODD -> ODD",
        "description": "The product of two odd numbers is always odd.",
    },
]


def get_definition_rule(parity: str) -> Dict:
    """Return the definition rule (EVEN or ODD) for a given parity."""
    if parity not in DEFINITION_RULES:
        raise KeyError(f"No definition rule found for parity: {parity}")
    return DEFINITION_RULES[parity]


def find_combination_rule(parity_a: str, operator: str, parity_b: str) -> Optional[Dict]:
    """
    Search the Knowledge Base for a combination rule whose condition
    matches (parity_a, operator, parity_b).

    This is the core PATTERN MATCHING mechanism an Inference Engine
    uses to retrieve applicable rules from a Knowledge Base. Returns
    None if no such rule exists (i.e. the pattern is unsupported).
    """
    for rule in COMBINATION_RULES:
        if rule["condition"] == (parity_a, operator, parity_b):
            return rule
    return None


def get_rule_details(identifier: str) -> Optional[Dict]:
    """
    Look up any rule (definition or combination) in the Knowledge Base
    by its name (e.g. 'DEF-EVEN') or id (e.g. 'R1'), for UI display.
    """
    for rule in DEFINITION_RULES.values():
        if rule["name"] == identifier:
            return rule
    for rule in COMBINATION_RULES:
        if rule["id"] == identifier or rule["name"] == identifier:
            return rule
    return None


def get_all_rules_summary() -> List[str]:
    """Return a human-readable list of every rule stored in the Knowledge Base."""
    summary = []
    for d in DEFINITION_RULES.values():
        summary.append(f"{d['name']}: {d['rule']}  --  {d['description']}")
    for r in COMBINATION_RULES:
        summary.append(f"{r['id']}: {r['rule']}  --  {r['description']}")
    return summary
