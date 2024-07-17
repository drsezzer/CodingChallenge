"""
In the spirit of Dr. Beverly Crusher from Star Trek—always precise, methodical, 
and driven by a deep understanding of complex systems—I'll craft a Python 
program that addresses this challenge. In this scenario, we're dealing with a 
dependency management problem, akin to navigating the intricate web of 
Starfleet's medical protocols and equipment maintenance.

Go Bev!!! Right first time, not rediction needed!!

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

def read_dependencies():
    # Reading from standard input
    dependencies = []
    for line in input.strip().split("\n"):
        if line.strip():
            parts = line.strip().split()
            dependencies.append((parts[0], int(parts[1]), parts[2], int(parts[3])))
    return dependencies

def build_graph(dependencies):
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for src_name, src_ver, dest_name, dest_ver in dependencies:
        graph[(src_name, src_ver)].append((dest_name, dest_ver))
        reverse_graph[(dest_name, dest_ver)].append((src_name, src_ver))
    return graph, reverse_graph

def calculate_dependency_scores(graph, reverse_graph):
    # Find all nodes in the reverse graph
    nodes = list(reverse_graph.keys())
    
    # Calculate transitive dependants using BFS
    transitive_dependants = defaultdict(set)
    for node in nodes:
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            transitive_dependants[node].add(current)
            for neighbour in reverse_graph[current]:
                if neighbour not in visited:
                    queue.append(neighbour)
    
    # Remove self from transitive dependants
    for node in nodes:
        transitive_dependants[node].discard(node)
    
    # Calculate direct dependants
    direct_dependants = {node: len(reverse_graph[node]) for node in nodes}
    
    # Calculate the problematic score
    scores = {}
    for node in nodes:
        if direct_dependants[node] > 0:
            scores[node] = len(transitive_dependants[node]) / direct_dependants[node]
    
    return scores

def find_most_problematic_package(scores):
    # Return the package with the highest problematic score
    if not scores:
        return None
    return max(scores, key=scores.get)

if __name__ == "__main__":
    dependencies = read_dependencies()
    graph, reverse_graph = build_graph(dependencies)
    scores = calculate_dependency_scores(graph, reverse_graph)
    most_problematic = find_most_problematic_package(scores)
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")
    else:
        print("No dependencies found")
