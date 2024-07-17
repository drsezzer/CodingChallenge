"""
Taking on the role of Commander William Riker from Star Trek, I'll face this 
challenge head-on with the confidence and strategic thinking characteristic 
of Riker's approach. We'll boldly navigate through this programming task to 
determine the most impactful or "problematic" package dependency based on 
its influence over other packages in the system.

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
    try:
        for line in input.strip().split("\n"):
            if line.strip():
                dependencies.append(line.strip().split())
    except KeyboardInterrupt:
        pass
    return dependencies

def build_graph(dependencies):
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for dep in dependencies:
        pkg1, ver1, pkg2, ver2 = dep
        graph[(pkg2, ver2)].append((pkg1, ver1))
        reverse_graph[(pkg1, ver1)].append((pkg2, ver2))
    return graph, reverse_graph

def calculate_transitive_dependents(graph):
    transitive_count = {}
    for node in graph:
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            queue.extend(graph[current])
        transitive_count[node] = len(visited) - 1
    return transitive_count

def find_most_problematic_package(graph, reverse_graph):
    transitive_counts = calculate_transitive_dependents(graph)
    max_ratio = -1
    problematic_package = None
    for pkg, direct_deps in reverse_graph.items():
        if pkg in transitive_counts:
            trans_count = transitive_counts[pkg]
            direct_count = len(direct_deps)
            if direct_count > 0:
                ratio = trans_count / direct_count
                if ratio > max_ratio:
                    max_ratio = ratio
                    problematic_package = pkg
    return problematic_package

def main():
    dependencies = read_input()
    graph, reverse_graph = build_graph(dependencies)
    most_problematic = find_most_problematic_package(graph, reverse_graph)
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()
