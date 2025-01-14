# Advent of Code 2024 Day 7 Part 1

import io
import itertools
import os


# Each line represents a single equation. The test value appears before the colon on each line; 
# it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.
# Operators are always evaluated left-to-right, not according to precedence rules. 
# Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see 
# elephants holding two different types of operators: add (+) and multiply (*).
# The engineers just need the total calibration result, which is the sum of the test values 
# from just the equations that could possibly be true. 
# Determine which equations could possibly be true. What is their total calibration result?

# 1. Read input file
# 2. For each line store result in one list and the operands into another list.
# 3. From operand list, determine total number of combinations. Create a set of these.
# 4. Try each set of operations until we either match the current result or reach the end of possible combinations.
# 5. If found, then add current result to tally.
      
# 1. Read input file
f = io.FileIO(os.path.realpath("07\\input.txt"), 'r')
retList = f.readlines() # readall?
f.close()
f = None

lResults:list=[] # list of result values, integers, ex: [32, 3333, 29292, 1]
lOperands:list=[] # space-separated list of operand lists, integers ex: [' 32 3333, 29292, 1', ' 32 3333 9292 1', ' 32 3333 29292 1']

# 1. Read input file
# 2. For each line store result in one list and the operands into another list.
i=0
while(i<retList.__len__()):
    # Example line: 3267: 81 40 27
    # Decode from byte to string; clean up line of ending chars.
    line=retList[i].decode()
    line=line.replace('\n','')
    line=line.replace('\r','')

    # Split on : to get the two parts.
    sp:list=line.split(':')
    lResults.append(int(sp[0]))
    lOperands.append(str(sp[1]))
  
    
    i+=1


sumCalibrationResult:int=0
i=0
while(i<lResults.__len__()):
    # Number of permutations is pool-count raised to the number of positions. 
    # So when there are 2 operations (pool-count) and 1 position, then 2^1 = 2
    #   2^2=4, 2^3=8...
    print(f'{i} of {lResults.__len__()}: {lResults[i]}')

    currentResult:int=lResults[i]
    currentOperands:list=lOperands[i].split()

    allowedOperations:str=["+*"]
    operandCount:int=2

    lOps:list=lOperands[i].split()
    positionCount=lOps.__len__() - 1

    # The Product function support permutations with repetition in a fixed length.
    #   The Permutation function does not support repetition in a fixed length.
    # 3. From operand list, determine the a set of permutations.
    lPermuations:list=[] # A list of all possible permutations to attempt.
    l:list=itertools.product('+*', repeat=positionCount)
    for x in l:
        lPermuations.append(x)
        #print(x)


    # 4. Try each set of operations until we either match the current result or reach the end of possible combinations.# Carry out each form
    j=0
    while(j<lPermuations.__len__()):  # Set of permutations.
        currentPermutation:list=lPermuations[j]
        k=0
        tmpSum=int(currentOperands[0])
        while(k<currentOperands.__len__()):
            if(k<currentOperands.__len__()-1):
                if(currentPermutation[k]=='+'):
                    tmpSum+=int(currentOperands[k+1])
                elif(currentPermutation[k]=='*'):
                    tmpSum*=int(currentOperands[k+1])
            else:
                pass
            
            k+=1

        # 5. If sum matches current result, then add current result to tally.
        if(tmpSum==lResults[i]):
            sumCalibrationResult+=tmpSum
            break

        j+=1

    i+=1

print(sumCalibrationResult)