# Advent of Code 2024 Day 5 Part 2

import math
import io
import os

# For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order.
# Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

# 1. Read input file
# 2. Load rule portion of file into a list
# 3. Load updates portion of file into a list
# 4. First identify the incorrectly ordered updates by comparing page list to rules.
# 5. Next re-order the incorrectly ordered update to abide by the rules.
# 6. Then identify the middle page of each re-ordered (originally incorrectly ordered) update and add to sum.

# example answer 123
# answer 6370

# Function: Returns true if the current index of the update string string passes all rules.
def DoesUpdatePassRules(lRules:list, update:list) -> bool:
    countDoesNotPass = 0

    i=0
    while(i<update.__len__()):
        currPage = update[i]
        #print(' Current page: ' + currPage, end=', ')

        # Check pages before
        if(i==0):
            pass
        else:
            j=i-1
            while(j>=0):
                pageBefore=update[j]
                #print("page before: " + pageBefore, end=', ')
                if((pageBefore + '|' + currPage) in lRules):
                    #print("==", end=', ')
                    pass
                else:
                    #print(">>", end=', ')
                    countDoesNotPass+=1
                j-=1       
        # Check pages after
        if(i==update.__len__()):
            pass
        else:
            j=i+1
            while(j<update.__len__()):
                pageAfter=update[j]
                #print("page after: " + pageAfter, end=', ')
                if((currPage + '|' + pageAfter) in lRules):
                    #print("==", end=', ')
                    pass
                else:
                    #print("<<", end=', ')
                    countDoesNotPass+=1
                j+=1

        if(countDoesNotPass==0):
            #print('passes')
            pass
        else:
            #print('does not pass')
            pass

        i+=1
            
    return (countDoesNotPass==0)

# Given rules and list with bad ordering, moves one page to abide by rules.
def FixOnePage(lRules:list, update:list) -> list:
    print(update.__str__())
    lNewUpdate=update.copy()


    i=0
    while(i<update.__len__()):
        currPage = update[i]

        # Check pages before
        if(i==0):
            pass
        else:
            j=i-1
            while(j>=0):
                pageBefore=update[j]
                if((pageBefore + '|' + currPage) in lRules):
                    pass
                else:
                    # Shift right 1.
                    tmp=lNewUpdate[j+1]
                    lNewUpdate[j+1]=lNewUpdate[j]
                    lNewUpdate[j]=tmp
                    print(lNewUpdate)
                    lNewUpdate = FixOnePage(lRules, lNewUpdate)
                    break
                j-=1

        # Check pages after
        if(i==update.__len__()):
            pass
        else:
            j=i+1
            while(j<update.__len__()):
                pageAfter=update[j]
                if((currPage + '|' + pageAfter) in lRules):
                    pass
                else:
                    # Shift left 1.
                    tmp=lNewUpdate[j-1]
                    lNewUpdate[j-1]=lNewUpdate[j]
                    lNewUpdate[j]=tmp
                    print(lNewUpdate)
                    lNewUpdate = FixOnePage(lRules, lNewUpdate)
                    break
                j+=1

        if(DoesUpdatePassRules(lRules, lNewUpdate)):
            print("pass")
            break

        i+=1    
    return lNewUpdate
               
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

# 4. First identify the incorrectly ordered updates by comparing page list to rules.
sumOfOrderedMiddlePageNumbers = 0
i=0
while(i<lUpdate.__len__()):
    currUpdates=[]
    currUpdates=lUpdate[i].split(',')
    # Check each page in the current updates.
    countDoesNotPass=0
    #print(currUpdates.__str__())
    if(DoesUpdatePassRules(lRules, currUpdates)):
        pass
    else:
        countDoesNotPass+=1

    if(countDoesNotPass!=0):
        # 5. Next re-order the incorrectly ordered update to abide by the rules.
        new=[]
        new=FixOnePage(lRules, currUpdates)
        print("new updates: " + new.__str__())
        # 6. Then identify the middle page of each re-ordered (originally incorrectly ordered) update and add to sum.
        middleIdx=math.ceil(new.__len__()/2)
        sumOfOrderedMiddlePageNumbers+=int(new[middleIdx-1])

    i+=1

print(sumOfOrderedMiddlePageNumbers)