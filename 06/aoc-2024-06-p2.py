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

def PrintMapToFile(file_path, map:list):
    """
    Write the given content to a file.

    :param file_path: Path of the file to write to
    :param content: Content to write to the file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            i=0
            while(i<map.__len__()):
                j=0
                while(j<map[i].__len__()):
                    if(str(map[i][j])=='.'):
                        file.write('░')
                    elif(str(map[i][j])=='↑'):
                        file.write('▓')
                    elif(str(map[i][j])=='↓'):
                        file.write('▓')
                    elif(str(map[i][j])=='→'):
                        file.write('▓')
                    elif(str(map[i][j])=='←'):
                        file.write('▓')
                    else:
                        file.write(str(map[i][j]))
                    j+=1
                file.write('\n')
                i+=1
    except Exception as e:
        print(f"An error occurred: {e}")

def PrintMapToFileAsHtml(file_path, map:list, loopPositions:list):
    """
    Write the given content to a file.

    :param file_path: Path of the file to write to
    :param content: Content to write to the file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('<style>.loop-path{background-color:aqua} .new-obstacle{background-color:pink} .obstacle{background-color:gray} .guard-position{background-color:green}</style>')
            file.write('<table>')
            i=0
            while(i<map.__len__()):
                file.write('<tr>')
                j=0
                while(j<map[i].__len__()):
                    if([i,j] in loopPositions):
                        file.write('<td class="loop-path">')
                    else:
                        file.write('<td>')
                        
                    if(str(map[i][j])=='.'):
                        file.write(str(map[i][j]))
                    elif(str(map[i][j])=='↑'):
                        file.write(str(map[i][j]))
                    elif(str(map[i][j])=='↓'):
                        file.write(str(map[i][j]))
                    elif(str(map[i][j])=='→'):
                        file.write(str(map[i][j]))
                    elif(str(map[i][j])=='←'):
                        file.write(str(map[i][j]))
                    elif(str(map[i][j])=='#'):
                        file.write('<span class="obstacle">')
                        file.write(str(map[i][j]))
                        file.write('</span')
                    elif(str(map[i][j])=='@'):
                        file.write('<span class="new-obstacle">')
                        file.write(str(map[i][j]))
                        file.write('</span')
                    elif(str(map[i][j])=='<' or str(map[i][j])=='^' or str(map[i][j])=='>' or str(map[i][j])=='v'):
                        file.write('<span class="guard-position">')
                        file.write(str(map[i][j]))
                        file.write('</span')
                    else:
                        file.write(str(map[i][j]))
                    file.write('</td>')
                    j+=1
                file.write('</tr>')
                i+=1
            file.write('</table>')
    except Exception as e:
        print(f"An error occurred: {e}")

# Move one step
# Accepts a map, current position and heading. (Current Position and Heading could be derived from map)
# Returns true if the guard is still on the map after moving 1 step, otherwise false.
# Returns a tuple
#   bool, true if the guard is still on the map after moving 1 step, otherwise false.
#   list, length 2 of the new x and new y position
#   str, new heading
# Map is updated with most recent guard location and guard in new location with possible new heading.
def MoveOneStep(map: list, currPos:list, currHeading: str) -> tuple:
    
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
        if map[nextX][nextY]in ['#', '@']:
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
        if map[nextX][nextY] in ['#', '@']:
            # Obstacle, turn 'right' relative to current heading and re-calc next position. Think, we we're heading North but now need to head East due to obstacle.
            if(nextHeading==headings['north']): 
                nextHeading=headings['east']
                nextX=currPos[0]
                nextY= currPos[1]+1
            elif(nextHeading==headings['east']):
                nextHeading=headings['south']
                nextX=currPos[0]+1
                nextY= currPos[1]
            elif(nextHeading==headings['south']):
                nextHeading=headings['west']
                nextX=currPos[0]
                nextY= currPos[1]-1
            elif(nextHeading==headings['west']):
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
    return (not leftTheMapSw), [nextX, nextY], nextHeading
     
# Peek at the position the guard would move to next. Honors obstacles, in other words if there is an obstacle ahead, returns the character in position to the right.
# Accepts a map, a guard's current position and heading.
# Returns a tuple of positionChar and nextHeading, if will be off the map then returns '', .
def LookAhead(map: list, currPos:list, currHeading: str)-> tuple:
    positionChar=''
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
        if map[nextX][nextY] in ['#', '@']:
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
        if map[nextX][nextY] in ['#', '@']:
            # Obstacle, turn 'right' relative to current heading and re-calc next position. Think, we we're heading North but now need to head East due to obstacle.
            if(nextHeading==headings['north']):
                nextHeading=headings['east']
                nextX=currPos[0]
                nextY= currPos[1]+1
            elif(nextHeading==headings['east']):
                nextHeading=headings['south']
                nextX=currPos[0]+1
                nextY= currPos[1]
            elif(nextHeading==headings['south']):
                nextHeading=headings['west']
                nextX=currPos[0]
                nextY= currPos[1]-1
            elif(nextHeading==headings['west']):
                nextHeading=headings['north']
                nextX=currPos[0]-1
                nextY= currPos[1]
        positionChar=map[nextX][nextY]
    else:
        # Left the map
        positionChar=''

    return positionChar, nextHeading

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

# Save a copy of the original map before any guards traipse through it.
lOrigMap=copy.deepcopy(lMap)

# 3. With the original map, move guard until they leave the map; after this we will know their path.
onTheMapSw = True
lUniquePositions:list=[] # [(x,y)]
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

# Save the guard's staring position and heading
lStartGuardPosition:list=lCurrGuardPosition
sStartGuarHeading:str=sCurrGuarHeading

