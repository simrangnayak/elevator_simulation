import numpy as np
import pandas as pd

from elevator.main import Elevator
from building.main import Building

class System(object):
    def __init__(self, e1_floor, e2_floor, pressed_floors, minimum_floor, maximum_floor):
        """
        Initializing function for System class
        """
        self.e1_floor = e1_floor
        self.e2_floor = e2_floor

        self.floor = pressed_floors
        self.min_floor = minimum_floor
        self.max_floor = maximum_floor

    def ncr_combinations(self,floor_list):
        """
        Returns all nCr combinations given a list of tuples
        """
        # Initialize a list with empty subset, representing the start of our combinations
        combinations = [[]]
        for element in floor_list:
            # For each existing combination, create a new combination that includes the current element
            for sub_set in combinations.copy():
                new_sub_set = sub_set + [element]
                # Append the new combination to our list of combinations
                combinations.append(new_sub_set)

        return combinations
    
    def elevator_combinations(self):
        """
        Returns number of steps it takes for elevators to complete floor assignments for all combinations
        """
        # Changes floor dictionary into list
        floor_list = [(k,i) for k,l in self.floor.items() for i in l]
        combinations = self.ncr_combinations(floor_list)

        # Initializes dataframe to store floor assignments
        df = pd.DataFrame(columns=['e1_floors', 'e2_floors', 'steps_e1', 'steps_e2'])

        # For-loop goes through list of combinations and assigns tuples to elevators
        for i in combinations:
            e1_list = i
            if i == []:
                e2_list = floor_list    
            elif i == floor_list:
                e2_list = []
            else:
                e2_list = list(set(floor_list) - set(i))
            
            # Turns tuple lists back into dictionaries
            e1_dict = {}
            for j in e1_list:
                e1_dict.setdefault(j[0],[]).append(j[1])
            e2_dict = {}
            for j in e2_list:
                e2_dict.setdefault(j[0],[]).append(j[1])
            
            # Creates elevator and building classes based on floor assignments - this needs to be called here and not in init function to ensure elevator.floor resets at every i
            e1 = Elevator(cur_floor=self.e1_floor, direction='none')
            e2 = Elevator(cur_floor=self.e2_floor, direction='none')
            building_1 = Building(pressed_floors=e1_dict, minimum_floor=self.min_floor, 
                                maximum_floor=self.max_floor, elevator=e1)
            building_2 = Building(pressed_floors=e2_dict, minimum_floor=self.min_floor, 
                                maximum_floor=self.max_floor, elevator=e2)
            
            # Stores output in dataframe
            e1_steps = building_1.run(False)
            e2_steps = building_2.run(False)
            row_to_append = pd.DataFrame([{'e1_floors':e1_dict, 'e2_floors':e2_dict, 'steps_e1':e1_steps, 'steps_e2':e2_steps}])
            df = pd.concat([df,row_to_append])
        
        df['total_steps'] = df['steps_e1'] + df['steps_e2']
        return df
    
    def run(self):
        """
        Selects elevator assignments based on least number of total moves required
        """
        # Selects rows with least number of total moves
        df = self.elevator_combinations()
        df_ideal = df[df.total_steps == df.total_steps.min()]
        
        # If multiple ideal floor assignments, selects first one
        e1_ideal = df_ideal['e1_floors'].iloc[0]
        e2_ideal = df_ideal['e2_floors'].iloc[0]

        return e1_ideal, e2_ideal