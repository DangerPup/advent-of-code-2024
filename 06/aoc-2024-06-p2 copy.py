# Advent of Code 2024 Day 6 Part 2
import copy
import io
import os


# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
# Include the guard's starting position.
# Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:
# I f there is something directly in front of you, turn right 90 degrees.
#   Otherwise, take a step forward.
#   You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?

# 1. Read input file
# 2. Load map into a 2D array with characters indicating open space, obstacle, guard's position and heading.
#       open space = "."
#       obstascle = "#"
#       guard's position and heading = "<", "^", ">", "v"
# 3. With the original map, move guard until they leave the map; after this we will know their path.
# 4. Gather a list of unique positions that are their path.
# 5. Starting with the first known path position, replace it with an obstacle.
# 6. Test whether the new map with new obstacle placement, does the guard still leave the map or do they get stuck in a loop?


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
        # Check again since there could be an obstacle ahead of us AFTER we turned right.
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
     
# Peek at the guard's next position and return whether it's an obstacle or not.
# Accepts tracked obstacle position, guard's current position and heading.
# Returns True if the guard would encounter the tracked obstacle in next move, other false.
def PeekNextPositionIsTrackedObstacle(map: list, currPos:list, currHeading: str, trackObstaclePos:list)-> bool:
    
    nextPosIsTrackedObstacle=False

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
        nextPosIsTrackedObstacle=False
    elif(map[nextX][nextY]=='#' and nextX==trackObstaclePos[0] and nextY==trackObstaclePos[1]):
        nextPosIsTrackedObstacle=True 

    return nextPosIsTrackedObstacle

# 1. Read input file
f = io.FileIO(os.path.realpath("06\\input.txt"), 'r')
retList = f.readlines() # readall?
f.close()
f = None

# A 2D array representing the area map
lMap:list=[]
# Original map with guard at starting point.
lOrigMap:list=[]
# The guard's position, 0-based.
lCurrGuardPosition:list=[-1,-1]
# The guard's heading
sCurrGuarHeading:str='?'

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

lOrigMap=copy.deepcopy(lMap)

# 3. With the original map, move guard until they leave the map; after this we will know their path.
onTheMapSw = True
while(onTheMapSw):
    # Find the guard's start/current position and heading
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

# 4. Gather a list of unique positions that are their path and a corresponding list to track number of times the guard met the obstacle (and had to turn.)
#       This can help us identify a loop, for example, the guard has encountered the obstacle 3 times.
lUniquePositions:list=[] # [(x,y)]
#       Count one position for each heading, since we might encounter obstacle from different directions.
lObstacleTouchCount:dict={} # (xyh, hitcount)
i=0
while(i<lMap.__len__()):
    j=0
    while(j<lMap[i].__len__()):
        if(lMap[i][j] in mapStep.values()):
            lUniquePositions.append([i,j])
            lObstacleTouchCount[str(i) + str(j) + headings['north']] = 0
            lObstacleTouchCount[str(i) + str(j) + headings['east']] = 0
            lObstacleTouchCount[str(i) + str(j) + headings['south']] = 0
            lObstacleTouchCount[str(i) + str(j) + headings['west']] = 0
        j+=1
    i+=1

countOfLoopCausingPositions=0
# 5. Starting with the first known path position, replace it with an obstacle.
# we're working with a copy of the map.
i=0
while(i<lUniquePositions.__len__()):
    guardLeftMapOrIsInLoop:bool=False
    lMapCopy:list=copy.deepcopy(lOrigMap)

    # Insert an obstacle into a copy of the map
    lMapCopy[lUniquePositions[i][0]][lUniquePositions[i][1]]='#'

    while(not guardLeftMapOrIsInLoop):
         # Find the guard's start/current position and heading
        j=0
        while(j<lMapCopy.__len__()):
            if(headings['north']  in lMapCopy[j]):
                lCurrGuardPosition=[j,lMapCopy[j].index(headings['north'])]
                sCurrGuarHeading = headings['north']
                break
            if(headings['east']  in lMapCopy[j]):
                lCurrGuardPosition=[j,lMapCopy[j].index(headings['east'])]
                sCurrGuarHeading = headings['east']
                break
            if(headings['south']  in lMapCopy[j]):
                lCurrGuardPosition=[j,lMapCopy[j].index(headings['south'])]
                sCurrGuarHeading = headings['south']
                break
            if(headings['west']  in lMapCopy[j]):
                lCurrGuardPosition=[j,lMapCopy[j].index(headings['west'])]
                sCurrGuarHeading = headings['west']
                break
            j+=1

        if PeekNextPositionIsTrackedObstacle(lMapCopy, lCurrGuardPosition, sCurrGuarHeading, lUniquePositions[i]):
            # Increment the count of times guard has encountered this obstacle.
            lObstacleTouchCount[str(lUniquePositions[i][0]) + str(lUniquePositions[i][1]) + sCurrGuarHeading]+=1
            # If at 3, then this is a loop, save and move on to the next obstacle position.
            if lObstacleTouchCount[str(lUniquePositions[i][0]) + str(lUniquePositions[i][1]) + sCurrGuarHeading]>=3:
                countOfLoopCausingPositions+=1
                guardLeftMapOrIsInLoop=True

        if(not guardLeftMapOrIsInLoop):
            if MoveOneStep(lMapCopy, lCurrGuardPosition, sCurrGuarHeading):
                pass
            else:
                # Guard is off the map. This obstacle does NOT produce a loop.
                # Move on to the next obstacle position.
                guardLeftMapOrIsInLoop=True
    i+=1


print(countOfLoopCausingPositions)
