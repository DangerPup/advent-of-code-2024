# Advent of Code 2024 Day 3 Part 2

import io
import os
import re

# There are two new instructions you'll need to handle:
#   The do() instruction enables future mul instructions.
#   The don't() instruction disables future mul instructions.
#   Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.
# Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?

# 1. Read input file
# 2. For each line, find matching patterns.
# 3. "Execute" each matching pattern adding result to a total while honoring dos and donts.


# 1. Read input file
f = io.FileIO(os.path.realpath("03\\input.txt"), 'r')
retList = f.readlines() # readall?
f.close()
f = None

# 2. For each line, find matching patterns.
i=0
sumOfAllMultiplications = 0
sumOfAllMultiplications2 = 0
do = True # At the beginning of the program, mul instructions are enabled.
while(i<retList.__len__()):
    lMatches = []
    #print(str(retList[i]))
    # The following regex matches on must be after mul( and before ); gives a list like this: ['123, 45', 'do()', '89, 0', '8, 93', 'don't()', '115, 34']
    lMatches = re.findall(r"(?:don't\(\)|do\(\)|(?<=mul\()(?:\d{3}|\d{2}|\d{1}),(?:\d{3}|\d{2}|\d{1})(?=\)))", str(retList[i]),)
    #print(lMatches)

    # 3. "Execute" each matching pattern adding result to a total while honoring dos and donts.
    # j=0
    # while(j<lMatches.__len__()): # ['123, 45', 'do()', '89, 0', '8, 93', 'don't()', '115, 34']
    #     if(lMatches[j]=="don't()"):
    #         do = False
    #     elif(lMatches[j]=="do()"):
    #         do = True
    #     else:
    #         # split up the entry on the comma and multiple the operands.
    #         if(do):
    #             sumOfAllMultiplications+=int(lMatches[j].split(',')[0]) * int(lMatches[j].split(',')[1])
    #             #print(lMatches[j])
    #         #else:
    #             #print(lMatches[j])
    #     j+=1

    # another way using re.finditer
    for mtch in re.finditer(r"(?:don't\(\)|do\(\)|(?<=mul\()(?:\d{3}|\d{2}|\d{1}),(?:\d{3}|\d{2}|\d{1})(?=\)))", str(retList[i]),):
        if(mtch.group(0)=="don't()"):
            do = False
        elif(mtch.group(0)=="do()"):
            do = True
        else:
            # split up the entry on the comma and multiple the operands.
            if(do):
                sumOfAllMultiplications2+=int(mtch.group(0).split(',')[0]) * int(mtch.group(0).split(',')[1])

    i+=1

print(sumOfAllMultiplications)
print(sumOfAllMultiplications2)