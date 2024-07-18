"""
Alright, let's dive into this coding thing like we're searching for shoes on 
sale but for computer geek stuff instead! We're writing this program to figure 
out which package, among a bunch of 'em, gets the most "Oh no, not again" 
reactions because lots of other packages keep needing it, directly or 
indirectly. We want to find the one with the biggest fuss around it, in terms 
of who needs it the most overall, compared to just those who ask for it once. 
Sort of like finding the most popular drama queen in a soap opera!

Let's break this down into steps that even Sheldon would be proud of, or at 
least wouldn't complain too much about:
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
    dependencies = defaultdict(list)
    reverse_dependencies = defaultdict(list)
    for line in input.splitlines():
        first_package, first_version, second_package, second_version = line.split()
        first_package_version = (first_package, int(first_version))
        second_package_version = (second_package, int(second_version))
        dependencies[first_package_version].append(second_package_version)
        reverse_dependencies[second_package_version].append(first_package_version)
    return dependencies, reverse_dependencies

def compute_transitive_dependents(dependencies, reverse_dependencies):
    all_packages = set(dependencies.keys()).union(set(reverse_dependencies.keys()))
    transitive_count = {}
    for package in all_packages:
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            for dependent in reverse_dependencies[current]:
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
        # Subtract one to not count the package itself
        transitive_count[package] = len(visited) - 1
    return transitive_count

def find_most_problematic_package(dependencies, reverse_dependencies):
    transitive_dependents = compute_transitive_dependents(dependencies, reverse_dependencies)
    max_ratio = -1
    problematic_package = None
    for package, transitive in transitive_dependents.items():
        direct = len(reverse_dependencies[package])
        if direct > 0:  # Avoid division by zero
            ratio = transitive / direct
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package
    return problematic_package

def main():
    dependencies, reverse_dependencies = read_input()
    most_problematic = find_most_problematic_package(dependencies, reverse_dependencies)
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()
