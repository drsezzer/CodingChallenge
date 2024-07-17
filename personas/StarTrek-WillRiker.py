"""
redirected with 'it throws dictionary changed exception'
... but then it gives the answer as c4!?
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
    nodes = set()
    for dep in dependencies:
        pkg1, ver1, pkg2, ver2 = dep
        pkg1_ver1 = (pkg1, ver1)
        pkg2_ver2 = (pkg2, ver2)
        nodes.add(pkg1_ver1)
        nodes.add(pkg2_ver2)
        graph[pkg2_ver2].append(pkg1_ver1)
        reverse_graph[pkg1_ver1].append(pkg2_ver2)
    return graph, reverse_graph, nodes

def calculate_transitive_dependents(graph, nodes):
    transitive_count = {}
    for node in nodes:
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            queue.extend(graph[current])
        # Subtract one to exclude the node itself from its count
        transitive_count[node] = len(visited) - 1
    return transitive_count

def find_most_problematic_package(graph, reverse_graph, nodes):
    transitive_counts = calculate_transitive_dependents(graph, nodes)
    max_ratio = -1
    problematic_package = None
    for pkg in nodes:
        if pkg in reverse_graph:
            direct_deps = reverse_graph[pkg]
            direct_count = len(direct_deps)
            if direct_count > 0 and pkg in transitive_counts:
                trans_count = transitive_counts[pkg]
                ratio = trans_count / direct_count
                if ratio > max_ratio:
                    max_ratio = ratio
                    problematic_package = pkg
    return problematic_package

def main():
    dependencies = read_input()
    graph, reverse_graph, nodes = build_graph(dependencies)
    most_problematic = find_most_problematic_package(graph, reverse_graph, nodes)
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()
