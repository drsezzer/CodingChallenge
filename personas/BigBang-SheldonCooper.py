"""
Redirected with 'still wrong answer, it's giving b2, but i was expecting e1'.


"""

import sys
import networkx as nx

def main():
    graph = nx.DiGraph()

    # Assuming the input directly here for debugging purposes:
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

    most_problematic = None
    highest_ratio = -1

    for node in graph.nodes:
        direct_dependents = set(graph.predecessors(node))
        transitive_dependents = set(nx.descendants(graph, node))

        # Skipping nodes without direct dependents as they can't have a valid ratio
        if direct_dependents:
            ratio = len(transitive_dependents) / len(direct_dependents)
            print(f"Node {node} has ratio {ratio} with {len(transitive_dependents)} transitive and {len(direct_dependents)} direct dependents")
            if ratio > highest_ratio:
                most_problematic = node
                highest_ratio = ratio

    if most_problematic:
        print(f"Most problematic package is {most_problematic[0]} {most_problematic[1]} with a ratio of {highest_ratio:.2f}")
    else:
        print("No dependencies found.")

if __name__ == "__main__":
    main()