while(onTheMapSw):
    onTheMapSw,lCurrGuardPosition,sCurrGuarHeading=MoveOneStep(lMap, lCurrGuardPosition, sCurrGuarHeading)
    if(onTheMapSw):
        lUniquePositions.append(lCurrGuardPosition.copy())

# Remove the guard's starting position as an option for a new obstacle.
if(lStartGuardPosition in lUniquePositions):
    lUniquePositions.remove(lStartGuardPosition)

# # Find the guard's start/current position and heading
# j=0
# while(j<lOrigMap.__len__()):
#     if(headings['north']  in lOrigMap[j]):
#         lStartGuardPosition=[j,lOrigMap[j].index(headings['north'])]
#         sStartGuarHeading = headings['north']
#         break
#     if(headings['east']  in lOrigMap[j]):
#         lStartGuardPosition=[j,lOrigMap[j].index(headings['east'])]
#         sStartGuarHeading = headings['east']
#         break
#     if(headings['south']  in lOrigMap[j]):
#         lStartGuardPosition=[j,lOrigMap[j].index(headings['south'])]
#         sStartGuarHeading = headings['south']
#         break
#     if(headings['west']  in lOrigMap[j]):
#         lStartGuardPosition=[j,lOrigMap[j].index(headings['west'])]
#         sStartGuarHeading = headings['west']
#         break
#     j+=1

# 4. Gather a list of unique positions on the guard's path
# lUniquePositions:list=[] # [(x,y)]
# i=0
# while(i<lMap.__len__()):
#     j=0
#     while(j<lMap[i].__len__()):
#         if(lMap[i][j] in mapStep.values()):
#             # Skip guard's starting position.
#             if([i,j]==lStartGuardPosition):
#                 pass
#             else:
#                 lUniquePositions.append([i,j])
#         j+=1
#     i+=1

# 5. Starting with the first known path position, replace it with an obstacle.
# we're working with a copy of the map.
countOfLoopCausingPositions=0
i=0
i=46
while(i<lUniquePositions.__len__()):

    # Insert an obstacle into a copy of the map
    lMapCopy:list=copy.deepcopy(lOrigMap)
    lMapCopy[lUniquePositions[i][0]][lUniquePositions[i][1]]='@'
    
    # Rest start position.
    lCurrGuardPosition = lStartGuardPosition.copy()
    sCurrGuarHeading = sStartGuarHeading

    # Move guard until they leave the map or a loop is detected.
    guardLeftMapOrIsInLoop:bool=False
    while(not guardLeftMapOrIsInLoop):
        # Check if next position contains a directional arrow matching the direction the guard is moving in.
        lookAheadChar=''
        newGuardHeading=''
        lookAheadChar,newGuardHeading=LookAhead(lMapCopy, lCurrGuardPosition, sCurrGuarHeading)
        if(sCurrGuarHeading!=newGuardHeading):
            # Loop detection really only occurs at a turn. Is guard forced to turn and have they already been in the next position facing the same way?
            if ((newGuardHeading==headings['north'] and lookAheadChar==mapStep['north']) or
                (newGuardHeading==headings['east']  and lookAheadChar==mapStep['east']) or 
                (newGuardHeading==headings['south'] and lookAheadChar==mapStep['south']) or 
                (newGuardHeading==headings['west']  and lookAheadChar==mapStep['west']) or
                (newGuardHeading==headings['north'] and lookAheadChar==mapStep['south']) or # 180 degree turn
                (newGuardHeading==headings['east']  and lookAheadChar==mapStep['west']) or 
                (newGuardHeading==headings['south'] and lookAheadChar==mapStep['north']) or 
                (newGuardHeading==headings['west']  and lookAheadChar==mapStep['east'])): # a directional arrow.
                guardLeftMapOrIsInLoop=True
                countOfLoopCausingPositions+=1
                print(f'found, i={i}, unique pos={lUniquePositions[i]}')
                print(f'    current heading={sCurrGuarHeading}, current guard pos={lCurrGuardPosition}, current guard heading={sCurrGuarHeading}')

                # Walk through the loop once, so we can highlight it.
                lLoopPositions:list=[]
                lLoopStartPosition:list=lCurrGuardPosition.copy()
                lLoopPositions.append(lCurrGuardPosition)
                continueLoopSw=True
                while(continueLoopSw):
                   moveOneStepSw, lCurrGuardPosition, sCurrGuarHeading = MoveOneStep(lMapCopy, lCurrGuardPosition, sCurrGuarHeading)        
                   lLoopPositions.append(lCurrGuardPosition)
                   if(lCurrGuardPosition==lLoopStartPosition):
                       continueLoopSw=False
                   if(moveOneStepSw==False):
                      continueLoopSw=False
                #PrintMap(lMapCopy)
                #PrintMapToFile(f'06\debug\{i}.txt', lMapCopy)
                #PrintMapToFileAsHtml(f'06\debug\{i}.htm', lMapCopy, lLoopPositions)
            elif lookAheadChar=='': # no next char since guard will leave the map.
                guardLeftMapOrIsInLoop=True
            
        if(not guardLeftMapOrIsInLoop):
            moveOneStepSw=False
            moveOneStepSw, lCurrGuardPosition, sCurrGuarHeading = MoveOneStep(lMapCopy, lCurrGuardPosition, sCurrGuarHeading)
            if moveOneStepSw:
                pass
            else:
                # Guard is off the map. This obstacle does NOT produce a loop.
                # Move on to the next obstacle position.
                guardLeftMapOrIsInLoop=True
    i+=1


print(countOfLoopCausingPositions)

