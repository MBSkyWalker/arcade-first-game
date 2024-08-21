# array_2d = [
#     [1, 2, 3, 4, 5],
#     [6, 7, 8, 9, 10],
#     [11, 12, 13, 14, 15],
#     [16, 17, 18, 19, 20]
# ]
#
# print(array_2d[3][4])
#
# from collections import deque
#
# graph = {}
# graph['you'] = ['alice', 'bob', 'claire']
# graph['bob'] = ['anuj', 'peggy']
# graph['alice'] = ['peggy']
# graph['claire'] = ['thom', 'jonny']
# graph['anuj'] = []
# graph['peggy'] = []
# graph['thom'] = []
# graph['jonny'] = []
#
# print(graph)
# def person_is_seller(person):
#     return person[-1] == 'm'
#
#
# def bfs(graph, start):
#     search_queue = deque()
#     search_queue += graph[start]
#
#     searched = []
#
#     while search_queue:
#         person = search_queue.popleft()
#
#         print(search_queue)
#         if person not in searched:
#             if person_is_seller(person):
#                 print(person + " is a mango seller!")
#                 return True
#             else:
#                 search_queue += graph[person]
#     return False
#
#
# print(bfs(graph, 'you'))
graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8'],
  '8' : []
}

visited = [] # List for visited nodes.
queue = []     #Initialize a queue

def bfs(visited, graph, node): #function for BFS
  visited.append(node)
  queue.append(node)

  while queue:          # Creating loop to visit each node
    m = queue.pop(0)
    print(m, end=" ")

    for neighbour in graph[m]:
      print(graph[m], neighbour)
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

# Driver Code
print("Following is the Breadth-First Search")
bfs(visited, graph, '5')    # function calling


from pyglet.math import Vec2

# Створюємо два вектори
vector1 = Vec2(3, 4)
vector2 = Vec2(1, 2)

# Додавання векторів
result_vector = vector1 + vector2

# Виводимо результат
print(f"Результат додавання: ({result_vector.x}, {result_vector.y})")
