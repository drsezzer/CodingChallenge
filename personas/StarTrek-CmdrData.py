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
    reverse_graph = defaultdict(list)
    for depender, depender_ver, dependee, dependee_ver in dependencies:
        graph[(depender, depender_ver)].append((dependee, dependee_ver))
        reverse_graph[(dependee, dependee_ver)].append((depender, depender_ver))
    return graph, reverse_graph

def calculate_dependents(reverse_graph):
    transitive_count = defaultdict(int)
    direct_count = defaultdict(lambda: 0)

    # Calculate direct dependents
    for node, dependents in reverse_graph.items():
        direct_count[node] = len(dependents)

    # Calculate transitive dependents using a modified BFS that collects updates
    for node in reverse_graph:
        visited = set()
        queue = deque([node])
        local_updates = defaultdict(int)
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for dependent in reverse_graph[current]:
                    if dependent not in visited:
                        local_updates[dependent] += 1
                        queue.append(dependent)
        # Apply the collected updates to the transitive count
        for dep, count in local_updates.items():
            transitive_count[dep] += count

    return transitive_count, direct_count

def find_most_problematic(transitive_count, direct_count):
    max_ratio = -1
    problematic_package = None
    for node, direct in direct_count.items():
        if direct > 0:  # Avoid division by zero
            trans = transitive_count[node]
            ratio = trans / direct
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = node
    return problematic_package

def main():
    dependencies = read_input()
    _, reverse_graph = build_graph(dependencies)
    transitive_count, direct_count = calculate_dependents(reverse_graph)
    problematic_package = find_most_problematic(transitive_count, direct_count)
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic dependencies")

if __name__ == "__main__":
    main()
