"""
redirected with 'its still throwing dictionary changed exception for line 'for node in graph''
now works but returned wrong answer b2!
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
    # Simulating reading from standard input for the example
    dependencies = input.strip().split('\n')
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)

    for line in dependencies:
        package1, version1, package2, version2 = line.split()
        version1, version2 = int(version1), int(version2)
        graph[(package1, version1)].append((package2, version2))
        reverse_graph[(package2, version2)].append((package1, version1))

    return graph, reverse_graph

def compute_transitive_dependants(graph):
    transitive_counts = {}

    def dfs(node):
        stack = [node]
        visited = set()
        visited.add(node)
        count = 0
        while stack:
            current = stack.pop()
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    count += 1
        return count

    for node in list(graph.keys()):  # Operate on a static list of keys
        transitive_counts[node] = dfs(node)

    return transitive_counts

def compute_direct_dependants(reverse_graph):
    direct_counts = {}
    for node, dependants in reverse_graph.items():
        direct_counts[node] = len(dependants)
    return direct_counts

def find_most_problematic_package(transitive_counts, direct_counts):
    max_ratio = -1
    problematic_package = None

    for package, transitive_count in transitive_counts.items():
        if package in direct_counts:
            direct_count = direct_counts[package]
            if direct_count > 0:  # Avoid division by zero
                ratio = transitive_count / direct_count
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
