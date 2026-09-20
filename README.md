# AI Theorem Proving Assistant

A small **Knowledge-Based AI prototype** for automated theorem proving,
built for **CIA-1 Part 5 (Implementation of a small part of a system
using an AI tool)**.

![System Architecture](assets/architecture.png)

---

## 1. Project Title

**AI Theorem Proving Assistant** -- A Knowledge-Based AI Prototype for
Automated Mathematical Reasoning.

---

## 2. Problem Statement

The selected research paper, *"Artificial Intelligence Technology in
Mathematical and Engineering Applications"*, discusses several AI
applications in mathematics, one of which is **Automated Theorem
Proving (ATP)** -- the use of AI techniques (knowledge representation,
inference, and search) to construct formal proofs of mathematical
statements automatically.

Full-scale automated theorem provers (e.g. Coq, Lean, Prover9) are
extremely complex research systems. This project implements a **small,
transparent, educational prototype** that demonstrates the *same
underlying AI concepts* -- Knowledge Base, Inference Engine, and
Heuristic Search -- on a restricted, well-defined class of theorems:
elementary **parity proofs** (properties of even and odd numbers).

---

## 3. Motivation

- Automated theorem proving is one of the oldest and most fundamental
  applications of AI, directly connecting **Knowledge Representation**,
  **Inference**, and **Search** -- three pillars of the AI syllabus.
- A full ATP system is infeasible to build and demonstrate within the
  scope of a CIA assignment. A small, faithful prototype lets us show
  *how* such a system works internally, rather than treating it as a
  black box.
- Building it ourselves (instead of calling an external AI/theorem-proving
  API) satisfies the "implementation using an AI tool/technique" CIA
  requirement honestly, without pretending to have solved general
  theorem proving.

---

## 4. Objectives

1. Represent elementary number-theory knowledge as an explicit,
   inspectable **Knowledge Base**.
2. Implement a small **Inference Engine** that performs forward
   chaining: Facts -> Rule Selection -> Inference -> New State -> Goal
   Test -> Proof.
3. Demonstrate **A\* Search** over the space of partial proofs, with
   real g(n), h(n), f(n) computation (reusing the A\* concept from CIA
   Part 2).
4. Provide **Explainable AI**: for every proof step, explain *why*
   that particular rule was selected.
5. Build a clear, demonstrable **Streamlit** UI suitable for a live
   college presentation.
6. Be explicit about the system's **limitations** -- it must never
   claim to solve theorems outside its Knowledge Base.

---

## 5. AI Concepts Demonstrated

| Concept | Where it appears |
|---|---|
| Knowledge-Based Agent | Overall system design |
| Knowledge Base | `knowledge_base.py` |
| Inference Engine | `inference_engine.py` |
| Problem Formulation | `theorem_library.py` (facts, goal) |
| Goal-Based Agent | Goal test in the Inference Engine |
| Search / A\* Search | `astar.py` |
| Problem-Solving Agent | The full pipeline in `app.py` |
| Learning Agent (concept only) | See *Future Scope* -- KB is designed to be extensible with new rules over time |
| Performance Measure | Correct, step-by-step, explainable proof (shown in sidebar PEAS box) |
| PEAS | Shown in the app sidebar |
| Explainable AI | Section 7 of the app, and the `reasoning` field attached to every proof step |

---

## 6. System Architecture

```
User Input
    |
    v
Problem Formulation   (theorem_library.py)
    |
    v
Knowledge Base         (knowledge_base.py)
    |
    v
Inference Engine        (inference_engine.py)
    |
    v
A* Search               (astar.py)
    |
    v
Goal Test
    |
    v
Proof
    |
    v
Explanation (Explainable AI)
```

See `assets/architecture.png` for the visual diagram (also rendered at
the top of this README and inside the app itself).

---

## 7. Knowledge Base

Implemented in `knowledge_base.py`, kept strictly **separate** from the
user interface and from the reasoning logic. It stores only
declarative knowledge:

**Definition rules**
```
EVEN(x) -> x = 2k
ODD(x)  -> x = 2k + 1
```

**Combination rules**
```
EVEN + EVEN      -> EVEN
ODD  + ODD       -> EVEN
EVEN + ODD       -> ODD
EVEN x INTEGER   -> EVEN
ODD  x ODD       -> ODD
```

The Inference Engine queries this Knowledge Base by **pattern
matching** on `(parity_a, operator, parity_b)` -- it never guesses or
hard-codes a rule outside this table.

---

## 8. Inference Engine

Implemented in `inference_engine.py`. For every theorem it performs
the classic reasoning cycle taught in the syllabus:

```
Facts -> Rule Selection -> Inference -> New State -> Goal Test -> Proof
```

Concretely, for each theorem the engine:

1. Reads the initial **facts** (from Problem Formulation).
2. Selects and applies the **definition rule** for each variable's
   parity (e.g. `a = 2m`).
