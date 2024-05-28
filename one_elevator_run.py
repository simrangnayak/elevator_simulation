from elevator.main import Elevator
from building.main import Building

def run():
    """
    This takes a total of 4 inputs:
        - floors: dictionary of floors pressed
        - ev_floor: position of elevator
        - min_floor: minimum floor of building
        - max_floor: maximum floor of building
    
    Assumptions:
        - This code assumes one elevator.
        - This code requires floors pressed (both inside and outside the elevator) be in dictionary format: keys as floors passengers are on, values as floors passengers would like to go to.
        - This code raises an error if floors pressed are outside of the range of the building.
        - This concept behind this elevator system is not purely of efficiency but rather the policy of no starvation.
    """
    # Keys represent the floors pressed in the building in the order they have been pressed
    # Values represent the floors passengers intend to go to for that key
    floors = {1:[0], 4:[6], 5:[3,2,7], 2:[1,6]}

    # Default position of elevator - this code assumes a singular elevator
    ev_floor = 3

    # Minimum floor of building
    min_floor = 0

    # Maximum floor of building
    max_floor = 10

    # Create elevator and building systems
    ev = Elevator(cur_floor=ev_floor, direction=None)
    building = Building(pressed_floors=floors, minimum_floor=min_floor, maximum_floor=max_floor, elevator=ev)

    # Process request
    print("Elevator:")
    steps = building.run(True)
    print("Elevator takes " + str(steps) + " total step(s).")

if __name__ == '__main__':
    run()