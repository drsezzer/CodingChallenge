"""
Alright, I'll take on the role of Wesley Crusher, the young and ambitious 
Starfleet Academy cadet from Star Trek: The Next Generation, always keen to 
dive into a challenging problem with an analytical approach. I'll write the 
Python program in a way that reflects Wesley's enthusiasm for solving complex 
problems using technology and his love for experimentation and learning. Let's 
tackle the task of finding the most problematic dependency among packages.


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

def parse_input():
    # Reading from standard input (simulated here as an example for understanding)
    dependencies = input.strip().split('\n')
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)

    for line in dependencies:
        package1, version1, package2, version2 = line.split()
        graph[(package1, int(version1))].append((package2, int(version2)))
        reverse_graph[(package2, int(version2))].append((package1, int(version1)))

    return graph, reverse_graph

def compute_transitive_dependants(graph):
    def dfs(node, visited):
        count = 0
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                count += 1 + dfs(neighbor, visited)
        return count

    transitive_counts = {}
    for node in graph:
        visited = set()
        transitive_counts[node] = dfs(node, visited)

    return transitive_counts

def compute_direct_dependants(reverse_graph):
    direct_counts = {node: len(dependants) for node, dependants in reverse_graph.items()}
    return direct_counts

def find_most_problematic_package(transitive_counts, direct_counts):
    max_ratio = -1
    problematic_package = None

    for package, transitive_count in transitive_counts.items():
        if package in direct_counts and direct_counts[package] > 0:
            ratio = transitive_count / direct_counts[package]
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package

    return problematic_package

def main():
    graph, reverse_graph = parse_input()
    transitive_counts = compute_transitive_dependants(graph)
    direct_counts = compute_direct_dependants(reverse_graph)
    problematic_package = find_most_problematic_package(transitive_counts, direct_counts)
    
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic package found")

if __name__ == "__main__":
    main()