3. **Substitutes** these definitions into the theorem's expression
   (`a + b` or `a * b`).
4. Performs **algebraic simplification** (expansion, factoring) to
   reduce the expression back to the canonical form `2k` or `2k + 1`.
5. Matches the simplified form against a **combination rule** in the
   Knowledge Base.
6. Runs a **goal test**: does the derived parity match the theorem's
   required goal?
7. Returns the full list of proof steps, the final conclusion, the
   proof status (`PROVED` / `NOT_PROVED` / `UNSUPPORTED`), and the
   number of steps taken.

Each step is a structured record (`step_no`, `action`, `rule_used`,
`reasoning`, `result`) -- **not** a single hard-coded paragraph.

---

## 9. A\* Search

Implemented in `astar.py`. The search space is defined as:

- **State**: a partial proof (one node per proof step generated by the
  Inference Engine).
- **Action**: applying the next inference rule to move to the next
  proof state.
- **g(n)**: number of proof steps already taken.
- **h(n)**: estimated (here, exact and therefore admissible/consistent)
  number of proof steps remaining until the goal.
- **f(n) = g(n) + h(n)**.

The algorithm uses a genuine priority queue (`heapq`), an open list, a
closed (`visited`) list, and an explicit goal test -- it is not a
lookup table of pre-written numbers. Because this small Knowledge Base
produces exactly one reasoning path per theorem, the resulting search
graph is a simple chain, so A\* confirms that the one available path
is optimal (constant f(n) throughout, as expected for a consistent
heuristic).

Example output table for *Even + Even = Even*:

| Node | Proof State | g(n) | h(n) | f(n) |
|---|---|---|---|---|
| Start | Given: a is even, b is even | 0 | 5 | 5 |
| S1 | a = 2m | 1 | 4 | 5 |
| S2 | b = 2n | 2 | 3 | 5 |
| S3 | a + b = 2m + 2n | 3 | 2 | 5 |
| S4 | a + b = 2(m+n) | 4 | 1 | 5 |
| Goal | a + b = 2(m+n) | 5 | 0 | 5 |

---

## 10. Explainable AI

