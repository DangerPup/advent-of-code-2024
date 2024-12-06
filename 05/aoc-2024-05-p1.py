# Advent of Code 2024 Day 5 Part 1

import math
import io
import os


# To get the printers going as soon as possible, start by identifying which updates are already in the right order.
# For some reason, the Elves also need to know the middle page number of each update being printed.

# 1. Read input file
# 2. Load rule portion of file into a list
# 3. Load updates portion of file into a list
# 4. First identify the correctly ordered updates by comparing page list to rules.
# 5. Next identify the middle page of each correctly ordered update and add to sum.

# Function: Returns true if the current index of the update string string passes all rules.
def DoesUpdatePassRules(lRules:list, update:list, updateCurrentIndex:int) -> bool:
    passesSw = False
    currPage = update[updateCurrentIndex]
    print(' Current page: ' + currPage, end=', ')

    # Check pages before
    if(updateCurrentIndex==0):
        passesSw=True
    else:
        j=updateCurrentIndex-1
        while(j>=0):
            pageBefore=update[j]
            print(" page before: " + pageBefore, end=', ')
            if((pageBefore + '|' + currPage) in lRules):
                passesSw=True
            else:
                passesSw=False
                break
            j-=1       
    # Check pages after
    if(updateCurrentIndex==update.__len__()):
        passesSw = True
    else:
        j=updateCurrentIndex+1
        while(j<update.__len__()):
            pageAfter=update[j]
            print("page after: " + pageAfter, end=', ')
            if((currPage + '|' + pageAfter) in lRules):
                passesSw=True
            else:
                passesSw=False
                break
            j+=1

    if(passesSw):
        print('passes')
    else:
        print('does not pass')

    return passesSw

# 1. Read input file
f = io.FileIO(os.path.realpath("05\\input.txt"), 'r')
retList = f.readlines() # readall?
f.close()
f = None

lRules=[] # list of rules, ex: ['32|86', '27|29', '15|32', '12|32']
lUpdate=[] # list of page updates, ex: ['12, 32, 15, 86, 27, 29', '12, 14, 15, 17, 18']

i=0
while(i<retList.__len__()):
    # Decode from byte to string; clean up line of ending chars.       
    line=retList[i].decode()
    line=line.replace('\n','')
    line=line.replace('\r','')
    if(line==''):
        pass
    elif("|" in str(line)):
        # 2. Load rule portion of file into a list
        lRules.append(line)
    else:
        # 3. Load updates portion of file into a list
        lUpdate.append(line)
    i+=1

# 4. First identify the correctly ordered updates by comparing page list to rules.
sumOfOrderedMiddlePageNumbers = 0
i=0
while(i<lUpdate.__len__()):
    j=0
    currUpdates=[]
    currUpdates=lUpdate[i].split(',')
    # Check each page in the current updates.
    updatesPassSw=False
    print(currUpdates.__str__())
    while(j<currUpdates.__len__()):
        updatesPassSw=DoesUpdatePassRules(lRules, currUpdates, j)
        if(not updatesPassSw):
            break
        j+=1
    if(updatesPassSw):
        # 5. Next identify the middle page of each correctly ordered update.
        middleIdx=math.ceil(currUpdates.__len__()/2)
        sumOfOrderedMiddlePageNumbers+=int(currUpdates[middleIdx-1])
    i+=1

print(sumOfOrderedMiddlePageNumbers)