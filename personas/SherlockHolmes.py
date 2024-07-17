input = """a 1 b 2
a 1 c 4
b 2 c 4
b 2 d 0
b 3 b 2
b 3 e 2
c 4 d 0
c 4 e 1"""


def read_input(input):
    #import sys
    #input = sys.stdin.read().strip()
    return input.split('\n')

def build_graph(dependencies):
    from collections import defaultdict
    graph = defaultdict(list)
    direct_dependents_count = defaultdict(int)
    
    for dep in dependencies:
        pkg1, ver1, pkg2, ver2 = dep.split()
        ver1 = int(ver1)
        ver2 = int(ver2)
        graph[(pkg2, ver2)].append((pkg1, ver1))
        direct_dependents_count[(pkg2, ver2)] += 1
    
    return graph, direct_dependents_count

def find_transitive_dependents(graph):
    from collections import defaultdict, deque
    transitive_dependents_count = defaultdict(int)
    
    def bfs(start):
        visited = set()
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for dependent in graph[node]:
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
                    transitive_dependents_count[start] += 1
                    
    nodes = list(graph.keys())
    for node in nodes:
        bfs(node)
    
    return transitive_dependents_count

def find_most_problematic_dependency(graph, direct_count, transitive_count):
    max_ratio = -1
    problematic_package = None
    
    for pkg, direct in direct_count.items():
        transitive = transitive_count.get(pkg, 0)
        if direct > 0:  # To avoid division by zero
            ratio = transitive / direct
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = pkg
    
    return problematic_package

def main():
    dependencies = read_input(input)
    graph, direct_dependents_count = build_graph(dependencies)
    transitive_dependents_count = find_transitive_dependents(graph)
    most_problematic = find_most_problematic_dependency(graph, direct_dependents_count, transitive_dependents_count)
    
    if most_problematic:
        print(f"{most_problematic[0]} {most_problematic[1]}")

if __name__ == "__main__":
    main()
