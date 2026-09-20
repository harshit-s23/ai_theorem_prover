"""
astar.py

This module implements a small, deterministic A* SEARCH over the space
of partial proofs, mirroring the A* Search taught in the AI syllabus.

AI Concept: A* SEARCH
-----------------------
State  : a partial proof (one node in the proof chain produced by the
         Inference Engine).
Action : applying the next inference rule to move from one proof state
         to the next.
g(n)   : the number of proof steps already taken to reach state n.
h(n)   : a heuristic estimate of how many proof steps still remain
         before the goal is reached. Here it is exact (not merely an
         estimate), since the Inference Engine has already determined
         the full proof chain -- which makes it a perfectly admissible
         and consistent heuristic for A*.
f(n)   : g(n) + h(n) -- the evaluation function A* minimises when
         choosing which node to expand next.

Because this small Knowledge Base produces exactly one reasoning path
per theorem (no alternative rule choices), the resulting search graph
is a simple chain. A* is still executed exactly as it would be for a
graph with branching -- using an open list (priority queue), a closed
list, and an explicit goal test -- it simply confirms that the single
available path is optimal.
"""

import heapq
from typing import Dict, List


class ProofNode:
    """A node in the proof-state search graph."""

    def __init__(self, node_id: str, label: str, index: int):
        self.node_id = node_id   # e.g. "Start", "S1", "S2", "Goal"
        self.label = label       # human-readable proof-state description
        self.index = index       # position in the proof chain (0 = Start)

    def __lt__(self, other: "ProofNode") -> bool:
        # Needed so heapq can break ties between nodes with equal f(n).
        return self.index < other.index


def build_proof_graph(node_labels: List[str]) -> List[ProofNode]:
    """Build the linear proof-state graph from the Inference Engine's output."""
    total = len(node_labels)
    nodes = []
    for i, label in enumerate(node_labels):
        if i == 0:
            node_id = "Start"
        elif i == total - 1:
            node_id = "Goal"
        else:
            node_id = f"S{i}"
        nodes.append(ProofNode(node_id, label, i))
    return nodes


def heuristic(node: ProofNode, goal_index: int) -> int:
    """h(n): exact number of remaining proof steps to reach the Goal node."""
    return goal_index - node.index


def a_star_search(node_labels: List[str]) -> Dict:
    """
    Perform an A* search over the proof-state graph built from
    node_labels and return the resulting search table (for display)
    together with the optimal path found and its total cost.
    """
    if not node_labels:
        return {"search_table": [], "path": [], "total_cost": 0}

    nodes = build_proof_graph(node_labels)
    goal_index = len(nodes) - 1
    start = nodes[0]

    open_list = []  # priority queue of (f, index, node)
    g_score = {start.index: 0}

    heapq.heappush(open_list, (heuristic(start, goal_index), start.index, start))

    search_table = []
    visited = set()

    while open_list:
        f_current, _, current = heapq.heappop(open_list)

        if current.index in visited:
            continue
        visited.add(current.index)

        g_current = g_score[current.index]
        h_current = heuristic(current, goal_index)

        search_table.append({
            "Node": current.node_id,
            "Proof State": current.label,
            "g(n)": g_current,
            "h(n)": h_current,
            "f(n)": g_current + h_current,
        })

        # GOAL TEST
        if current.index == goal_index:
            break

        # Expand the successor (single successor -- linear proof chain)
        next_index = current.index + 1
        if next_index < len(nodes):
            neighbour = nodes[next_index]
            tentative_g = g_current + 1
            if neighbour.index not in g_score or tentative_g < g_score[neighbour.index]:
                g_score[neighbour.index] = tentative_g
                f_neighbour = tentative_g + heuristic(neighbour, goal_index)
                heapq.heappush(open_list, (f_neighbour, neighbour.index, neighbour))

    path = [row["Node"] for row in search_table]

    return {
        "search_table": search_table,
        "path": path,
        "total_cost": search_table[-1]["g(n)"] if search_table else 0,
    }
