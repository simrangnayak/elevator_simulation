from elevator.main import Elevator
from building.main import Building
from two_elevator_system.main import System

def run():
    """
    This takes a total of 4 inputs:
        - floors: dictionary of floors pressed
        - ev_floor_1: position of elevator 1
        - ev_floor_2: plosition of elevator 2
        - min_floor: minimum floor of building
        - max_floor: maximum floor of building
    
    Assumptions:
        - This code assumes two elevators.
        - This code requires floors pressed (both inside and outside the elevator) be in dictionary format: keys as floors passengers are on, values as floors passengers would like to go to.
        - This code raises an error if floors pressed are outside of the range of the building.
        - This concept behind this elevator system is not purely of efficiency but rather the policy of no starvation.
    """
    # Keys represent the floors pressed in the building in the order they have been pressed
    # Values represent the floors passengers intend to go to for that key
    floors = {1:[0], 4:[6], 5:[3,2,7], 2:[1,6]}

    # Default position of elevators - this code assumes two elevators
    ev_floor_1 = 3
    ev_floor_2 = 6

    # Minimum floor of building
    min_floor = 0

    # Maximum floor of building
    max_floor = 10

    # Create elevator and building systems
    e1 = Elevator(cur_floor=ev_floor_1, direction=None)
    e2 = Elevator(cur_floor=ev_floor_2, direction=None)
    sys = System(e1_floor=ev_floor_1, e2_floor=ev_floor_2, pressed_floors=floors, minimum_floor=0, maximum_floor=10)
    e1_ideal, e2_ideal = sys.run()

    # Creates building classes based on ideal floor assignments
    building_1 = Building(pressed_floors=e1_ideal, minimum_floor=min_floor, maximum_floor=max_floor, elevator=e1)
    building_2 = Building(pressed_floors=e2_ideal, minimum_floor=min_floor, maximum_floor=max_floor, elevator=e2)
    
    # Process request
    print("Elevator 1:")
    e1_steps = building_1.run(True)
    print("Elevator 1 takes " + str(e1_steps) + " total step(s).")
    print("\n")
    print("Elevator 2:")
    e2_steps = building_2.run(True)
    print("Elevator 2 takes " + str(e2_steps) + " total step(s).")
    print("\n")
    total_steps = e1_steps + e2_steps
    print("Both elevators take " + str(total_steps) + " total step(s).")

if __name__ == '__main__':
    run()