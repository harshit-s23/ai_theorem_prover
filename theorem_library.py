"""
theorem_library.py

This module defines the PROBLEM FORMULATION for each theorem supported
by the AI Theorem Proving Assistant.

AI Concept: PROBLEM FORMULATION
--------------------------------
Before a Problem-Solving / Goal-Based Agent can search for a solution,
the problem must be formulated in terms of:
    - Initial State      (the given facts)
    - Goal                (what must be proved)
    - Actions / Operators (rule applications, supplied by the
                            Inference Engine using the Knowledge Base)

Each theorem below is expressed exactly in this form, so that
inference_engine.py and astar.py can operate on it generically rather
than through separate hard-coded logic for every theorem.
"""

from typing import Dict, List, Optional, Tuple


THEOREMS: Dict[str, Dict] = {
    "even_plus_even": {
        "id": "even_plus_even",
        "title": "1. Even + Even = Even",
        "statement": "If a and b are even numbers, prove that a + b is even.",
        "var_a_parity": "EVEN",
        "var_b_parity": "EVEN",
        "operator": "+",
        "facts": ["a is even", "b is even"],
        "goal": "a + b is even",
        "goal_type": "EVEN",
    },
    "odd_plus_odd": {
        "id": "odd_plus_odd",
        "title": "2. Odd + Odd = Even",
        "statement": "If a and b are odd numbers, prove that a + b is even.",
        "var_a_parity": "ODD",
        "var_b_parity": "ODD",
        "operator": "+",
        "facts": ["a is odd", "b is odd"],
        "goal": "a + b is even",
        "goal_type": "EVEN",
    },
    "even_times_integer": {
        "id": "even_times_integer",
        "title": "3. Even x Integer = Even",
        "statement": "If a is even and b is an integer, prove that a*b is even.",
        "var_a_parity": "EVEN",
        "var_b_parity": "INTEGER",
        "operator": "x",
        "facts": ["a is even", "b is an integer"],
        "goal": "a * b is even",
        "goal_type": "EVEN",
    },
    "odd_times_odd": {
        "id": "odd_times_odd",
        "title": "4. Odd x Odd = Odd",
        "statement": "If a and b are odd numbers, prove that a*b is odd.",
        "var_a_parity": "ODD",
        "var_b_parity": "ODD",
        "operator": "x",
        "facts": ["a is odd", "b is odd"],
        "goal": "a * b is odd",
        "goal_type": "ODD",
    },
    "even_plus_odd": {
        "id": "even_plus_odd",
        "title": "5. Even + Odd = Odd",
        "statement": "If a is even and b is odd, prove that a + b is odd.",
        "var_a_parity": "EVEN",
        "var_b_parity": "ODD",
        "operator": "+",
        "facts": ["a is even", "b is odd"],
        "goal": "a + b is odd",
        "goal_type": "ODD",
    },
}


def get_theorem(theorem_id: str) -> Optional[Dict]:
    """
    Retrieve a theorem specification by its id.
    Returns None if the theorem id is not present in the Knowledge Base
    -- this is how the application detects unsupported theorems.
    """
    return THEOREMS.get(theorem_id)


def list_theorem_titles() -> List[Tuple[str, str]]:
    """
    Return (id, title) pairs for populating the UI dropdown.

    A single deliberately UNSUPPORTED entry ("unsupported_demo") is
    appended so the application can visibly demonstrate its
    limitation-handling behaviour for theorem patterns that do not
    exist in the Knowledge Base.
    """
    titles = [(tid, t["title"]) for tid, t in THEOREMS.items()]
    titles.append(("unsupported_demo", "6. Prime + Prime = ? (Not in Knowledge Base)"))
    return titles
