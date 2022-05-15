import math

import cv2 as cv
from collections import deque as queue

img = cv.imread('images/home-tests/resTest/upRight-858-121.png', 1)

distanceBetweenCameraAndNearEdgeOfImpactArea = 500
sideOfImpactArea = 400

height = img.shape[0]
width = img.shape[1]
rows = cols = 3
markerPointsColor = [255, 100, 100]
targetPointColor = [100, 100, 255]


def getTheta(p1, p2):
    dy = (p2[0] - p1[0])
    dx = (p2[1] - p1[1])
    result = 0
    if dx == 0:
        result = 90
    else:
        # result = (math.atan2(dy, dx) * -180) / math.pi
        result = math.atan2(dy, dx)
    return result


def getAvgTheta(p1, p2, p3):
    return float((getTheta(p1, p2) + getTheta(p1, p3) + getTheta(p2, p3)) / 3)


def getDistance(p1, p2):
    dy = (p2[0] - p1[0])
    dx = (p2[1] - p1[1])
    return math.sqrt(dy * dy + dx * dx)


def getTerminalPointCoordinate(knownPoint, yOfUnknownPoint, angle):
    xOfUnknownPoint = knownPoint[1] + int((yOfUnknownPoint - knownPoint[0]) / math.tan(angle))
    return [yOfUnknownPoint, xOfUnknownPoint]


vis = [[False for i in range(width)] for i in range(height)]


def check(h, w):
    py = img[h][w]

    if (py[0] == markerPointsColor[0]) and (py[1] == markerPointsColor[1]) and (py[2] == markerPointsColor[2]):
        return [True, True]
    elif (py[0] == targetPointColor[0]) and (py[1] == targetPointColor[1]) and (py[2] == targetPointColor[2]):
        return [True, False]
    else:
        return [False, False]


dRow = [-1, 0, 1, 0, 1, 1, -1, -1]
dCol = [0, 1, 0, -1, 1, -1, -1, 1]
numberOfNeighbors = len(dRow)


def isValid(row, col):
    if row < 0 or col < 0 or row >= height or col >= width:
        return False

    try:
        if vis[row][col]:
            return False
    except:
        print("---------------", row, col)
    return True


def BFS(row, col):
    q = queue()
    q.append((row, col))
    vis[row][col] = True

    count = 0
    t_x = 0
    t_y = 0

    while len(q) > 0:
        cell = q.popleft()
        x = cell[0]
        y = cell[1]

        t_x += x
        t_y += y
        count += 1

        for i in range(numberOfNeighbors):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            resFromChecking = check(adjx, adjy)
            if isValid(adjx, adjy) and resFromChecking[0]:
                q.append((adjx, adjy))
                vis[adjx][adjy] = True

    return [int(t_x / count), int(t_y / count)]


markers = []
impactPoint =[]

for i in range(height):
    for j in range(width):
        resFromChecking = check(i, j)
        if resFromChecking[0]:
            if not vis[i][j]:
                res = BFS(i, j)
                if resFromChecking[1]:
                    markers.append(res)
                else:
                    impactPoint.append(res)

impactPoint = impactPoint[0]

print("markers ", markers)
print("impactPoint ", impactPoint)

topLeft = []
topMid = []
topRight = []
midLeft = []
midMid = []
midRight = []
downLeft = []
downMid = []
downRight = []

if len(markers) == 4:

    midSum0 = 0
    midSum1 = 0

    for i in markers:
        midSum0 += i[0]
        midSum1 += i[1]

    midMid.append(int(midSum0 / len(markers)))
    midMid.append(int(midSum1 / len(markers)))

    for i in markers:
        if i[0] < midMid[0]:
            if i[1] < midMid[1]:
                topLeft.append(i[0])
                topLeft.append(i[1])
            else:
                topRight.append(i[0])
                topRight.append(i[1])
        else:
            if i[1] < midMid[1]:
                downLeft.append(i[0])
                downLeft.append(i[1])
            else:
                downRight.append(i[0])
                downRight.append(i[1])

    topMid.append(int((topLeft[0] + topRight[0]) / 2))
    topMid.append(int((topLeft[1] + topRight[1]) / 2))

    downMid.append(int((downLeft[0] + downRight[0]) / 2))
    downMid.append(int((downLeft[1] + downRight[1]) / 2))

    midLeft.append(int((topLeft[0] + downLeft[0]) / 2))
    midLeft.append(int((topLeft[1] + downLeft[1]) / 2))

    midRight.append(int((downRight[0] + topRight[0]) / 2))
    midRight.append(int((downRight[1] + topRight[1]) / 2))


