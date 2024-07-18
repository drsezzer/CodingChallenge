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
    direct_dependents = defaultdict(set)

    for line in input.strip().split("\n"):
        if line.strip():
            # Parse the input line
            src_pkg, src_ver, dst_pkg, dst_ver = line.split()
            src_ver, dst_ver = int(src_ver), int(dst_ver)
            # src depends on dst
            dependencies[(dst_pkg, dst_ver)].append((src_pkg, src_ver))
            direct_dependents[(dst_pkg, dst_ver)].add((src_pkg, src_ver))
            
    return dependencies, direct_dependents

def calculate_transitive_dependants(dependencies, direct_dependents):
    transitive_dependents = defaultdict(set)

    # Process each package-version pair
    for pkg_ver in dependencies:
        visited = set()
        queue = deque([pkg_ver])
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for dependent in dependencies.get(current, []):
                if dependent not in visited:
                    queue.append(dependent)
                    transitive_dependents[pkg_ver].add(dependent)
        
        # Remove direct dependents from transitive dependents to avoid double counting
        transitive_dependents[pkg_ver] -= direct_dependents[pkg_ver]

    return transitive_dependents

def find_most_problematic_package(direct_dependents, transitive_dependents):
    max_ratio = -1
    problematic_package = None

    for pkg_ver, dependents in direct_dependents.items():
        if dependents:
            trans_count = len(transitive_dependents[pkg_ver])
            direct_count = len(dependents)
            ratio = trans_count / direct_count
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = pkg_ver

    return problematic_package

def main():
    dependencies, direct_dependents = read_input()
    transitive_dependents = calculate_transitive_dependants(dependencies, direct_dependents)
    most_problematic_package = find_most_problematic_package(direct_dependents, transitive_dependents)

    if most_problematic_package:
        print(f"{most_problematic_package[0]} {most_problematic_package[1]}")

if __name__ == "__main__":
    main()
