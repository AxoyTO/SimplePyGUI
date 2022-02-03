from math import sqrt, factorial
from itertools import permutations


# Euclidean distance between two points
def findDistance(point1: tuple, point2: tuple):
    return sqrt(abs((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2))


def shortestPath(points: list):
    startPoint = points.pop(0)
    paths = list(list(x) for x in permutations(points))

    for i in range(len(paths)):
        paths[i].append(startPoint)

    pathsWithDistances = {}
    distances = []
    for path in paths:
        string = f"{startPoint} -> {path[0]}["
        sum = findDistance(startPoint, path[0])
        string += f"{sum}]"
        for i in range(len(path) - 1):
            string += f" -> {path[i + 1]}["
            sum += findDistance(path[i], path[i + 1])
            string += f"{sum}]"
        string += f" = {sum}"
        pathsWithDistances[string] = sum
        distances.append(sum)
    shortestDistance = min(distances)

    keys = list(pathsWithDistances.keys())
    vals = list(pathsWithDistances.values())
    for i in range(len(vals)):
        if vals[i] == shortestDistance:
            print(keys[i])


point_1 = (0, 2)  # Почтовое отделение
point_2 = (2, 5)  # Ул. Грибоедова, 104/25
point_3 = (5, 2)  # Ул. Бейкер стрит, 221б
point_4 = (6, 6)  # Ул. Большая Садовая, 302-бис
point_5 = (8, 3)  # Вечнозелёная Аллея, 742

points = [point_1, point_2, point_3, point_4, point_5]
shortestPath(points)
