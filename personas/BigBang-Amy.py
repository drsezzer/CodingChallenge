""" GPT4o
Sure, I'll write the program for you in Python, keeping the style and 
mannerisms of Amy Farrah Fowler from The Big Bang Theory in mind. Amy is known 
for her precision, intelligence, and sometimes verbose explanations. Here's 
how she might write the program:
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

class DependencyGraph:
    def __init__(self):
        self.dependencies = defaultdict(set)
        self.reverse_dependencies = defaultdict(set)
        self.direct_dependants = defaultdict(int)
        self.transitive_dependants = defaultdict(set)

    def add_dependency(self, package_from, version_from, package_to, version_to):
        key_from = (package_from, version_from)
        key_to = (package_to, version_to)
        self.dependencies[key_from].add(key_to)
        self.reverse_dependencies[key_to].add(key_from)
        self.direct_dependants[key_from] += 1

    def calculate_transitive_dependants(self):
        for package in list(self.dependencies.keys()):
            visited = set()
            queue = deque([package])
            while queue:
                current = queue.popleft()
                if current not in visited:
                    visited.add(current)
                    for neighbour in self.dependencies[current]:
                        self.transitive_dependants[neighbour].add(package)
                        queue.append(neighbour)
    
    def find_most_problematic_dependency(self):
        self.calculate_transitive_dependants()
        max_ratio = -1
        most_problematic = None

        for package, trans_dependants in self.transitive_dependants.items():
            direct_dependants = self.direct_dependants[package]
            if direct_dependants > 0:
                ratio = len(trans_dependants) / direct_dependants
                if ratio > max_ratio:
                    max_ratio = ratio
                    most_problematic = package

        return most_problematic

def main():
    dependency_graph = DependencyGraph()
    
    for line in input.splitlines():
        parts = line.strip().split()
        if len(parts) != 4:
            print("Error: Each line must contain exactly four parts.")
            return
        
        package_from = parts[0]
        version_from = int(parts[1])
        package_to = parts[2]
        version_to = int(parts[3])
        
        dependency_graph.add_dependency(package_from, version_from, package_to, version_to)
    
    most_problematic = dependency_graph.find_most_problematic_dependency()
    
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")
    else:
        print("No dependencies found or input format is incorrect.")

if __name__ == "__main__":
    main()
