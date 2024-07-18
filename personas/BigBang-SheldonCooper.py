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

    # Identify all nodes and their end-chain status
    end_chain_nodes = {node: False for node in graph.nodes()}
    for node in graph.nodes:
        if not list(graph.successors(node)):  # This is an end-chain node
            end_chain_nodes[node] = True

    # Determine which end-chain node is most problematic based on its dependency importance
    most_problematic = None
    longest_dependency_chain = -1

    for node, is_end in end_chain_nodes.items():
        if is_end:
            # Compute the length of the longest path leading to this node
            lengths = [nx.shortest_path_length(graph, source=n, target=node) for n in graph.nodes() if nx.has_path(graph, n, node)]
            if lengths:
                max_length = max(lengths)
                if max_length > longest_dependency_chain:
                    longest_dependency_chain = max_length
                    most_problematic = node

    if most_problematic:
        print(f"Most problematic package due to critical dependency chain: {most_problematic[0]} {most_problematic[1]}, Chain length: {longest_dependency_chain}")
    else:
        print("No problematic package found.")

if __name__ == "__main__":
    main()
