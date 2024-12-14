# Advent of Code 2024 Day 6 Part 1

import io
import os


# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
# Include the guard's starting position.
# Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:
#   If there is something directly in front of you, turn right 90 degrees.
#   Otherwise, take a step forward.
# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

# 1. Read input file
# 2. Load map into a 2D array with characters indicating open space, obstacle, guard's position and heading.
#       open space = "."
#       obstascle = "#"
#       guard's position and heading = "<", "^", ">", "v"
# 3. Move guard until they leave the map
# 4. Count the distinct locations that the guard was in, independent of heading, only count a location once.


# Heading names and associated map characters.
headings:dict={'north': '^','east': '>','south': 'v','west': '<'}
# Guard direction names and associated map characters. How they moved through a space, for example north, east, turned-west...
#   alt-key 24-27
mapStep:dict={'north': '↑','east': '→','south': '↓','west': '←'}

# PrintMap
# Print the map to output window
# Accepts a 2D array.
def PrintMap(map:list):
    i=0
    while(i<map.__len__()):
        j=0
        while(j<map[i].__len__()):
            print(map[i][j], end=' ')
            j+=1
        print('\n\r')
        i+=1
        

# Move one step
# Accepts a map, current position and heading. (Current Position and Heading could be derived from map)
# Returns true if the guard is still on the map after moving 1 step, otherwise false.
# Map is updated with most recent guard location and guard in new location with possible new heading.
def MoveOneStep(map: list, currPos:list, currHeading: str) -> bool:
    
    leftTheMapSw=False

    # Calculate the next position based on the old position.
    nextX=-1
    nextY=-1
    if(currHeading==headings['north']):
        nextX=currPos[0]-1
        nextY= currPos[1]
    elif(currHeading==headings['east']):
        nextX=currPos[0]
        nextY= currPos[1]+1
    elif(currHeading==headings['south']):
        nextX=currPos[0]+1
        nextY= currPos[1]
    elif(currHeading==headings['west']):
        nextX=currPos[0]
        nextY= currPos[1]-1
      
    # Check whether next position leaves the board.
    if nextX<0 or nextY<0 or nextX>=map.__len__() or nextY>=map.__len__():
        # We have left the board.
        leftTheMapSw=True
    
    # If next position is still on the board, check for possibility of movement or obstacle.
    # Check whether new position is blocked by an obstacle.
    nextHeading=currHeading
    if(not leftTheMapSw):
        if map[nextX][nextY]=='#':
            # Obstacle, turn 'right' relative to current heading and re-calc next position. Think, we we're heading North but now need to head East due to obstacle.
            if(currHeading==headings['north']): 
                nextHeading=headings['east']
                nextX=currPos[0]
                nextY= currPos[1]+1
            elif(currHeading==headings['east']):
                nextHeading=headings['south']
                nextX=currPos[0]+1
                nextY= currPos[1]
            elif(currHeading==headings['south']):
                nextHeading=headings['west']
                nextX=currPos[0]
                nextY= currPos[1]-1
            elif(currHeading==headings['west']):
                nextHeading=headings['north']
                nextX=currPos[0]-1
                nextY= currPos[1]

    # Check whether next position leaves the board.
    if nextX<0 or nextY<0 or nextX>=map.__len__() or nextY>=map.__len__():
        # We have left the board.
        leftTheMapSw=True

    # Update the map: current position shows direction moved; re-position guard in next position.
    if(nextHeading==headings['north']):
        map[currPos[0]][currPos[1]]=mapStep['north']
        if(not leftTheMapSw):
            map[nextX][nextY]=headings['north']
    elif(nextHeading==headings['east']):
        map[currPos[0]][currPos[1]]=mapStep['east']
        if(not leftTheMapSw):
            map[nextX][nextY]=headings['east']
    elif(nextHeading==headings['west']):
         map[currPos[0]][currPos[1]]=mapStep['west']
         if(not leftTheMapSw):
            map[nextX][nextY]=headings['west']
    elif(nextHeading==headings['south']):
        map[currPos[0]][currPos[1]]=mapStep['south']
        if(not leftTheMapSw):
            map[nextX][nextY]=headings['south']

    # Print resulting map
    #print('__________________________________________________')
    #PrintMap(map)

    # True: on the map; False: off the map
    return (not leftTheMapSw)
     

# 1. Read input file
f = io.FileIO(os.path.realpath("06\\input.txt"), 'r')
retList = f.readlines() # readall?
f.close()
f = None

# A 2D array representing the area map
lMap=[]
# The guard's position, 0-based.
lCurrGuardPosition=[-1,-1]
# The guard's heading
sCurrGuarHeading='?'

# 2. Load map into a 2D array with characters indicating open space, obstacle, guard's position and heading.
i=0
while(i<retList.__len__()):
    # Decode from byte to string; clean up line of ending chars.       
    line=retList[i].decode()
    line=line.replace('\n','')
    line=line.replace('\r','')
    new=[]
    if(line==''):
        pass
    else:
        #new=list(line).copy()
        j=0
        while(j<line.__len__()):
            new.append(line[j])
            j+=1
        lMap.append(new)
    i+=1


# 3. Move guard until they leave the map
onTheMapSw = True
while(onTheMapSw):
    # Find the guard's current position and heading
    i=0
    while(i<lMap.__len__()):
        if(headings['north']  in lMap[i]):
            lCurrGuardPosition=[i,lMap[i].index(headings['north'])]
            sCurrGuarHeading = headings['north']
            break
        if(headings['east']  in lMap[i]):
            lCurrGuardPosition=[i,lMap[i].index(headings['east'])]
            sCurrGuarHeading = headings['east']
            break
        if(headings['south']  in lMap[i]):
            lCurrGuardPosition=[i,lMap[i].index(headings['south'])]
            sCurrGuarHeading = headings['south']
            break
        if(headings['west']  in lMap[i]):
            lCurrGuardPosition=[i,lMap[i].index(headings['west'])]
            sCurrGuarHeading = headings['west']
            break
        i+=1
    onTheMapSw=MoveOneStep(lMap, lCurrGuardPosition, sCurrGuarHeading)

# 4. Count the distinct locations that the guard was in, independent of heading, only count a location once.
countOfGuardMoves=0
i=0
while(i<lMap.__len__()):
    j=0
    while(j<lMap[i].__len__()):
        if(lMap[i][j] in mapStep.values()):
            countOfGuardMoves+=1
        j+=1
    
    i+=1

print(countOfGuardMoves)