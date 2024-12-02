# Advent of Code 2024 Day 1 Part 1

import io
import os

# The levels are either all increasing or all decreasing.
# Any two adjacent levels differ by at least one and at most three.

# Objective: How many reports are safe?

# 1. Read input file
# 2. For each report analyze movement of levels.
# 3. Sum all that are Safe

def isRecordSafe(lLevels: list) -> bool:
    #   1. Levels are either ascending or descending, and
    #   2. Any adjacent levels are different by 1 to 3 inclusive.
    test1Sw = False
    test2Sw = False
    lLevelsAsc = sorted(lLevels, reverse=False)
    if(lLevels==lLevelsAsc):
        test1Sw = True
    else:
        lLevelsDsc = sorted(lLevels, reverse=True)
        if(lLevels==lLevelsDsc):
            test1Sw = True
        else:
            test1Sw = False

    if(test1Sw):
        i=1
        while(i<lLevels.__len__()):
            if(abs(lLevels[i] - lLevels[i-1])>=1 and abs(lLevels[i] - lLevels[i-1])<=3):
                test2Sw = True
            else:
                test2Sw = False
                break
            i+=1

    # Debugging: print those that failed test 1.
    #if(test1Sw==False):
    #    print(lLevels)
    
    # Record is safe when all tests are true.
    if(test1Sw and test2Sw):
        print(lLevels)

    return (test1Sw and test2Sw)

# 1. read file and fill 2 lists from each line part
f = io.FileIO(os.path.realpath("02\\input.txt"), 'r')
retList = f.readlines()
f.close()
f = None

countOfSafeRecords = 0
i=0
while (i<retList.__len__()):
    # Split the record.
    blLevels = retList[i].split(None, -1)

    # Convert to integers for better sorting and comparisons. Binary gave results that didn't work for this.
    j=0
    lLevels=[]
    while(j<blLevels.__len__()):
        lLevels.append(int(blLevels[j]))
        j+=1

    # Loop through each level, comparing current level to prior level.
    # Two things to check:
    #   1. Levels are either ascending or descending, and
    #   2. Absolute difference between first and list level are within allowed range.
    #       Allowed range is between abs(1 * number-of-level-changes) and abs(3 * number-of-level-changes), inclusive.
    #       number-of-level-changes is equal to (number of levels - 1)
    if(isRecordSafe(lLevels)==True):
        countOfSafeRecords+=1

    i+=1

print(countOfSafeRecords)