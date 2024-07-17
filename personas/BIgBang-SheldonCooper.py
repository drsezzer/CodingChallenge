"""
standard prompt 

Ah, an intellectual challenge, how refreshing! You're asking for a program in 
Python to solve a problem regarding package dependencies. It's reminiscent of a 
dependency graph, and what we seek to find is the package with the highest 
ratio of transitive dependents to direct dependents. This is, essentially, a 
graph problem where nodes are packages with versions, and edges define 
dependency relationships.

Given the sheer importance of defining our constructs properly, let's use a 
directed graph where each node represents a package-version tuple, like 
("a", 1). An edge from ("a", 1) to ("b", 2) implies that version 1 of package 
"a" depends on version 2 of package "b".

We'll utilize the networkx library for graph operations as it provides 
extensive functionalities for handling directed graphs, including methods for 
finding predecessors and descendants which are quintessential for our 
calculations.


... but ultimately gets it wrong! b2.
"""

input = """a 1 b 2
a 1 c 4
b 2 c 4
b 2 d 0
b 3 b 2
b 3 e 2
c 4 d 0
c 4 e 1
"""

import sys
import networkx as nx

def main():
    # Initialize the directed graph
    graph = nx.DiGraph()

    # Read lines from standard input
    for line in input.strip().split("\n"):
        # Split the line into components
        src_package, src_version, dest_package, dest_version = line.split()
        src_version = int(src_version)
        dest_version = int(dest_version)

        # Add nodes and directed edge to the graph
        graph.add_edge((src_package, src_version), (dest_package, dest_version))

    # Variable to track the package with the highest problematic ratio
    most_problematic = None
    highest_ratio = -1

    # Analyze the graph to find the most problematic dependency
    for node in graph.nodes:
        # Find direct dependents (predecessors)
        direct_dependents = set(graph.predecessors(node))
        # Find transitive dependents (all reachable nodes)
        transitive_dependents = set(nx.descendants(graph, node))

        # Calculate the ratio if there are any direct dependents
        if direct_dependents:
            ratio = len(transitive_dependents) / len(direct_dependents)
            # Update the most problematic package if this ratio is higher
            if ratio > highest_ratio:
                most_problematic = node
                highest_ratio = ratio

    if most_problematic:
        # Output the most problematic package and its ratio
        print(f"{most_problematic[0]} {most_problematic[1]}: {highest_ratio:.2f}")
    else:
        print("No dependencies found.")

if __name__ == "__main__":
    main()
