"""
app.py

AI THEOREM PROVING ASSISTANT
==============================
A small Knowledge-Based AI prototype built for CIA-1 Part 5, based on
the research paper "Artificial Intelligence Technology in Mathematical
and Engineering Applications" -- specifically the AUTOMATED THEOREM
PROVING problem area.

This Streamlit application demonstrates, end to end and on a small
scale, how a Knowledge-Based / Goal-Based Agent can:
    - store domain knowledge in a KNOWLEDGE BASE (knowledge_base.py),
    - formulate the problem in terms of facts and a goal
      (theorem_library.py),
    - use an INFERENCE ENGINE to apply rules and derive new facts
      (inference_engine.py),
    - use A* SEARCH to explore the space of partial proofs (astar.py),
      and
    - explain its own reasoning at every step (EXPLAINABLE AI).

IMPORTANT: This is an educational PROTOTYPE. It proves only the
predefined theorem patterns stored in its Knowledge Base. It does NOT
implement general-purpose automated theorem proving, and it clearly
reports when a requested theorem is outside its Knowledge Base.
"""

import pandas as pd
import streamlit as st

import knowledge_base as kb
import theorem_library as tl
from astar import a_star_search
from inference_engine import InferenceEngine

# -----------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="AI Theorem Proving Assistant",
    page_icon="\u2234",  # THEREFORE symbol
    layout="wide",
)

# -----------------------------------------------------------------------
# SESSION STATE INITIALISATION
# -----------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "selected_theorem_id" not in st.session_state:
    st.session_state.selected_theorem_id = None
if "search_result" not in st.session_state:
    st.session_state.search_result = None
if "is_demo" not in st.session_state:
    st.session_state.is_demo = False


def run_proof(theorem_id: str) -> None:
    """Run the Inference Engine and, if successful, the A* Search."""
    engine = InferenceEngine()
    result = engine.prove(theorem_id)
    st.session_state.result = result
    st.session_state.selected_theorem_id = theorem_id

    if result["status"] != "UNSUPPORTED" and result["steps"]:
        theorem = result["theorem"]
        start_label = "Given: " + ", ".join(theorem["facts"])
        node_labels = [start_label] + [s["result"] for s in result["steps"]]
        st.session_state.search_result = a_star_search(node_labels)
    else:
        st.session_state.search_result = None


def reset_app() -> None:
    st.session_state.result = None
    st.session_state.selected_theorem_id = None
    st.session_state.search_result = None
    st.session_state.is_demo = False


# -----------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------
st.title("AI Theorem Proving Assistant")
st.caption("A Knowledge-Based AI Prototype for Automated Mathematical Reasoning")

st.info(
    "This prototype demonstrates how a knowledge-based agent can use "
    "mathematical rules, inference, and heuristic search to construct a "
    "proof.\n\n"
    "**This educational prototype proves selected theorems using its "
    "predefined mathematical knowledge base and inference rules.**"
)

st.divider()

# -----------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------
st.sidebar.header("Theorem Selection")

theorem_options = tl.list_theorem_titles()
theorem_labels = [title for _id, title in theorem_options]
theorem_ids = [tid for tid, _title in theorem_options]

selected_index = st.sidebar.selectbox(
    "Choose a theorem to prove:",
    options=range(len(theorem_labels)),
    format_func=lambda i: theorem_labels[i],
)
chosen_theorem_id = theorem_ids[selected_index]

col_a, col_b = st.sidebar.columns(2)
prove_clicked = col_a.button("Prove Theorem", use_container_width=True)
reset_clicked = col_b.button("Reset", use_container_width=True)

st.sidebar.divider()
demo_clicked = st.sidebar.button("\u25B6 Run Demo Mode (Even + Even)", use_container_width=True)

st.sidebar.divider()
st.sidebar.markdown(
    "**PEAS Description**\n\n"
    "- **Performance measure:** correct, step-by-step, explainable proof\n"
    "- **Environment:** a small mathematical Knowledge Base\n"
    "- **Actuators:** displaying proof steps and the final conclusion\n"
    "- **Sensors:** the theorem chosen by the user"
)

if reset_clicked:
    reset_app()

if prove_clicked:
    run_proof(chosen_theorem_id)
    st.session_state.is_demo = False

if demo_clicked:
    run_proof("even_plus_even")
    st.session_state.is_demo = True

# -----------------------------------------------------------------------
# MAIN AREA
# -----------------------------------------------------------------------
result = st.session_state.result

if result is None:
    st.markdown("### Welcome")
    st.write(
        "Select a theorem from the sidebar and click **Prove Theorem**, "
        "or click **Run Demo Mode** to see a full, automatic walkthrough "
        "of *Even + Even = Even*."
    )
    st.markdown("#### Supported theorem patterns in the Knowledge Base")
    for tid, title in tl.list_theorem_titles():
        if tid != "unsupported_demo":
            st.markdown(f"- {title}")

