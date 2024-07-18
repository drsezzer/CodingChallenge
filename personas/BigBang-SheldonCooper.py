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

    # Identify terminal nodes
    terminal_nodes = [node for node in graph.nodes if not list(graph.successors(node))]

    # Identify the most problematic among terminal nodes by the significance of what they depend on
    most_problematic = None
    max_direct_dependents = -1
    for node in terminal_nodes:
        # Checking what each terminal node depends on
        dependencies = graph.predecessors(node)
        total_dependents = sum(len(list(graph.successors(dep))) for dep in dependencies)

        if total_dependents > max_direct_dependents:
            most_problematic = node
            max_direct_dependents = total_dependents

    if most_problematic:
        print(f"Most problematic terminal package: {most_problematic[0]} {most_problematic[1]}, depending on nodes with {max_direct_dependents} total direct dependents")
    else:
        print("No terminal nodes found.")

if __name__ == "__main__":
    main()
