"""
redirected with 'it's throwing changed dictionary size exception for line 'for node in reverse_graph''
... forth attempt - it gets the right answer!
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
from collections import defaultdict, deque

def read_input():
    dependencies = []
    try:
        lines = input.strip().split("\n")
        for line in lines:
            if line:
                dependencies.append(line.split())
            else:
                break
    except EOFError:
        pass
    return dependencies

def build_graphs(dependencies):
    reverse_graph = defaultdict(set)
    graph = defaultdict(set)
    
    for dep in dependencies:
        dependent, dep_ver, dependency, depd_ver = dep
        dep_pair = (dependent, dep_ver)
        depd_pair = (dependency, depd_ver)
        reverse_graph[depd_pair].add(dep_pair)
        graph[dep_pair].add(depd_pair)
    
    return graph, reverse_graph

def calculate_transitive_dependents(reverse_graph):
    transitive_dependents_count = {}
    nodes = list(reverse_graph.keys())  # Copy of keys to stabilize the dictionary during iteration
    for node in nodes:
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for neighbor in reverse_graph[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        transitive_dependents_count[node] = len(visited) - 1  # Exclude the node itself
    return transitive_dependents_count

def find_most_problematic_package(reverse_graph, transitive_dependents_count):
    max_ratio = -1
    problematic_package = None

    for package, dependents in reverse_graph.items():
        if package in transitive_dependents_count:
            transitive_count = transitive_dependents_count[package]
            direct_count = len(dependents)
            if direct_count > 0:
                ratio = transitive_count / direct_count
                if ratio > max_ratio:
                    max_ratio = ratio
                    problematic_package = package
    
    return problematic_package

def main():
    dependencies = read_input()
    graph, reverse_graph = build_graphs(dependencies)
    transitive_dependents_count = calculate_transitive_dependents(reverse_graph)
    problematic_package = find_most_problematic_package(reverse_graph, transitive_dependents_count)
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")

if __name__ == "__main__":
    main()
