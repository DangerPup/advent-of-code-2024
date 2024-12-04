# Advent of Code 2024 Day 3 Part 1

import io
import os
import re

# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

# 1. Read input file
# 2. For each line, find matching patterns.
# 3. "Execute" each matching pattern adding result to a total.


# 1. Read input file
f = io.FileIO(os.path.realpath("03\\input.txt"), 'r')
retList = f.readlines() # readall?
f.close()
f = None

# 2. For each line, find matching patterns.
i=0
sumOfAllMultiplications = 0
x=0
while(i<retList.__len__()):
    lMatches = []
    print(str(retList[i]))
    # The following regex matches on must be after mul( and before ); gives a list like this: ['123, 45', '89, 0']
    lMatches = re.findall(r'(?<=mul\()(?:\d{3}|\d{2}|\d{1}),(?:\d{3}|\d{2}|\d{1})(?=\))', str(retList[i]), )
    print(lMatches)

    # 3. "Execute" each matching pattern adding result to a total.
    j=0
    while(j<lMatches.__len__()): # ['123, 45', '89, 0']
        # split up the entry on the comma and multiple the operands.
        sumOfAllMultiplications+=int(lMatches[j].split(',')[0]) * int(lMatches[j].split(',')[1])
        j+=1
        x+=1
    i+=1

print(x)
print(sumOfAllMultiplications)