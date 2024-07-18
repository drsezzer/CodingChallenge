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
from collections import defaultdict

def parse_input():
    direct_dependencies = defaultdict(list)
    all_packages = set()
    for line in input.splitlines():
        if line.strip():
            src_pkg, src_ver, dst_pkg, dst_ver = line.strip().split()
            src_ver, dst_ver = int(src_ver), int(dst_ver)
            direct_dependencies[(dst_pkg, dst_ver)].append((src_pkg, src_ver))
            all_packages.update([(src_pkg, src_ver), (dst_pkg, dst_ver)])
    return direct_dependencies, all_packages

def compute_transitive_dependents(dependencies, all_packages):
    transitive_dependents = {pkg: set() for pkg in all_packages}
    
    def dfs(current, origin):
        for dependent in dependencies[current]:
            if dependent not in transitive_dependents[origin]:
                transitive_dependents[origin].add(dependent)
                dfs(dependent, origin)

    for package in all_packages:
        dfs(package, package)
    
    return transitive_dependents

def calculate_problematic_ratio(direct_dependencies, transitive_dependents):
    ratios = {}
    for package in transitive_dependents:
        td = len(transitive_dependents[package])
        dd = len(direct_dependencies[package])
        if dd > 0:
            ratios[package] = td / dd
    return ratios

def find_most_problematic_package(ratios):
    return max(ratios, key=ratios.get) if ratios else None

def main():
    direct_dependencies, all_packages = parse_input()
    transitive_dependents = compute_transitive_dependents(direct_dependencies, all_packages)
    ratios = calculate_problematic_ratio(direct_dependencies, transitive_dependents)
    most_problematic_package = find_most_problematic_package(ratios)
    
    if most_problematic_package:
        print(f"{most_problematic_package[0]} {most_problematic_package[1]}")
    else:
        print("No problematic package found")

if __name__ == "__main__":
    main()
