# Advent of Code 2024 Day 4 Part 1

import io
import os
import re

# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. 
# It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them.
# How many times does XMAS appear?

# 1. Read input file
# 2. Load into a 2-D array where each position contains a single character.
# 3. Find X, then spread out from there in each direction (?)


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

# 3. Find X, then spread out from there in each direction (?)
# Use compass nomenclature (N, E, S, SW, etc)
# Start in top left corner.
countOfXmas = 0
x=0
while(x<twoD.__len__()):
    y=0
    while(y<twoD[x].__len__()):
        # Find an X then check all positions in relation.
        if(twoD[x][y].upper()=="X"):
            # North
            if(x>=3):
                if(twoD[x-1][y].upper()=="M" and twoD[x-2][y].upper()=="A" and twoD[x-3][y].upper()=="S"):
                    countOfXmas+=1

            # South
            if(x<twoD.__len__()-3):
                if(twoD[x+1][y].upper()=="M" and twoD[x+2][y].upper()=="A" and twoD[x+3][y].upper()=="S"):
                    countOfXmas+=1

            # East
            if(y<twoD[x].__len__()-3):
                if(twoD[x][y+1].upper()=="M" and twoD[x][y+2].upper()=="A" and twoD[x][y+3].upper()=="S"):
                    countOfXmas+=1

            # West
            if(y>=3):
                if(twoD[x][y-1].upper()=="M" and twoD[x][y-2].upper()=="A" and twoD[x][y-3].upper()=="S"):
                    countOfXmas+=1

            # NE
            if(x>=3 and y<twoD[x].__len__()-3):
                if(twoD[x-1][y+1].upper()=="M" and twoD[x-2][y+2].upper()=="A" and twoD[x-3][y+3].upper()=="S"):
                    countOfXmas+=1

            # SE
            if(x<twoD[x].__len__()-3 and y<twoD[x].__len__()-3):
                if(twoD[x+1][y+1].upper()=="M" and twoD[x+2][y+2].upper()=="A" and twoD[x+3][y+3].upper()=="S"):
                    countOfXmas+=1

            # SW
            if(x<twoD[x].__len__()-3 and y>=3):
                if(twoD[x+1][y-1].upper()=="M" and twoD[x+2][y-2].upper()=="A" and twoD[x+3][y-3].upper()=="S"):
                    countOfXmas+=1

            # NW
            if(x>=3 and y>=3):
                if(twoD[x-1][y-1].upper()=="M" and twoD[x-2][y-2].upper()=="A" and twoD[x-3][y-3].upper()=="S"):
                    countOfXmas+=1

        y+=1
    x+=1

print(countOfXmas)