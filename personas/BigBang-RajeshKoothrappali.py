"""
Oh, my Raj! Challenge accepted! This is like figuring out the celestial 
echanics of heavenly bodies, but with software packages and their 
dependencies instead. I'll be crafting a Python script that does just 
that.

Here's the plan: We'll dive into this cosmic network of dependencies 
and compute which package is the most "problematic" — sounds a bit 
like my social interactions at parties, doesn't it? We'll need to 
calculate the ratio of transitive dependents to direct dependents 
for each package and version.
"""

_input = """a 1 b 2
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
    # Collecting dependency information for graph traversal.
    dependencies = defaultdict(list)
    dependents = defaultdict(list)
    input = _input.splitlines()
    for line in input:
        if line.strip():
            src, src_ver, dest, dest_ver = line.split()
            src, dest = (src, int(src_ver)), (dest, int(dest_ver))
            dependencies[src].append(dest)
            dependents[dest].append(src)
    return dependencies, dependents

def calculate_transitive_dependents(dependents):
    # Using breadth-first search to find all transitive dependents.
    transitive_count = {}
    for package in list(dependents):
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for dependent in dependents[current]:
                if dependent not in visited:
                    queue.append(dependent)
        # Don't count the package itself as its dependent.
        transitive_count[package] = len(visited) - 1
    return transitive_count

def find_most_problematic(dependencies, dependents):
    transitive_dependents = calculate_transitive_dependents(dependents)
    most_problematic = None
    highest_ratio = -1
    
    # Calculating the ratio of transitive dependants to direct dependants
    for package in list(dependents):
        direct_dependent_count = len(dependents[package])
        transitive_dependent_count = transitive_dependents.get(package, 0)
        if direct_dependent_count > 0:
            ratio = transitive_dependent_count / direct_dependent_count
            if ratio > highest_ratio:
                highest_ratio = ratio
                most_problematic = package

    return most_problematic

def main():
    dependencies, dependents = read_input()
    most_problematic = find_most_problematic(dependencies, dependents)
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")
    else:
        print("No dependencies found.")

if __name__ == "__main__":
    main()
