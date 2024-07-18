"""
Ah, stepping into the shoes of Howard Wolowitz, huh? Alright, let's tackle this 
using my engineer's prowess, and perhaps with a dash of his flair for the 
dramatic and technical. We're going to crack this challenge by calculating the 
dependency ratios in a universe where dependencies aren’t just relationships 
but an intricate dance of software ballet.
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

def read_dependencies():
    dependencies = defaultdict(list)
    dependants = defaultdict(set)

    # Reading input from standard input
    input_data = input.splitlines()
    for line in input_data:
        if line.strip():
            pkg1, ver1, pkg2, ver2 = line.split()
            ver1, ver2 = int(ver1), int(ver2)
            # pkg1 depends on pkg2
            dependencies[(pkg1, ver1)].append((pkg2, ver2))
            # pkg2 is depended on by pkg1
            dependants[(pkg2, ver2)].add((pkg1, ver1))

    return dependencies, dependants

def calculate_transitive_dependants(dependants):
    all_dependants = {}
    for package in dependants:
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for neighbor in dependants[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        all_dependants[package] = visited - {package}  # Remove the package itself from its dependants
    return all_dependants

def find_most_problematic(dependants, all_dependants):
    max_ratio = -1
    problematic_package = None

    for package, transitive_deps in all_dependants.items():
        transitive_count = len(transitive_deps)
        direct_count = len(dependants[package])  # Direct dependants
        if direct_count > 0:  # To avoid division by zero
            ratio = transitive_count / direct_count
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package

    return problematic_package

def main():
    dependencies, dependants = read_dependencies()
    all_dependants = calculate_transitive_dependants(dependants)
    problematic_package = find_most_problematic(dependants, all_dependants)
    
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic package found.")

if __name__ == "__main__":
    main()
