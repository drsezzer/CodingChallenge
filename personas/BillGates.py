"""
could you write me some code, but whilst assuming the character of Bill Gates?

here's the challenge


Alright, let's dive into the challenge you've outlined, using an approach that 
might resonate with my vision back in the early days of Microsoft—focusing on 
structure, efficiency, and robust software design. We're tasked with 
identifying a dependency problem within a software package management system, 
quite reminiscent of challenges we faced in the complex ecosystems of Windows 
development.

Notes: had to redirect: 'it throws a dictionary changed size exception' but just 
once, then it gave correct answer.
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

def main():
    input_lines = input.strip().split('\n')
    dependencies = defaultdict(list)
    reverse_dependencies = defaultdict(list)
    
    # Build the graph
    for line in input_lines:
        src, src_version, dst, dst_version = line.split()
        src = (src, int(src_version))
        dst = (dst, int(dst_version))
        dependencies[src].append(dst)
        reverse_dependencies[dst].append(src)
    
    # Compute all transitive and direct dependants
    transitive_dependents_count = {}
    all_packages = set(reverse_dependencies.keys()) | set(dependencies.keys())
    
    for package in all_packages:
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                queue.extend(reverse_dependencies[current])
        # Exclude the package itself from its dependants count
        transitive_dependents_count[package] = len(visited) - 1
    
    # Find the package with the highest ratio
    max_ratio = -1
    problematic_package = None
    for package in all_packages:
        direct_dependents = len(reverse_dependencies[package])
        total_dependents = transitive_dependents_count[package]
        if direct_dependents > 0:  # To avoid division by zero
            ratio = total_dependents / direct_dependents
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = package
    
    # Output the most problematic package
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic package found")

if __name__ == "__main__":
    main()
