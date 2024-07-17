input = """a 1 b 2
a 1 c 4
b 2 c 4
b 2 d 0
b 3 b 2
b 3 e 2
c 4 d 0
c 4 e 1
"""


def read_dependencies():
    import sys
    # Here, we gather the tales of dependencies, each line a narrative of need.
    # input_lines = sys.stdin.read().strip()
    input_lines = input.strip()
    return input_lines.split('\n')

def construct_the_web(dependencies):
    from collections import defaultdict
    graph = defaultdict(list)
    direct_followers = defaultdict(int)
    
    # We weave the web of dependencies, connecting tales of packages and their seekers.
    for dependency in dependencies:
        benefactor, benefactor_version, beneficiary, beneficiary_version = dependency.split()
        benefactor_version = int(benefactor_version)
        beneficiary_version = int(beneficiary_version)
        graph[(beneficiary, beneficiary_version)].append((benefactor, benefactor_version))
        direct_followers[(beneficiary, beneficiary_version)] += 1
    
    return graph, direct_followers

def count_transitive_followers(graph):
    from collections import defaultdict, deque
    transitive_followers = defaultdict(int)
    
    # A journey through the web, counting those who follow, near and far.
    def traverse(web_start):
        visited = set()
        queue = deque([web_start])
        while queue:
            current = queue.popleft()
            for follower in graph[current]:
                if follower not in visited:
                    visited.add(follower)
                    queue.append(follower)
                    transitive_followers[web_start] += 1
                    
    # We embark on this traversal for each node in our web.
    all_nodes = list(graph.keys())
    for node in all_nodes:
        traverse(node)
    
    return transitive_followers

def identify_culprit(graph, direct, transitive):
    highest_drama = -1
    central_character = None
    
    # Who bears the weight of most tales? Who is the linchpin of our narrative?
    for character, direct_followers in direct.items():
        indirect_tales = transitive.get(character, 0)
        if direct_followers > 0:  # We seek not those with no followers
            drama = indirect_tales / direct_followers
            if drama > highest_drama:
                highest_drama = drama
                central_character = character
    
    return central_character

def main():
    dependencies = read_dependencies()
    graph, direct_followers = construct_the_web(dependencies)
    transitive_followers = count_transitive_followers(graph)
    protagonist = identify_culprit(graph, direct_followers, transitive_followers)
    
    if protagonist:
        print(f"{protagonist[0]} {protagonist[1]}")

if __name__ == "__main__":
    main()
