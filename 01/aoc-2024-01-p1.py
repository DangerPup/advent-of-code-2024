# Advent of Code 2024 Day 1 Part 1

import io
import os

# 1. read file and fill 2 lists from each line part
# 2. sort each list
# 3. return sum of absolute difference of each number at every list position


# 1. read file and fill 2 lists from each line part
f = io.FileIO(os.path.realpath("01\\input.txt"), 'r')
retList = f.readlines()
f.close()
f = None

lLeft = []
lRight = []
i=0
while (i<retList.__len__()):
    # convert to integers while we're here.
    lLeft.append(int(retList[i].split(None, -1)[0]))
    lRight.append(int(retList[i].split(None, -1)[1]))
    i+=1


# 2. sort each list
lLeft.sort()
lRight.sort()

# 3. return sum of absolute difference of each number at every list position
i=0
sumOfDiffs = 0
while (i<lLeft.__len__()):
    sumOfDiffs += abs(lLeft[i] - lRight[i])
    i+=1

print(sumOfDiffs)