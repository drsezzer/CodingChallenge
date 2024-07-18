"""
As I channel my inner Amy Farrah Fowler, let's tackle this fascinating 
programming puzzle, which involves analyzing dependency graphs—a topic that, 
as an enthusiastic neurobiologist, I find tangentially similar to mapping 
neural connections, albeit with packages and versions instead of neurons and 
synapses.
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
    # Reading from standard input and parsing
    dependencies = defaultdict(list)
    for line in input.splitlines():
        src_package, src_version, dst_package, dst_version = line.split()
        src_version, dst_version = int(src_version), int(dst_version)
        dependencies[(src_package, src_version)].append((dst_package, dst_version))
    return dependencies

def calculate_transitive_dependents(dependencies):
    # Reverse the dependency graph to find dependents
    dependents = defaultdict(set)
    for package, deps in dependencies.items():
        for dep in deps:
            dependents[dep].add(package)
    
    # Calculate transitive closure using BFS
    transitive_dependents = {}
    for package in dependents:
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            for dependent in dependents[current]:
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
        transitive_dependents[package] = visited

    return transitive_dependents

def find_most_problematic_package(dependencies):
    # Calculate direct and transitive dependents
    direct_dependents = defaultdict(set)
    for package, deps in dependencies.items():
        for dep in deps:
            direct_dependents[dep].add(package)
    
    transitive_dependents = calculate_transitive_dependents(dependencies)
    
    # Calculate the most problematic package
    max_ratio = -1
    problematic_package = None
    for package, trans_deps in transitive_dependents.items():
        direct_count = len(direct_dependents[package])
        transitive_count = len(trans_deps)
        if direct_count > 0:  # to avoid division by zero
            ratio = transitive_count / direct_count
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package
    
    return problematic_package

def main():
    dependencies = read_dependencies()
    problematic_package = find_most_problematic_package(dependencies)
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No dependencies found.")

if __name__ == "__main__":
    main()
