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
    inverse_dependencies = defaultdict(set)
    for line in input.splitlines():
        if line.strip():
            src_pkg, src_ver, dst_pkg, dst_ver = line.split()
            src_ver, dst_ver = int(src_ver), int(dst_ver)
            dependencies[(dst_pkg, dst_ver)].append((src_pkg, src_ver))
            inverse_dependencies[(src_pkg, src_ver)].add((dst_pkg, dst_ver))
    return dependencies, inverse_dependencies

def find_transitive_dependents(dependencies):
    transitive_count = defaultdict(set)
    
    def dfs(node, start):
        for dependent in dependencies[node]:
            if dependent not in transitive_count[start]:
                transitive_count[start].add(dependent)
                dfs(dependent, start)

    for pkg in dependencies:
        dfs(pkg, pkg)
    
    return {pkg: len(deps) for pkg, deps in transitive_count.items()}

def calculate_problematic_ratio(dependencies, transitive_count):
    direct_count = {pkg: len(dependencies[pkg]) for pkg in dependencies}
    ratio = {}

    for pkg in transitive_count:
        if direct_count.get(pkg, 0) > 0:
            ratio[pkg] = transitive_count[pkg] / direct_count[pkg]

    return ratio

def find_most_problematic_package(ratio):
    return max(ratio, key=ratio.get, default=None)

def main():
    dependencies, inverse_dependencies = parse_input()
    transitive_count = find_transitive_dependents(inverse_dependencies)
    ratio = calculate_problematic_ratio(inverse_dependencies, transitive_count)
    most_problematic = find_most_problematic_package(ratio)
    
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")
    else:
        print("No dependencies found")

if __name__ == "__main__":
    main()
