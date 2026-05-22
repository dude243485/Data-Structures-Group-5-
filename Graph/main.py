

hashMap = {
    1 : [9, 6, 5],
    5 : [6, 1, 4],
    4 : [5, 8, 10, 3],
    8 : [4, 2, 10],
    10 : [8, 4, 6, 2 ],
    2 : [8, 10, 6, 7],
    7 : [2, 6, 3],
    3 : [6, 4, 9],
    9 : [3, 1, 6],
    6 : [1, 5, 9, 3, 10, 7 , 2]
}

def dfs(start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        print(node, end = " ")
        for n in hashMap[node]:
            if n not in visited:
                stack.append(n)
                
def bfs(start):
    visited = set()
    queue = [start]
    visited.add(start)
    
    while queue:
        node = queue.pop(0)
        print(node, end=" ")
        for n in hashMap[node]:
            if n not in visited:
                visited.add(n)
                queue.append(n)
  
  
print("Depth first search : ") 
#enter your start node into  the dfs function          
dfs(1)
print()
print("Breadth first search :  ")
#enter your start node into  the bfs function
bfs(1)