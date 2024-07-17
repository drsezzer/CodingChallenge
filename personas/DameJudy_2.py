"""
could you write me some code, but whilst assuming the character of dame judy 
dench, who is not technical, and has never programmed before?

here's the challenge
...

Oh, what a fascinating challenge! Well, my dear, while I've never professed 
to be an adept in the technological arena, let’s proceed with the spirit of 
a novice embracing a new script. We’re going to write a program, and it 
feels quite like learning lines for a new role, doesn’t it?

Our task, if I grasp it correctly—and do correct me if I stray—is to understand 
how these packages rely on each other, a bit like characters in a play 
depending on each other’s actions. We will write this in Python, which I’m told 
is a very approachable language, rather like starting with Shakespeare before 
venturing into more avant-garde playwrights.

Here is how I imagine this script might come to life
"""

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
    # First, we need to gather our cast of dependencies from the script we're handed (the input).
    dependencies = defaultdict(list)
    packages = set()

    # Reading from what's handed to us on the stage (standard input).
    for line in input.split('\n'): # sys.stdin:
        if line.strip():
            # Each line tells us who depends on whom, much like a stage direction.
            src_pkg, src_ver, dest_pkg, dest_ver = line.split()
            src = (src_pkg, int(src_ver))
            dest = (dest_pkg, int(dest_ver))
            dependencies[src].append(dest)
            packages.add(src)
            packages.add(dest)

    # Now, to find out who has the most on their shoulders (most problematic dependency).
    def count_transitive_dependents(package):
        # We will discover all the roles affected by this one, directly or indirectly.
        visited = set()
        queue = deque([package])
        while queue:
            current = queue.popleft()
            for dependent in dependencies[current]:
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
        return visited

    # We're comparing the weight each character has to bear.
    most_problematic = None
    max_ratio = -1

    for package in packages:
        # Direct dependents are those immediately influenced by our package.
        direct_dependents = {dep for src, dep_list in dependencies.items() for dep in dep_list if src == package}
        # Transitive dependents include the entire cascade of influence.
        all_dependents = count_transitive_dependents(package)
        
        if direct_dependents:
            ratio = len(all_dependents) / len(direct_dependents)
            if ratio > max_ratio:
                max_ratio = ratio
                most_problematic = package

    # And our conclusion, who carries the heaviest burden?
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()
