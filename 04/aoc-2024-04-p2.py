# Advent of Code 2024 Day 4 Part 2

import io
import os
import re

# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. 
# It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them.
# How many times does an X-MAS appear?

# 1. Read input file
# 2. Load into a 2-D array where each position contains a single character.
# 3. Find A, then spread out from there in NW, NE, SE and SW. There are 4 variations of an "X":
#   M_S
#   _A_
#   M_S

#   S_M
#   _A_
#   S_M

#   M_M
#   _A_
#   S_S

#   S_S
#   _A_
#   M_M


# 1. Read input file
f = io.FileIO(os.path.realpath("04\\input.txt"), 'r')
retList = f.readlines() # readall?
f.close()
f = None

# 2. Load into a 2-D array where each position contains a single character.
twoD=[]
i=0
while(i<retList.__len__()):
    # Decode from byte to string; clean up line of ending chars.
    line=retList[i].decode()
    line=line.replace('\n','')
    line=line.replace('\r','')
    j=0
    newRow=[]
    while(j<line.__len__()):
        newRow.append(line[j])
        j+=1
    twoD.append(newRow)

    i+=1

# 3. Find X, then spread out from there in each direction.
#   Use compass nomenclature (NW, NE, SE and SW)
#   Start in top left corner (0,0).
countOfXmas = 0
x=0
while(x<twoD.__len__()):
    y=0
    while(y<twoD[x].__len__()):
        # Find an A then check all positions in relation.
        if(twoD[x][y].upper()=="A"):

            if(x>=1 and y<twoD[x].__len__()-1 and y>=1 and x<twoD[x].__len__()-1):
                # Compare NE + SW, then NW + SE.
                # NE is (x-1 y+1) and SW is (x+1, y-1), NW is (x-1, y-1) and SE is (x+1, y+1).

                #   M_M
                #   _A_
                #   S_S
                if(twoD[x-1][y+1].upper()=="M" and twoD[x+1][y-1].upper()=="S"):
                    if(twoD[x-1][y-1].upper()=="M" and twoD[x+1][y+1].upper()=="S"):
                        countOfXmas+=1
                
                #   S_S
                #   _A_
                #   M_M
                if(twoD[x-1][y+1].upper()=="S" and twoD[x+1][y-1].upper()=="M"):
                    if(twoD[x-1][y-1].upper()=="S" and twoD[x+1][y+1].upper()=="M"):
                        countOfXmas+=1

                #   M_S
                #   _A_
                #   M_S
                if(twoD[x-1][y+1].upper()=="S" and twoD[x+1][y-1].upper()=="M"):
                    if(twoD[x-1][y-1].upper()=="M" and twoD[x+1][y+1].upper()=="S"):
                        countOfXmas+=1

                #   S_M
                #   _A_
                #   S_M
                if(twoD[x-1][y+1].upper()=="M" and twoD[x+1][y-1].upper()=="S"):
                    if(twoD[x-1][y-1].upper()=="S" and twoD[x+1][y+1].upper()=="M"):
                        countOfXmas+=1
        y+=1
    x+=1

print(countOfXmas)