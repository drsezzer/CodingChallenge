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
from collections import defaultdict, deque

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

def calculate_dependents(graph):
    direct_count = defaultdict(int)
    transitive_count = defaultdict(set)  # Use a set to avoid duplicates

    # Count direct dependants and prepare for transitive calculation
    for node, dependants in graph.items():
        direct_count[node] = len(dependants)
        for dependant in dependants:
            transitive_count[dependant].add(node)

    # Calculate transitive dependants using a BFS
    for node in list(graph):
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for dependant in graph[current]:
                    if dependant not in visited:
                        transitive_count[dependant].update(transitive_count[current])
                        queue.append(dependant)

    # Convert sets to counts
    transitive_counts = {k: len(v) for k, v in transitive_count.items()}
    return transitive_counts, direct_count

def find_most_problematic(transitive_count, direct_count):
    max_ratio = -1
    problematic_package = None
    for node in direct_count:
        if direct_count[node] > 0:  # Avoid division by zero
            ratio = transitive_count[node] / direct_count[node]
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = node
    return problematic_package

def main():
    dependencies = read_input()
    graph = build_graph(dependencies)
    transitive_count, direct_count = calculate_dependents(graph)
    problematic_package = find_most_problematic(transitive_count, direct_count)
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic dependencies found.")

if __name__ == "__main__":
    main()