Every proof step carries a `reasoning` field explaining **why** that
rule was chosen (e.g. *"Because a is even, apply the Knowledge Base
definition EVEN(x) -> x = 2k: a = 2m."*). Section 7 of the app
("Explainable AI") additionally explains, in plain language, why this
particular chain of rules -- and no other -- was selected: because it
is the only sequence whose conditions match the given facts in the
Knowledge Base.

---

## 11. Supported Theorems

| # | Theorem | Goal |
|---|---|---|
| 1 | If a and b are even, prove a + b is even | EVEN |
| 2 | If a and b are odd, prove a + b is even | EVEN |
| 3 | If a is even and b is an integer, prove a·b is even | EVEN |
| 4 | If a and b are odd, prove a·b is odd | ODD |
| 5 | If a is even and b is odd, prove a + b is odd | ODD |

A sixth dropdown option, *"Prime + Prime = ? (Not in Knowledge Base)"*,
is included deliberately to demonstrate the application's
**limitation-handling**: it is not covered by any rule, so the app
reports this honestly instead of fabricating a proof.

---

## 12. Installation Instructions

**Requirements:** Python 3.10+

```bash
cd ai_theorem_prover
pip install -r requirements.txt
```

No API keys, no paid services, and no internet connection are
required -- the application works fully offline after installation.

---

## 13. How to Run

```bash
streamlit run app.py
```

Streamlit will print a local URL (typically `http://localhost:8501`)
-- open it in your browser.

---

## 14. Demonstration Procedure

1. Launch the app with `streamlit run app.py`.
2. In the sidebar, either:
   - select a theorem from the dropdown and click **Prove Theorem**, or
   - click **Run Demo Mode (Even + Even)** for a fully automatic walkthrough.
3. Scroll through Sections 1-8 in the main area: Problem Statement,
   Initial State, Knowledge Base, A\* Search table, Proof Steps, Final
   Result, Explainable AI, and System Architecture.
4. Select the sixth ("Prime + Prime") option and click **Prove
   Theorem** to demonstrate limitation-handling.
5. Click **Reset** to clear the screen and start again.

---

## 15. Limitations

- This prototype supports **only** the five predefined parity theorem
  patterns stored in its Knowledge Base -- it is **not** a
  general-purpose theorem prover.
- It does not parse arbitrary user-typed theorems or free-form natural
  language; theorems are chosen from a fixed dropdown.
- The proof search space is a simple linear chain (no branching), by
  design, to keep the A\* demonstration simple and deterministic for a
  short classroom demo.
- It performs no formal verification against a proof assistant kernel
  (e.g. Lean/Coq) -- correctness is guaranteed only for the fixed,
  hand-verified rule set in `knowledge_base.py`.

---

## 16. Future Scope

- Extend the Knowledge Base with more rule families (e.g. divisibility,
  inequalities, basic set theory) without changing the Inference
  Engine or A\* Search code, since both already operate generically.
- Add a **Learning Agent** layer that records which rules were used
  most often (a simple performance log) and could, in principle,
  reorder rule search priority over time.
- Allow limited natural-language input, parsed into the existing
  `(parity, operator, parity)` fact structure.
- Introduce real branching in the search graph once multiple valid
  proof strategies exist per theorem, to make the A\* demonstration
  richer.

---

## 2-Minute CIA Demonstration Script

1. **(0:00-0:15) Introduce the problem:** "My paper covers AI in
   mathematical applications; I picked Automated Theorem Proving. This
   is a small Knowledge-Based prototype that proves parity theorems
   using a Knowledge Base, an Inference Engine, and A\* Search."
2. **(0:15-0:25)** In the sidebar, select **"1. Even + Even = Even"**.
3. **(0:25-0:35)** Point out **Section 2: Initial State** -- the facts
   (`a is even`, `b is even`) and the goal (`a + b is even`).
4. **(0:35-0:50)** Point out **Section 3: Knowledge Base** -- show the
   retrieved rules (`DEF-EVEN`, `R1: EVEN + EVEN -> EVEN`) and expand
   "View the complete Knowledge Base".
5. **(0:50-0:55)** Click **Prove Theorem** (if not already run).
6. **(0:55-1:15)** Point out **Section 4: A\* Search table** -- explain
   g(n), h(n), f(n) briefly, and that A\* found the Goal node.
7. **(1:15-1:35)** Point out **Section 5: Proof Steps** -- expand one
   or two steps to show the rule, reasoning, and result.
8. **(1:35-1:45)** Point out **Section 7: Explainable AI** -- read one
   sentence explaining why the proof took this path.
9. **(1:45-1:55)** Point out **Section 6: Final Result** --
   "✓ THEOREM PROVED".
10. **(1:55-2:00)** Switch the dropdown to **"6. Prime + Prime = ?"**,
    click **Prove Theorem**, and show the honest limitation message:
    "Unable to prove this theorem with the current knowledge base."

---

## Likely Viva Questions and Answers

**Q1. Why did you model this as a Knowledge-Based Agent?**
A Knowledge-Based Agent maintains an internal representation of
domain facts and rules (a Knowledge Base) and uses an Inference Engine
to derive new facts and decisions from it. Theorem proving is
naturally suited to this model because a proof *is* a sequence of
facts derived by applying known rules -- exactly the Knowledge-Based
Agent cycle of "perceive facts -> consult Knowledge Base -> infer ->
act (produce proof step)".

**Q2. Why did you also describe it as a Goal-Based Agent?**
Because the agent's behaviour is driven by an explicit **goal**
(e.g. "a + b is even") rather than a fixed action mapping. At every
stage the Inference Engine checks whether the current derived state
satisfies this goal (the **goal test**), and only reports success when
it does -- this goal-directed control is the defining feature of a
Goal-Based Agent.

**Q3. Why did you use A\* Search here, and how do g(n)/h(n)/f(n) work
in this context?**
A\* was already used in my CIA Part 2, so I reused the same concept to
show it can also apply to proof search: each state is a partial proof,
g(n) counts proof steps taken so far, and h(n) estimates the steps
still needed (which is exact here because the Inference Engine already
determined the whole chain, making the heuristic admissible and
consistent). A\* always expands the lowest-f(n) node, guaranteeing the
optimal (shortest) proof path is found -- which in this small,
non-branching Knowledge Base is the single available path.

**Q4. What exactly is the Knowledge Base in your system?**
It is `knowledge_base.py`, a Python module containing only declarative
data: definition rules (`EVEN(x) -> x = 2k`, `ODD(x) -> x = 2k+1`) and
combination rules (`EVEN + EVEN -> EVEN`, etc.). It has no control
logic of its own -- the Inference Engine is solely responsible for
deciding *when* and *how* to use these rules. This separation of
knowledge from reasoning is a core Knowledge-Based Agent design
principle.

**Q5. What is the Inference Engine, and how does it differ from the
Knowledge Base?**
The Inference Engine (`inference_engine.py`) is the reasoning
component: it takes the facts of a chosen theorem, pattern-matches
them against the Knowledge Base to select applicable rules, applies
those rules step by step (forward chaining) to derive a sequence of
new states, and finally checks the last state against the goal. While
the Knowledge Base only *stores* rules, the Inference Engine *applies*
them and produces the explainable, step-by-step proof shown in the UI.

---

## Project Structure

```
ai_theorem_prover/
│
├── app.py                 # Streamlit UI (all 8 sections + Demo Mode)
├── knowledge_base.py       # Declarative rules (facts have no place here)
├── inference_engine.py     # Forward-chaining reasoning cycle
├── astar.py                 # A* search over proof states
├── theorem_library.py       # Problem formulation for each theorem
├── requirements.txt
├── README.md
└── assets/
    └── architecture.png
```
