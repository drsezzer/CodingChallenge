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

def read_dependencies():
    dependencies = []
    try:
        # Accept input until an EOF is encountered
        for line in input.strip().split('\n'):
            if line:
                parts = line.split()
                if len(parts) == 4:
                    dependencies.append((parts[0], int(parts[1]), parts[2], int(parts[3])))
    except EOFError:
        pass
    return dependencies

def build_graph(dependencies):
    forward_graph = defaultdict(list)
    for depender, depender_ver, dependee, dependee_ver in dependencies:
        forward_graph[(dependee, dependee_ver)].append((depender, depender_ver))
    return forward_graph

def calculate_dependents(graph):
    direct = defaultdict(set)
    transitive = defaultdict(set)

    # Populate direct dependents
    for node, dependents in graph.items():
        for dependent in dependents:
            direct[node].add(dependent)

    # Calculate transitive dependents using BFS without modifying the graph structure
    for node in list(graph.keys()):  # Ensure the graph's keys are listed before iteration
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for dependent in graph[current]:
                    transitive[node].add(dependent)
                    if dependent not in visited:
                        queue.append(dependent)

    # Adjust transitive counts by removing direct dependents
    for node in transitive:
        transitive[node] -= direct[node]

    return {node: len(transitives) for node, transitives in transitive.items()}, {node: len(directs) for node, directs in direct.items()}

def find_most_problematic(transitive, direct):
    max_ratio = -1
    problematic_package = None
    for node in direct:
        if direct[node] > 0 and node in transitive:  # Ensuring valid ratio computation
            ratio = transitive[node] / direct[node]
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = node
    return problematic_package

def main():
    dependencies = read_dependencies()
    graph = build_graph(dependencies)
    transitive_count, direct_count = calculate_dependents(graph)
    problematic_package = find_most_problematic(transitive_count, direct_count)
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic dependencies found.")

if __name__ == "__main__":
    main()
