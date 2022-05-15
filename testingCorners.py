import math
from queue import Queue

import cv2

rows = cols = 3




img = cv2.imread('images/home-tests/another.png', 1)

height = img.shape[0]
width = img.shape[1]

largerProperty = width

points = []
if height > width:
    largerProperty = height

multiplicationFactor = int(math.pow(10, int(math.log10(largerProperty) + 1)))

for i in range(height):
    for j in range(width):
        # bgr
        if img[i][j][0] == 255 and img[i][j][1] == 100 and img[i][j][2] == 100:
            points.append(int((i * multiplicationFactor) + j))


"""

cornerCount = 0
actualCornerCount = 9
initialPointsCount = len(points)
pixelNeighborFactor = 5

neighborCount = 0
sumX = 0
sumY = 0

for i in range(initialPointsCount - 1):
    x1 = int(points[i] % multiplicationFactor)
    y1 = int(points[i] / multiplicationFactor)
    if neighborCount == 0:
        sumX = sumX + x1
        sumY = sumY + y1
        neighborCount = neighborCount + 1
    x2 = int(points[i + 1] % multiplicationFactor)
    y2 = int(points[i + 1] / multiplicationFactor)

    if (math.fabs(x1 - x2) < pixelNeighborFactor) and (math.fabs(y1 - y2) < pixelNeighborFactor):
        sumX = sumX + x2
        sumY = sumY + y2
        neighborCount = neighborCount + 1
    else:
        X = int(sumX / neighborCount)
        Y = int(sumY / neighborCount)
        targetPoints.append([Y, X])
        neighborCount = 0
        sumX = 0
        sumY = 0

x1 = int(points[initialPointsCount - 2] % multiplicationFactor)
y1 = int(points[initialPointsCount - 2] / multiplicationFactor)
x2 = int(points[initialPointsCount - 1] % multiplicationFactor)
y2 = int(points[initialPointsCount - 1] / multiplicationFactor)
if (math.fabs(x1 - x2) < pixelNeighborFactor) and (math.fabs(y1 - y2) < pixelNeighborFactor):
    pass
else:
    targetPoints.append([y2, x2])

points = []

for i in range(rows):
    tmpPoints = []
    for j in range(cols):
        tmpPoint = targetPoints[j]
        tmpPoints.append([tmpPoint[1], tmpPoint])
    tmpPoints.sort()
    for j in tmpPoints:
        targetPoints.append(j[1])
        targetPoints.pop(0)

print(len(targetPoints))
print(targetPoints)

for i in targetPoints:
    img[i[0]][i[1]] = [0, 0, 0]
    cv2.imwrite('anotherEdited.png', img)

# (y,x) ||| (0,0) -> top left


"""
