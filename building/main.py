import numpy as np
import pandas as pd

from elevator.main import Elevator

class Building(object):
    def __init__(self, pressed_floors, minimum_floor, maximum_floor, elevator):
        """
        Initializing function for Building class
        """
        self.floor = pressed_floors # Note: pressed floors must be of dictionary type
        self.min_floor = minimum_floor
        self.max_floor = maximum_floor
        self.elevator = elevator
        
        self.down_floors = {}
        self.up_floors = {}

        # Below for-loop divides pressed floors into two directions: those wanting to go up and those wanting to go down
        for key, values in self.floor.items():
            for value in values:
                if value < key:
                    if key not in self.down_floors:
                        self.down_floors[key] = []
                    self.down_floors[key].append(value)
                else:
                    if key not in self.up_floors:
                        self.up_floors[key] = []
                    self.up_floors[key].append(value)
        
        # Sorts the floors to be most efficient depending on the direction
        self.down_floors = dict(sorted(self.down_floors.items(), reverse=True))
        self.up_floors = dict(sorted(self.up_floors.items()))

        # Sets moves taken as 0
        self.n_moves = 0

    def direction_pressed(self):
        """
        Selects direction that elevator should go first: up or down
        """
        # Edge case
        if self.floor == {}:
            return {}, {}, None

        # First floor elevator needs to visit
        first_floor = list(self.floor.keys())[0]

        # If first floor elevator needs to visit contains both up and down directions, check which direction has the least distance to travel to visit first drop off
        if first_floor in self.down_floors and first_floor in self.up_floors:
            first_down = list(self.down_floors.keys())[0]
            first_down_request = self.down_floors[first_down]
            min_down = abs(self.max_floor - self.min_floor)
            for i in first_down_request:
                holder = abs(first_down - i)
                if holder <= min_down:
                    min_down = holder
            
            first_up = list(self.up_floors.keys())[0]
            first_up_request = self.up_floors[first_up]
            min_up = abs(self.max_floor - self.min_floor)
            for i in first_up_request:
                    holder = abs(first_up - i)
                    if holder <= min_up:
                        min_up = holder
            
            min_direction = min(min_down, min_up)

            # If least amount of initial travel for down direction, elevator goes down first
            if min_direction == min_down:
                first_set = self.down_floors
                second_set = self.up_floors
                bool = True
            
            # If least amount of initial travel for up direction, elevator goes up first
            else:
                first_set = self.up_floors
                second_set = self.down_floors
                bool = False

        # If first floor elevator needs to visit contains down direction, elevator travels down first and then travels up
        elif first_floor in self.down_floors:
            first_set = self.down_floors
            second_set = self.up_floors
            bool = True
        
        # If first floor elevator needs to visit contains up direction, elevator travels up first and then travels down
        else:
            first_set = self.up_floors
            second_set = self.down_floors
            bool = False

        return first_set, second_set, bool

    def active(self, first_set, bool, print_bool):
        """
        Moves elevator to pick up and drop off passengers
        """
        # While loop ensures this movement is repeated until no floors left
        while first_set != {}:
            init_floor = self.elevator.floor
            idx = list(first_set.keys())[0]
            current_steps = 0

            # Moves elevator to first floor elevator needs to visit
            while idx != self.elevator.floor:
                if idx < self.elevator.floor:
                    self.elevator.direct = 'down'
                else:
                    self.elevator.direct = 'up'
                self.elevator.move()
                self.n_moves += 1
                current_steps +=1

            # Any floors passengers select to visit are added back into dictionary of floors to ensure they are seen
            for value in first_set[idx]:
                if value not in first_set:
                    first_set[value] = []
            del first_set[idx]

            # Once floors passengers choose to visit are adeded back in, floors are sorted again to ensure efficiency
            first_set = dict(sorted(first_set.items(), reverse=bool))

            # If this is the final elevator selection, print output #TODO: make this a better output statement
            if print_bool == True:
                print("travels from floor " + str(init_floor) + " to floor " + str(self.elevator.floor) + " in " + str(current_steps) + " step(s).")
    
    def run(self, print_bool):
        """
        Runs elevator in order of directions selected and returns number of total moves elevator makes
        """
        # Total list of floors pressed, either inside or out
        keys = list(self.floor.keys())
        values = [i for k,l in self.floor.items() for i in l]
        all_floors = keys + values

        # Raise error if any floor pressed is outside of building range
        if max(all_floors, default=self.min_floor) > self.max_floor or min(all_floors, default=self.max_floor) < self.min_floor:
            raise ValueError("Error. Floor(s) pressed are outside of building range.")

        first_set, second_set, bool = self.direction_pressed()
        self.active(first_set, bool, print_bool)
        self.active(second_set, not bool, print_bool)
        
        return self.n_moves