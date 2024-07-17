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

def main():
    # We'll read our inputs, the relations of dependencies.
    dependencies = defaultdict(list)
    dependants = defaultdict(set)

    # We must understand each line of input, interpreting the dependencies.
    for line in input.split('\n'): # sys.stdin
        if line.strip():
            src_pkg, src_ver, dest_pkg, dest_ver = line.split()
            src = (src_pkg, int(src_ver))
            dest = (dest_pkg, int(dest_ver))
            dependencies[src].append(dest)
            dependants[dest].add(src)

    # Now, we determine the reach of each package, both direct and by extension.
    def count_transitive_dependents(package):
        # Let's find out how many are indirectly dependent on our package.
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            for dependent in dependencies[current]:
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
        return visited

    # We seek the character with the deepest connections.
    most_problematic = None
    max_ratio = -1

    for package in dependants:
        # Direct dependents are those immediately reliant on our package.
        direct_dependents = dependants[package]
        # Transitive dependents include the full range of influence.
        all_dependents = count_transitive_dependents(package)
        
        if direct_dependents:
            ratio = len(all_dependents) / len(direct_dependents)
            if ratio > max_ratio:
                max_ratio = ratio
                most_problematic = package

    # We'll announce the one with the heaviest burden to carry.
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()
