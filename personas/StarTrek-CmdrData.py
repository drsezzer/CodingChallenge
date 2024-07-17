""" standard prompt 

throw dictionary changed exception """

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
    transitive_count = defaultdict(int)
    direct_count = defaultdict(int)
    
    # Calculate direct dependents
    for node, dependents in graph.items():
        direct_count[node] = len(dependents)
    
    # Calculate transitive dependents using BFS
    for node in graph:
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for dependent in graph[current]:
                    transitive_count[dependent] += 1
                    queue.append(dependent)

    return transitive_count, direct_count

def find_most_problematic(transitive_count, direct_count):
    max_ratio = -1
    problematic_package = None
    for node in transitive_count:
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
        print("No dependencies found")

if __name__ == "__main__":
    main()
