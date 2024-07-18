"""
"""

import sys
import networkx as nx

def main():
    graph = nx.DiGraph()

    input_lines = [
        "a 1 b 2",
        "a 1 c 4",
        "b 2 c 4",
        "b 2 d 0",
        "b 3 b 2",
        "b 3 e 2",
        "c 4 d 0",
        "c 4 e 1"
    ]

    for line in input_lines:
        src_package, src_version, dest_package, dest_version = line.split()
        src_version, dest_version = int(src_version), int(dest_version)
        graph.add_edge((src_package, src_version), (dest_package, dest_version))

    # Explore an alternative metric for "problematic"
    problematic_scores = {}
    for node in graph.nodes:
        direct_dependents = set(graph.predecessors(node))
        transitive_dependents = set(nx.descendants(graph, node))

        if direct_dependents:
            ratio = len(transitive_dependents) / len(direct_dependents)
        else:
            ratio = 0  # Avoid division by zero

        # Maybe consider adding weight based on how many nodes this one influences indirectly
        problematic_scores[node] = ratio

    # Determine the most problematic package
    most_problematic = max(problematic_scores, key=problematic_scores.get)
    highest_ratio = problematic_scores[most_problematic]

    print(f"Most problematic package: {most_problematic[0]} {most_problematic[1]}, Ratio: {highest_ratio:.2f}")

if __name__ == "__main__":
    main()
