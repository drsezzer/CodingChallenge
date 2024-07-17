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

def main():
    dependencies = defaultdict(list)
    direct_dependants = defaultdict(set)
    
    # Read input lines
    for line in input.split('\n'): # sys.stdin:
        if line.strip():
            src_pkg, src_ver, dest_pkg, dest_ver = line.split()
            src = (src_pkg, int(src_ver))
            dest = (dest_pkg, int(dest_ver))
            dependencies[src].append(dest)
            direct_dependants[dest].add(src)

    # Function to find all transitive dependants
    def find_transitive_dependants(package):
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            for dependent in dependencies[current]:
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
        return visited

    # Determine the most problematic package
    most_problematic = None
    highest_ratio = -1
    
    # Compute for each package that has at least one direct dependent
    for package in direct_dependants:
        transitive_dependants = find_transitive_dependants(package)
        direct_deps = direct_dependants[package]
        ratio = len(transitive_dependants) / len(direct_deps)
        print(f"Package: {package}, Ratio: {ratio}, Transitive: {len(transitive_dependants)}, Direct: {len(direct_deps)}")  # Debug output
        if ratio > highest_ratio:
            highest_ratio = ratio
            most_problematic = package

    if most_problematic:
        print(f"Most problematic package: {most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()
