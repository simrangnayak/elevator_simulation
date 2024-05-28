# Elevator Code in Python

# Problem:

This code attempts to solve the problem where a building has one or two elevators servicing the floors of a building. Inputs can be adjusted in `./one_elevator_run.py` and `./two_elevator_run.py`. The program creates an output of each step the elevator(s) take to visit all passengers and deliver them to their destination. The code also raises an error when the floors entered are out of the building's range.


# Default Inputs:

`floors = {1:[0], 4:[6], 5:[3,2,7], 2:[1,6]}` - A dictionary identifying all floors elevator(s) must visit. Keys represent floors passengers are on while its values represent floors passengers want to go to.

Default position of elevator for one elevator problem:
`ev_floor = 3`

Default position of elevators for two elevator problem:
`ev_floor_1 = 3`
`ev_floor_2 = 6`

`min_floor = 0` - Minimum floor of the building.

`max_floor = 10` - Maximum floor of the building.


# Underlying Concept:

This process prioritizes no starvation. While this code may not output the most efficient outcome, it ensures that every passenger gets seen at some point. This follows from the assumption that an elevator will continue going in a direction until all the floors in that direction are visited. The top comment on this [post](https://softwareengineering.stackexchange.com/questions/331692/what-algorithm-is-used-by-elevators-to-find-the-shortest-path-to-travel-floor-or) provided this idea!

The two elevator problem calls the one elevator problem for every subset of the set of passenger tuples. For example, if the floors are `{5:[2,7], 1:[5]}`, there are 3 passenger tuples: `(5,2) (5,7) (1,5)`. I used this [page](https://blog.enterprisedna.co/how-to-generate-all-combinations-of-a-list-in-python/) to help me form a custom combination function to find all $2^n$ subsets, where `n` = number of passenger tuples (not sure why I didn't just use combinations from itertools...). This runs the one elevator problem $2^{n+1}$ times as one elevator may require fewer steps depending on its initial floor position.

The program then selects the divsion of passenger tuples per elevator based on the least number of total steps taken by both elevators. If there are multiple division of passenger tuples that take the minimum number of total steps, the code selects the first division.

I've noticed on repeated trials that when it is more efficient to use two elevators over one, the optimal division of passenger tuples involves each elevator "choosing" a direction to go into. I think this is a result of how I've coded the policy of no starvation: with an elevator staying in one direction until it completes all floors in its path.

I'm sure this would change in a dynamic elevator system (i.e. not all floors are pressed at the same time) but I wonder if this result could help reduce the time and space complexity as when `n` increases, the number of total combinations increases exponentially. This would also help the general n-elevator system (see below). The only problem left then would be to figure the point at which it is more efficient to just use one elevator.


# Further Exploration:

I initially started this problem looking at the n-elevator system and quickly realized how complicated it got. I realized that if I used my method of running the one elevator problem for each subset of passenger tuples, I would have to find all combinations in Stirling number of the second kind (number of ways to partition `n` objects into `k` non-empty subsets). In fact, I'd have to find all combinations of $S(n,k)$ for `k` <= number of elevators, as I'd have to check whether I need to use `k` or fewer elevators. This number grows exponentially and while I may be able to solve this recursively using $S(n,k)$'s recurrence relationship, I decided to just focus on the two elevator problem for simplicity.

However, the result I'm seeing from the two elevator problem suggests that I'd only have to find subsets of passenger tuples where all tuples in a subset follow one direction (i.e. subsets only consist of passengers wanting to go up or down). I'm working on a formal proof of the result.
