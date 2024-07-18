"""
Redirected with 'still wrong answer, it's giving b2, but i was expecting e1'.


"""

import sys
import networkx as nx

def main():
    # Initializing the directed graph to model the dependencies
    graph = nx.DiGraph()

    # For demonstration, replacing sys.stdin with a list of input lines
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

    # Populate the graph with edges based on input
    for line in input_lines:
        src_package, src_version, dest_package, dest_version = line.split()
        src_version, dest_version = int(src_version), int(dest_version)
        graph.add_edge((src_package, src_version), (dest_package, dest_version))

    # Variables to track the most problematic package
    most_problematic = None
    highest_ratio = -1

    # Analyzing each node in the graph
    for node in graph.nodes:
        direct_dependents = set(graph.predecessors(node))  # Directly dependent nodes
        transitive_dependents = set(nx.descendants(graph, node))  # Indirectly dependent nodes

        # Calculating the ratio if there are direct dependents to avoid division by zero
        if direct_dependents:
            ratio = len(transitive_dependents) / len(direct_dependents)
            # Debugging output to trace computation
            print(f"Node {node} has {len(transitive_dependents)} transitive dependents and {len(direct_dependents)} direct dependents, ratio: {ratio:.2f}")

            # Updating the most problematic node if the current ratio is higher
            if ratio > highest_ratio:
                most_problematic = node
                highest_ratio = ratio

    # Final output of the most problematic package
    if most_problematic:
        print(f"Most problematic package: {most_problematic[0]} {most_problematic[1]}, Ratio: {highest_ratio:.2f}")
    else:
        print("No dependencies found.")

if __name__ == "__main__":
    main()
