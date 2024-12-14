**Advent of Code 2024 Day 6**

Programming Language: Python

*Notes:*
- I had fun with puzzle 1, tracking the guard's movement with position and heading, marking each position reached and direction the guard was moving at the time ↑ ↓ → ←.

- I tried solving puzzle 1 with recursion, which worked for the example, however in Python I ran into a recursion-depth limit exception.

    _ `RecursionError: maximum recursion depth exceeded while calling a Python object` see aoc-2024-06-p1-RecursionException.py

    _ I ended up solving puzzle 1 with 'aoc-2024-06-p1.py' which has a solution which works iteratively.

 - Puzzle 2 initially had some performance problems, after reducing the number of nested while loops and storing some initial values up-front (so as to not need to recalculate them), the performance improved.

 - I solved Puzzle 2 by

    _ Running through the original map to identify the path.
 
    _ Copy the map and replace one position the guard was in with an obstacle to see if we encountered a loop. Repeat for each guard-occupied position from original run-through.
 
    _ To identify a loop, if the next position was already guard-occupied and is the same heading (n,s,e,w), then we're in a loop.
    
 - Learned about list deep copies.
 - [Learned about functions returning tuples as a means of implementing 'by reference'.](https://realpython.com/python-pass-by-reference/#contrasting-pass-by-reference-and-pass-by-value)

 - Have not successfully solved day 6 part 2, however checking in so I can move on to the other puzzles since I am already very far behind. Will need to come back to part 2 and re-work the solution.

*Puzzle answers for my puzzle input:*
1. 5409
2.