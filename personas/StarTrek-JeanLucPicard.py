"""
Ah, a challenge worthy of a starship captain. Let us navigate through the stars 
of this programming task, with clarity and strategic foresight.

The mission: To create a program capable of deducing the most problematic 
dependency from a list. We will proceed with Python, a versatile tool, as our 
programming language.
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
    dependencies = defaultdict(list)
    direct_dependents_count = defaultdict(int)
    for line in input.strip().split('\n'): 
        if line.strip():
            first_package, first_version, second_package, second_version = line.split()
            first_version = int(first_version)
            second_version = int(second_version)
            dependencies[(second_package, second_version)].append((first_package, first_version))
            direct_dependents_count[(first_package, first_version)] += 1
    return dependencies, direct_dependents_count

def calculate_transitive_dependants(dependencies):
    transitive_dependants_count = defaultdict(int)
    
    for package_version in dependencies:
        visited = set()
        queue = deque([package_version])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            transitive_dependants_count[package_version] += 1
            for dependent in dependencies[current]:
                if dependent not in visited:
                    queue.append(dependent)
        transitive_dependants_count[package_version] -= 1  # Exclude itself
    return transitive_dependants_count

def find_most_problematic_package(dependencies, direct_dependents_count, transitive_dependants_count):
    max_ratio = -1
    problematic_package = None
    for package, transitive_count in transitive_dependants_count.items():
        if direct_dependents_count[package] > 0:
            ratio = transitive_count / direct_dependents_count[package]
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package
    return problematic_package

def main():
    dependencies, direct_dependents_count = read_input()
    transitive_dependants_count = calculate_transitive_dependants(dependencies)
    most_problematic_package = find_most_problematic_package(dependencies, direct_dependents_count, transitive_dependants_count)
    if most_problematic_package:
        print(f"{most_problematic_package[0]} {most_problematic_package[1]}")

if __name__ == "__main__":
    main()