else:
    theorem_id = st.session_state.selected_theorem_id
    theorem = tl.get_theorem(theorem_id)

    if st.session_state.is_demo:
        st.success(
            "**Demo Mode:** automatically demonstrating the full pipeline "
            "for *Even + Even = Even* -- "
            "Initial State \u2192 Knowledge Retrieval \u2192 Rule Selection \u2192 "
            "A* Search \u2192 Proof Generation \u2192 Goal Test \u2192 Theorem Proved."
        )

    # ---------------------------------------------------------------
    # UNSUPPORTED THEOREM HANDLING
    # ---------------------------------------------------------------
    if result["status"] == "UNSUPPORTED" or theorem is None:
        st.error("Unable to prove this theorem with the current knowledge base.")
        st.warning(
            "**Limitation:** This is an educational prototype and supports "
            "only predefined theorem patterns. The selected theorem's "
            "pattern (e.g. properties of prime numbers) is not represented "
            "in `knowledge_base.py`, so no proof can be generated."
        )

    else:
        # -------------------------------------------------------
        # SECTION 1: PROBLEM STATEMENT
        # -------------------------------------------------------
        st.header("1. Problem Statement")
        st.markdown(f"**Theorem:** {theorem['title']}")
        st.write(theorem["statement"])

        # -------------------------------------------------------
        # SECTION 2: INITIAL STATE
        # -------------------------------------------------------
        st.header("2. Initial State (Problem Formulation)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Facts:**")
            for fact in theorem["facts"]:
                st.markdown(f"- {fact}")
        with col2:
            st.markdown("**Goal:**")
            st.markdown(f"- {theorem['goal']}")

        # -------------------------------------------------------
        # SECTION 3: KNOWLEDGE BASE
        # -------------------------------------------------------
        st.header("3. Knowledge Base (Rules Retrieved)")
        st.write(
            "The Inference Engine matched the facts above against the "
            "Knowledge Base and retrieved the following rules:"
        )
        for rule_id in result["rules_used"]:
            detail = kb.get_rule_details(rule_id)
            if detail:
                st.markdown(
                    f"- **{detail.get('name', rule_id)}**: "
                    f"`{detail['rule']}` -- {detail['description']}"
                )

        with st.expander("View the complete Knowledge Base"):
            for line in kb.get_all_rules_summary():
                st.markdown(f"- {line}")

        # -------------------------------------------------------
        # SECTION 4: A* SEARCH
        # -------------------------------------------------------
        st.header("4. A* Search Over Proof States")
        st.write(
            "**State** = a partial proof. **g(n)** = proof steps already "
            "taken. **h(n)** = estimated remaining steps to the goal. "
            "**f(n) = g(n) + h(n)**. A* repeatedly expands the node with "
            "the lowest f(n) until the Goal state is reached."
        )
        search_result = st.session_state.search_result
        if search_result and search_result["search_table"]:
            df = pd.DataFrame(search_result["search_table"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success(
                f"A* Search reached the Goal state after expanding "
                f"{len(search_result['search_table'])} node(s), with a "
                f"total path cost g(Goal) = {search_result['total_cost']}."
            )

        # -------------------------------------------------------
        # SECTION 5: PROOF STEPS
        # -------------------------------------------------------
        st.header("5. Proof Steps (Inference Engine Output)")
        for step in result["steps"]:
            with st.expander(f"Step {step['step_no']}: {step['action']}"):
                st.markdown(f"**Rule applied:** `{step['rule_used']}`")
                st.markdown(f"**Reasoning:** {step['reasoning']}")
                st.markdown(f"**Result:** {step['result']}")

        # -------------------------------------------------------
        # SECTION 6: FINAL RESULT
        # -------------------------------------------------------
        st.header("6. Final Result")
        if result["status"] == "PROVED":
            st.success(f"\u2713 THEOREM PROVED\n\n{result['final_conclusion']}")
        else:
            st.error(f"\u2717 THEOREM COULD NOT BE PROVED\n\n{result['final_conclusion']}")

        # -------------------------------------------------------
        # SECTION 7: EXPLAINABLE AI
        # -------------------------------------------------------
        st.header("7. Explainable AI")
        st.markdown("**Why was this proof selected?**")
        with st.expander("Click to view the explanation", expanded=True):
            st.write(
                f"The Inference Engine selected the definition rules for "
                f"the parity of **a** and **b** because the theorem's "
                f"facts explicitly state their parity. It then applied "
                f"**substitution** to combine both definitions into a "
                f"single expression, followed by **algebraic "
                f"simplification** to reduce that expression back into "
                f"the standard form (2k or 2k+1). Finally, it matched "
                f"this form against the Knowledge Base combination rule "
                f"for **{theorem['var_a_parity']} {theorem['operator']} "
                f"{theorem['var_b_parity']}**, which is the only rule in "
                f"the Knowledge Base whose condition matches the given "
                f"facts -- this is why this specific chain of steps, and "
                f"no other, was chosen."
            )
            st.markdown("**Step-by-step justification:**")
            for step in result["steps"]:
                st.markdown(f"- Step {step['step_no']}: {step['reasoning']}")

        # -------------------------------------------------------
        # SECTION 8: SYSTEM ARCHITECTURE
        # -------------------------------------------------------
        st.header("8. System Architecture")
        st.code(
            "User Input\n"
            "    |\n"
            "    v\n"
            "Problem Formulation   (theorem_library.py)\n"
            "    |\n"
            "    v\n"
            "Knowledge Base         (knowledge_base.py)\n"
            "    |\n"
            "    v\n"
            "Inference Engine        (inference_engine.py)\n"
            "    |\n"
            "    v\n"
            "A* Search               (astar.py)\n"
            "    |\n"
            "    v\n"
            "Goal Test\n"
            "    |\n"
            "    v\n"
            "Proof\n"
            "    |\n"
            "    v\n"
            "Explanation (Explainable AI)",
            language="text",
        )

st.divider()
st.caption(
    "AI Theorem Proving Assistant | Educational prototype for CIA-1 Part 5 | "
    "Supports only the predefined theorem patterns stored in its Knowledge Base."
)
