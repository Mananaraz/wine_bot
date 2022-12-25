import math

graph = {}
points_in_graph = []
n = len(graph)
Visited = []


def main():
    cuts_count = int(input())
    for i in range(cuts_count):
        input_vertex()
    get_graph()
    comps_count, extra_slices = get_comps_count()
    print(extra_slices + comps_count - 1)


def input_vertex():
    input()
    points = []
    coords = [int(x) for x in input().split()]

    for i in range(len(coords) - 1):
        if i % 2 == 0:
            point = (coords[i], coords[i + 1])
            if point not in graph:
                graph[point] = set()
            points.append(point)

    points_in_graph.append(points)


def print_formatted_dict(dictionary):
    for key in dictionary.keys():
        print(f'{key}: {dictionary[key]}')


def get_graph():
    for points_block in points_in_graph:
        for ind in range(len(points_block) - 1):
            graph[points_block[ind]].add(points_block[ind + 1])
            graph[points_block[ind + 1]].add(points_block[ind])


def DFS(start):
    stack = [start]
    comp = 0
    while stack:
        vertex = stack.pop()
        if vertex not in Visited:
            Visited.append(vertex)
            if len(graph[vertex]) % 2 != 0:
                comp += 1
            stack.extend(set(graph[vertex]) - set(Visited))
    return comp // 2 - 1 if comp > 0 else 0


def get_comps_count():
    comps_count = 0
    odd_count = 0
    for i in graph.keys():
        if i not in Visited:
            comps_count += 1
            odd_count += (DFS(i))
    return comps_count, odd_count


if __name__ == '__main__':
    main()
