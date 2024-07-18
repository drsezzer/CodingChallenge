"""
"""

input = """a 1 b 2
a 1 c 4
b 2 c 4
b 2 d 0
b 3 b 2
b 3 e 2
c 4 d 0
c 4 e 1"""

import sys
from collections import defaultdict

def read_input():
    dependencies = []
    for line in input.strip().split("\n"):
        parts = line.strip().split()
        if len(parts) == 4:
            dependencies.append((parts[0], int(parts[1]), parts[2], int(parts[3])))
    return dependencies

def build_graph(dependencies):
    graph = defaultdict(list)
    for depender, depender_ver, dependee, dependee_ver in dependencies:
        graph[(dependee, dependee_ver)].append((depender, depender_ver))
    return graph

def compute_dependents(graph):
    direct = defaultdict(set)
    all_dependents = defaultdict(set)

    # Collect direct dependents
    for node, dependents in graph.items():
        for dependent in dependents:
            direct[node].add(dependent)
            all_dependents[node].add(dependent)

    # Compute all (transitive) dependents using DFS
    def dfs(node, accum):
        for dependent in graph[node]:
            if dependent not in accum:
                accum.add(dependent)
                all_dependents[dependent].update(accum)
                dfs(dependent, accum)

    for node in graph:
        dfs(node, set(direct[node]))

    # Calculate transitive dependents
    transitive = {node: len(all_dependents[node] - direct[node]) for node in graph}

    return transitive, {node: len(direct[node]) for node in graph}

def find_most_problematic(transitive, direct):
    max_ratio = -1
    problematic_package = None
    for node in transitive:
        if direct[node] > 0:  # Avoid division by zero
            ratio = transitive[node] / direct[node]
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = node
    return problematic_package

def main():
    dependencies = read_input()
    graph = build_graph(dependencies)
    transitive, direct = compute_dependents(graph)
    problematic_package = find_most_problematic(transitive, direct)
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic dependencies found.")

if __name__ == "__main__":
    main()