def dfs(current, target, steps):
    if steps > 6:
        return False
    if current == target:
        return True
    
    visited[current] = True
    for neighbor in graph[current]:
        if not visited[neighbor]:
            if dfs(neighbor, target, steps + 1):
                return True
    visited[current] = False
    
    return False

T = int(input())

for _ in range(T):
    n, m = map(int, input().split())
    
    graph = [[] for _ in range(n)]
    visited = [False] * n
    
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
    
    src, dst = map(int, input().split())
    
    if dfs(src, dst, 0):
        print("YES")
    else:
        print("NO")
