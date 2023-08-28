import sys

def dfs(node, parent, L, dp, graph):
    dp[node] = L[node]
    for neighbor in graph[node]:
        if neighbor != parent:
            dp[node] += min(dfs(neighbor, node, L, dp, graph), 0)
    return dp[node]

def solve(N, L, roads):
    graph = [[] for _ in range(N + 1)]
    for u, v in roads:
        graph[u].append(v)
        graph[v].append(u)
    
    result = []
    for start in range(1, N + 1):
        dp = [0] * (N + 1)
        spending = dfs(start, -1, L, dp, graph)
        result.append(spending)
    
    return result

def main():
    N = int(input())
    L = [0] + list(map(int, input().split()))  # Adding a dummy value at the beginning for 1-based indexing
    
    roads = []
    for _ in range(N - 1):
        u, v = map(int, input().split())
        roads.append((u, v))
    
    result = solve(N, L, roads)
    print(*result)

if __name__ == "__main__":
    main()
