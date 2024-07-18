""" Runs without modification, but gives b2 as result."""

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
    all_packages = set()
    
    for line in input.strip().split("\n"):
        if line.strip():
            first_package, first_version, second_package, second_version = line.split()
            first_version, second_version = int(first_version), int(second_version)
            # Each line indicates that first_package depends on second_package
            dependencies[(second_package, second_version)].append((first_package, first_version))
            direct_dependents_count[(second_package, second_version)] += 1
            all_packages.add((first_package, first_version))
            all_packages.add((second_package, second_version))
    
    return dependencies, direct_dependents_count, all_packages

def calculate_transitive_dependants(dependencies, all_packages):
    transitive_dependants_count = defaultdict(int)
    
    # Calculate transitive dependants for each package
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
        
        # Increment transitive count for each visited package (excluding itself)
        visited.remove(package_version)  # Remove the package itself from its transitive dependants
        for node in visited:
            transitive_dependants_count[node] += 1

    return transitive_dependants_count

def find_most_problematic_package(direct_dependents_count, transitive_dependants_count):
    max_ratio = -1
    problematic_package = None
    
    for package, direct_count in direct_dependents_count.items():
        if direct_count > 0:  # Avoid division by zero
            transitive_count = transitive_dependants_count[package]
            ratio = transitive_count / direct_count
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package
    
    return problematic_package

def main():
    dependencies, direct_dependents_count, all_packages = read_input()
    transitive_dependants_count = calculate_transitive_dependants(dependencies, all_packages)
    most_problematic_package = find_most_problematic_package(direct_dependents_count, transitive_dependants_count)
    if most_problematic_package:
        print(f"{most_problematic_package[0]} {most_problematic_package[1]}")

if __name__ == "__main__":
    main()
