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
    dependencies = input.strip().split('\n')
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)

    for line in dependencies:
        src, src_ver, dst, dst_ver = line.split()
        src_ver, dst_ver = int(src_ver), int(dst_ver)
        graph[(src, src_ver)].append((dst, dst_ver))
        reverse_graph[(dst, dst_ver)].append((src, src_ver))

    return graph, reverse_graph

def calculate_transitive_dependants(reverse_graph):
    transitive_counts = {}

    def bfs(start):
        queue = deque([start])
        visited = set([start])
        count = 0
        while queue:
            node = queue.popleft()
            for neighbor in reverse_graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    count += 1
        return count

    nodes = list(reverse_graph.keys())  # Create a list of keys to iterate over
    for node in nodes:
        transitive_counts[node] = bfs(node)

    return transitive_counts

def calculate_direct_dependants(reverse_graph):
    direct_counts = {node: len(deps) for node, deps in reverse_graph.items()}
    return direct_counts

def find_most_problematic_package(transitive_counts, direct_counts):
    max_ratio = -1
    problematic_package = None

    for package, trans_count in transitive_counts.items():
        direct_count = direct_counts.get(package, 0)
        if direct_count > 0:
            ratio = trans_count / direct_count
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package

    return problematic_package

def main():
    graph, reverse_graph = parse_input()
    transitive_counts = calculate_transitive_dependants(reverse_graph)
    direct_counts = calculate_direct_dependants(reverse_graph)
    problematic_package = find_most_problematic_package(transitive_counts, direct_counts)

    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic package found")

if __name__ == "__main__":
    main()
