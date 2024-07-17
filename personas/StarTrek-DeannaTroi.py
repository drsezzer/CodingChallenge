"""
Redirected with:
'it throws a dictionary change exception for line: 'for package in dependcies''
... but this time it works and give answer e1!!
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
        for line in input.strip().split("\n"):
            parts = line.strip().split()
            if len(parts) == 4:
                depender = (parts[0], int(parts[1]))
                dependee = (parts[2], int(parts[3]))
                dependencies.append((depender, dependee))
    except Exception as e:
        print("Error reading input:", e)
    return dependencies

def analyze_dependencies(dependencies):
    # Maps package (name, version) to a list of packages that depend on it directly
    dependents = defaultdict(list)
    # Maps package to a list of packages it directly depends on
    direct_dependencies = defaultdict(list)
    
    for depender, dependee in dependencies:
        dependents[dependee].append(depender)
        direct_dependencies[depender].append(dependee)
    
    # To find transitive dependents, we'll use a breadth-first search (BFS) approach
    transitive_count = defaultdict(int)
    # Prepare a set of all unique packages from dependencies
    all_packages = set(dependents.keys()).union(set(direct_dependencies.keys()))
    
    for package in all_packages:
        seen = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            for dependent in dependents[current]:
                if dependent not in seen:
                    seen.add(dependent)
                    queue.append(dependent)
        # Do not count the package itself
        transitive_count[package] = len(seen) - 1 if package in seen else len(seen)
    
    # Now calculate the ratio for each package and determine the most problematic one
    most_problematic = None
    highest_ratio = -1
    
    for package in all_packages:
        direct_count = len(dependents[package])
        if direct_count > 0:  # Avoid division by zero
            ratio = transitive_count[package] / direct_count
            if ratio > highest_ratio:
                highest_ratio = ratio
                most_problematic = package
    
    return most_problematic

def main():
    dependencies = read_input()
    most_problematic = analyze_dependencies(dependencies)
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")
    else:
        print("No dependencies found or unable to determine the most problematic.")

if __name__ == "__main__":
    main()
