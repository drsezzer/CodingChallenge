"""
Alright, let's tackle this programming challenge with the precise detail 
that Leonard Hofstadter would appreciate—balancing both his deep understanding 
of theoretical physics and his knack for dealing with Sheldon's quirks on a 
daily basis.
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

def parse_input():
    dependencies = defaultdict(list)
    for line in input.splitlines():
        if line.strip():
            src_pkg, src_ver, dst_pkg, dst_ver = line.split()
            src_ver, dst_ver = int(src_ver), int(dst_ver)
            dependencies[(src_pkg, src_ver)].append((dst_pkg, dst_ver))
    return dependencies

def find_transitive_dependents(dependencies):
    # To store transitive dependents count
    transitive_count = {pkg: set() for pkg in dependencies.keys()}
    
    def dfs(node, start):
        for dependent in dependencies[node]:
            if dependent not in transitive_count[start]:
                transitive_count[start].add(dependent)
                dfs(dependent, start)
                
    for pkg in list(dependencies.keys()):  # Work on a static list of keys
        dfs(pkg, pkg)
    
    return transitive_count

def calculate_problematic_ratio(dependencies, transitive_count):
    direct_count = {pkg: len(deps) for pkg, deps in dependencies.items()}
    ratio = {}

    for pkg, trans_deps in transitive_count.items():
        if direct_count[pkg] > 0:  # Prevent division by zero
            ratio[pkg] = len(trans_deps) / direct_count[pkg]

    return ratio

def find_most_problematic_package(ratio):
    return max(ratio, key=ratio.get, default=None)

def main():
    dependencies = parse_input()
    transitive_count = find_transitive_dependents(dependencies)
    ratio = calculate_problematic_ratio(dependencies, transitive_count)
    most_problematic = find_most_problematic_package(ratio)
    
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")
    else:
        print("No dependencies found")

if __name__ == "__main__":
    main()
