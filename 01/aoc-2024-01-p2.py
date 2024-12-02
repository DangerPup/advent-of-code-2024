# Advent of Code 2024 Day 1 Part 1

## This time, you'll need to figure out exactly how often each number from the 
## left list appears in the right list. Calculate a total similarity score by adding 
## up each number in the left list after multiplying it by the number of times that 
## number appears in the right list.

import io
import os

# 1. read file and fill 2 lists from each line part.
# 2. for each number in left list get number of occurences in right list.
# 3. sum the result of multiplying number by number of occurences.

def countOccurences(inList, match):
    i=0
    ret=0
    while(i<inList.__len__()):
        # I know inList is sort ascending, so let's speed this searchup.
        # We can exit the loop once we have counted all matching entries or once we encounter a number greater than match.
        if(inList[i]>match):
            exit
        else:            
            if(inList[i]==match):
                ret+=1
        i+=1
    return ret

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

# Sort each list to speed up comparisons.
lLeft.sort()
lRight.sort()

# 2. for each number in left list get number of occurences in right list.
i=0
similarityScore=0
while (i<lLeft.__len__()):
    numberOfOccurences = countOccurences(lRight, lLeft[i])
    # 3. sum the result of multiplying number by number of occurences.
    similarityScore += lLeft[i] * numberOfOccurences
    i+=1

print(similarityScore)