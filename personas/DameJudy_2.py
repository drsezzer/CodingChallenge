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
    reverse_dependencies = defaultdict(set)
    
    # Parse input and construct dependency graph and reverse graph
    for line in input.strip().split("\n"):
        if line.strip():
            src_pkg, src_ver, dest_pkg, dest_ver = line.split()
            src = (src_pkg, int(src_ver))
            dest = (dest_pkg, int(dest_ver))
            dependencies[src].append(dest)
            reverse_dependencies[dest].add(src)

    # Function to find all transitive dependents using the reverse graph
    def find_all_dependents(package):
        all_dependents = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            for dep in reverse_dependencies[current]:
                if dep not in all_dependents:
                    all_dependents.add(dep)
                    queue.append(dep)
        return all_dependents

    # Compute most problematic package
    most_problematic = None
    highest_ratio = -1

    # Create a static list of packages to iterate over to avoid dictionary size modification issues
    packages_list = list(reverse_dependencies.keys())
    
    # Compute for each package
    for package in packages_list:
        transitive_dependents = find_all_dependents(package)
        direct_deps = reverse_dependencies[package]
        ratio = len(transitive_dependents) / len(direct_deps)
        print(f"Package: {package}, Ratio: {ratio}, Transitive: {len(transitive_dependents)}, Direct: {len(direct_deps)}")  # Debug output
        if ratio > highest_ratio:
            highest_ratio = ratio
            most_problematic = package

    if most_problematic:
        print(f"Most problematic package: {most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()

