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

    # Expand to transitive dependents using a recursive DFS
    def dfs(node, visited):
        for dependent in direct[node]:
            if dependent not in visited:
                visited.add(dependent)
                all_dependents[dependent].update(all_dependents[node])
                dfs(dependent, visited)

    for node in graph:
        dfs(node, set())

    transitive = {node: len(all_deps - direct_deps) for node, all_deps in all_dependents.items() for direct_deps in (direct[node],)}
    direct_count = {node: len(direct_deps) for node, direct_deps in direct.items()}

    return transitive, direct_count

def find_most_problematic(transitive, direct):
    max_ratio = -1
    problematic_package = None
    for node in direct:
        if direct[node] > 0:  # Ensure we have direct dependants
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
