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
    # Reading input and building the graph
    dependencies = defaultdict(list)
    dependants = defaultdict(set)

    try:
        for line in input.splitlines():
            if line.strip():
                pkg1, ver1, pkg2, ver2 = line.split()
                ver1, ver2 = int(ver1), int(ver2)
                dependencies[(pkg1, ver1)].append((pkg2, ver2))
                dependants[(pkg2, ver2)].add((pkg1, ver1))
    except Exception as e:
        print("Error reading input:", e)
        sys.exit(1)

    return dependencies, dependants

def calculate_transitive_dependants(dependants):
    # Calculates all transitive dependants using a BFS approach
    all_dependants = {}
    for package in list(dependants.keys()):  # Work with a list of keys to avoid dictionary change during iteration
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

def find_most_problematic(dependencies, all_dependants):
    max_ratio = -1
    problematic_package = None

    for package in list(dependencies.keys()):  # Similarly, use list to avoid runtime dictionary change issues
        if package in all_dependants:
            transitive_count = len(all_dependants[package])
            direct_count = len(dependencies[package])
            if direct_count > 0:  # Avoid division by zero
                ratio = transitive_count / direct_count
                if ratio > max_ratio:
                    max_ratio = ratio
                    problematic_package = package

    return problematic_package

def main():
    dependencies, dependants = read_dependencies()
    all_dependants = calculate_transitive_dependants(dependants)
    problematic_package = find_most_problematic(dependencies, all_dependants)
    
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic package found.")

if __name__ == "__main__":
    main()
