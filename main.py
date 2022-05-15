import math

a = []

row = 10
col = 10

for i in range(row):
    tmp = []
    for j in range(col):
        tmp.append((i * row) + j)
    a.append(tmp)

"""

for i in range(row):
    for j in range(col):
        aa = int(a[i][j])
        spaces = 0
        if aa > 0:
            spaces = int(math.log10(aa))
        digits = int(math.log10(row * col)) - spaces + 1
        tmpSpace = ""
        for k in range(digits):
            tmpSpace = tmpSpace + " "
        print(a[i][j], end=tmpSpace)
    print()

# """

xPoints = [math.floor(col / 2)]
yPoints = [math.floor(row / 2)]

if not row % 2:
    xPoints.append(xPoints[0] - 1)
if not col % 2:
    yPoints.append(yPoints[0] - 1)

midPoints = []

for i in range(len(xPoints)):
    for j in range(len(yPoints)):
        midPoints.append((xPoints[i], yPoints[j]))

for i in midPoints:
    print(a[i[0]][i[1]])