import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def proximity_score(max_distance=0.2, *landmarks):
    points = [(lm.x, lm.y) for lm in landmarks]
    
    max_d = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = distance(points[i], points[j])
            if d > max_d:
                max_d = d
    
    if max_d >= max_distance:
        return 0
    else:
        return 1 - (max_d / max_distance)
