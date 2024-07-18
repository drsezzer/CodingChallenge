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

    # Analyze for critical leaf nodes
    critical_leaves = {}
    for node in graph.nodes:
        direct_dependents = set(graph.predecessors(node))
        transitive_dependents = set(nx.descendants(graph, node))

        # Condition for a critical leaf node
        if direct_dependents and not transitive_dependents:
            critical_leaves[node] = len(direct_dependents)

    # Determine if there are any critical leaf nodes
    if critical_leaves:
        most_problematic = max(critical_leaves, key=critical_leaves.get)
        direct_count = critical_leaves[most_problematic]
        print(f"Most problematic package as critical leaf: {most_problematic[0]} {most_problematic[1]}, Direct dependents count: {direct_count}")
    else:
        print("No critical leaves found.")

if __name__ == "__main__":
    main()