elif len(markers) == 9:

    for i in range(rows):
        tmp = [markers[(i * rows) + 0], markers[(i * rows) + 1], markers[(i * rows) + 2]]
        tmp.sort()
        for j in tmp:
            temp = j[0] + j[1]
            j[0] = temp - j[0]
            j[1] = temp - j[0]
        tmp.sort()
        for j in tmp:
            temp = j[0] + j[1]
            j[0] = temp - j[0]
            j[1] = temp - j[0]
        for j in range(rows):
            markers[(i * rows) + j] = tmp[j]

    topLeft = markers[0]
    topMid = markers[1]
    topRight = markers[2]

    midLeft = markers[3]
    midMid = markers[4]
    midRight = markers[5]

    downLeft = markers[6]
    downMid = markers[7]
    downRight = markers[8]

markers = []

# print()
# print(topLeft, topMid, topRight)
# print(midLeft, midMid, midRight)
# print(downLeft, downMid, downRight)
# print()

thetaOfHorizontalTopLine = getAvgTheta(topLeft, topMid, topRight)
thetaOfHorizontalMidLine = getAvgTheta(midLeft, midMid, midRight)
thetaOfHorizontalDownLine = getAvgTheta(downLeft, downMid, downRight)
thetaOfVerticalLeftLine = getAvgTheta(downLeft, midLeft, topLeft)
thetaOfVerticalMidLine = getAvgTheta(downMid, midMid, topMid)
thetaOfVerticalRightLine = getAvgTheta(downRight, midRight, topRight)

farLength = getDistance(topLeft, topRight)
closeLength = getDistance(downLeft, downRight)


leftPoint = getTerminalPointCoordinate(downLeft, impactPoint[0], thetaOfVerticalLeftLine)
rightPoint = getTerminalPointCoordinate(downRight, impactPoint[0], thetaOfVerticalRightLine)
impactPointHorizontalLength = getDistance(leftPoint, rightPoint)
ratioForImpactInVertical = closeLength / impactPointHorizontalLength
verticalDistanceFromNearEdge = distanceBetweenCameraAndNearEdgeOfImpactArea * (ratioForImpactInVertical - 1)
totalVerticalDistanceFromCamera = verticalDistanceFromNearEdge + distanceBetweenCameraAndNearEdgeOfImpactArea
midPoint = [int((leftPoint[0] + rightPoint[0])/2), int((leftPoint[1] + rightPoint[1])/2)]
impactPointHorizontalLengthFromMidPoint = getDistance(midPoint, impactPoint)
ratioForImpactInHorizontal = (impactPointHorizontalLengthFromMidPoint * 2) / impactPointHorizontalLength
totalHorizontalDistanceFromMidVerticalLine = (sideOfImpactArea * ratioForImpactInHorizontal) / 2

""" 
    zones
    
  1 | 2 | 3
-------------
  4 | 5 | 6
-------------
  7 | 8 | 9
  
  5 -> target box 
  
"""

zone = 0
impactedLeftOrRight = ""
if totalVerticalDistanceFromCamera > distanceBetweenCameraAndNearEdgeOfImpactArea + sideOfImpactArea:
    # 1 2 3
    if totalHorizontalDistanceFromMidVerticalLine <= (sideOfImpactArea / 2):
        zone = 2
    else:
        if impactPoint[1] < midPoint[1]:
            zone = 1
            impactedLeftOrRight = "Left"
        else:
            zone = 3
            impactedLeftOrRight = "Right"
elif totalVerticalDistanceFromCamera > distanceBetweenCameraAndNearEdgeOfImpactArea:
    # 4 5 6
    if totalHorizontalDistanceFromMidVerticalLine <= (sideOfImpactArea / 2):
        zone = 5
    else:
        if impactPoint[1] < midPoint[1]:
            zone = 4
            impactedLeftOrRight = "Left"
        else:
            zone = 6
            impactedLeftOrRight = "Right"
else:
    # 7 8 9
    if totalHorizontalDistanceFromMidVerticalLine <= (sideOfImpactArea / 2):
        zone = 8
    else:
        if impactPoint[1] < midPoint[1]:
            zone = 7
            impactedLeftOrRight = "Left"
        else:
            zone = 9
            impactedLeftOrRight = "Right"


print("From the camera the impact point is ", totalVerticalDistanceFromCamera, "meters ahead vertically and",
      totalHorizontalDistanceFromMidVerticalLine, "meters", impactedLeftOrRight, "from the target point")
