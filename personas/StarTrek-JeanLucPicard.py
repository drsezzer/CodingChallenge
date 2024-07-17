""" Aftering 2 attempts to get passed dictionary changed exception, this orked
but result as b3!
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
            first_version, second_version = int(first_version), int(second_version)
            dependencies[(second_package, second_version)].append((first_package, first_version))
            direct_dependents_count[(first_package, first_version)] += 1
    return dependencies, direct_dependents_count

def calculate_transitive_dependants(dependencies):
    transitive_dependants_count = defaultdict(int)
    all_packages = list(dependencies.keys())  # Take a snapshot of all keys to avoid runtime changes

    for package_version in all_packages:
        visited = set()
        queue = deque([package_version])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for dependent in dependencies[current]:
                if dependent not in visited:
                    queue.append(dependent)
        # Count each unique visit except the starting node
        for node in visited:
            if node != package_version:
                transitive_dependants_count[node] += 1
    return transitive_dependants_count

def find_most_problematic_package(direct_dependents_count, transitive_dependants_count):
    max_ratio = -1
    problematic_package = None
    for package, transitive_count in transitive_dependants_count.items():
        direct_count = direct_dependents_count[package]
        if direct_count > 0:  # Prevent division by zero
            ratio = transitive_count / direct_count
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package
    return problematic_package

def main():
    dependencies, direct_dependents_count = read_input()
    transitive_dependants_count = calculate_transitive_dependants(dependencies)
    most_problematic_package = find_most_problematic_package(direct_dependents_count, transitive_dependants_count)
    if most_problematic_package:
        print(f"{most_problematic_package[0]} {most_problematic_package[1]}")

if __name__ == "__main__":
    main()
