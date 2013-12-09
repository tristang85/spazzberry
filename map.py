import json
import math
import random
import copy

from collections import namedtuple
Population = namedtuple('Population', ['num_guys', 'is_mine'])
Flora = namedtuple('Flora', ['age', 'is_mine'])

import actions

class Map:
    """ A class that represents the relevant features of a game board """
    WIDTH = 50
    HEIGHT = 50
    STARTING_GOLD = 0
    STARTING_SEEDS = 10
    STARTING_GUYS = 5

    def __init__(self):
        self.width, self.height = Map.WIDTH, Map.HEIGHT
        self.p1_guys = [[0] * self.height for x in range(self.width)]
        self.p2_guys = [[0] * self.height for x in range(self.width)]
        # The elements in the plant array indicates the turn on which
        # the plant was planted.  Subtract this value from the current
        # turn to determine the plants age (and payout).
        # Initialize to -1 since 0 is a valid turn value.
        self.p1_plants = [[-1] * self.height for x in range(self.width)]
        self.p2_plants = [[-1] * self.height for x in range(self.width)]
        self.p1_seeds = Map.STARTING_SEEDS
        self.p2_seeds = Map.STARTING_SEEDS
        self.p1_gold = Map.STARTING_GOLD
        self.p2_gold = Map.STARTING_GOLD
        self.p1_spawn, self.p2_spawn = self.__generate_spawn_points()
        self.p1_guys_to_spawn = Map.STARTING_GUYS
        self.p2_guys_to_spawn = Map.STARTING_GUYS
        self.max_guys = 0
        self.max_gold = 0
        self.max_seeds = 0

    def board_state_for_json(self, turn):
        p1_guys_json = []
        p2_guys_json = []
        p1_plants_json = []
        p2_plants_json = []
        for x in range(self.width):
            for y in range(self.height):
                if self.p1_guys[x][y] > 0:
                    p1_guys_json.append([x, y, self.p1_guys[x][y]])
                elif self.p2_guys[x][y] > 0:
                    p2_guys_json.append([x, y, self.p2_guys[x][y]])
                # For plants, subtract the turn the plant was planted with
                # the current turn to determine the plant's age.
                if self.p1_plants[x][y] >= 0 and self.p1_plants[x][y] != turn:
                    p1_plants_json.append([x, y, int(turn - self.p1_plants[x][y])])
                elif self.p2_plants[x][y] >= 0 and self.p2_plants[x][y] != turn:
                    p2_plants_json.append([x, y, int(turn - self.p2_plants[x][y])])
        return {'p1m': self.p1_gold, 'p2m': self.p2_gold,
                'p1s' : self.p1_seeds, 'p2s' : self.p2_seeds,
                'p1g': p1_guys_json, 'p2g': p2_guys_json,
                'p1p' : p1_plants_json, 'p2p' : p2_plants_json}

    def spawn_new_guys(self):
        if self.p1_guys_to_spawn > 0:
            p1_spawn_x, p1_spawn_y = self.p1_spawn
            current = self.p1_guys[p1_spawn_x][p1_spawn_y]
            self.p1_guys[p1_spawn_x][p1_spawn_y] = int(current) + int(self.p1_guys_to_spawn)
            self.p1_guys_to_spawn = 0

        if self.p2_guys_to_spawn > 0:
            p2_spawn_x, p2_spawn_y = self.p2_spawn
            current = self.p2_guys[p2_spawn_x][p2_spawn_y]
            self.p2_guys[p2_spawn_x][p2_spawn_y] = int(current) + int(self.p2_guys_to_spawn)
            self.p2_guys_to_spawn = 0            
    
    def apply_actions(self, p1_actions, p2_actions, turn):
        new_p1_guys = [[0] * self.height for x in range(self.width)]
        new_p2_guys = [[0] * self.height for x in range(self.width)]
        # Resolve P1 actions
        orders, guys_to_hire = p1_actions
        for (x, y), action in orders:
            quantity = int(orders[((x, y), action)])
            if action not in actions.ALL_ACTIONS:
                continue
            if self.p1_guys[x][y] >= quantity:
                if action in actions.MOVE_ACTIONS:
                    # Resolve movement
                    new_x, new_y = actions.next_pos((x, y), action)
                    if self.__is_on_board((new_x, new_y)):
                        new_p1_guys[new_x][new_y] += quantity
                        self.p1_guys[x][y] -= quantity
                elif action == actions.PLANT:
                    # Plant a plant if there's no plant already here and they
                    # have enough seeds.
                    if self.p1_plants[x][y] < 0 and self.p2_plants[x][y] < 0 and self.p1_seeds > 0:
                        self.p1_plants[x][y] = turn
                        self.p1_seeds = self.p1_seeds - 1
                elif action == actions.HARVEST:
                    # Harvest a plant, but not one you planted this turn!
                    if self.p1_plants[x][y] >= 0 and self.p1_plants[x][y] != turn:
                        gold, seeds = actions.get_plant_payout(turn - self.p1_plants[x][y], True)
                        self.p1_gold = self.p1_gold + gold
                        self.p1_seeds = self.p1_seeds + seeds
                        self.p1_plants[x][y] = None                        
                    elif self.p2_plants[x][y] >= 0 and self.p2_plants[x][y] != turn:
                        gold, seeds = actions.get_plant_payout(turn - self.p2_plants[x][y], False)
                        self.p1_gold = self.p1_gold + gold
                        self.p1_seeds = self.p1_seeds + seeds
                        self.p2_plants[x][y] = None      
        # Hire more guys for P1
        if self.p1_gold >= (guys_to_hire * actions.GOLD_PER_GUY):
            self.p1_guys_to_spawn = guys_to_hire
            self.p1_gold = self.p1_gold - (guys_to_hire * actions.GOLD_PER_GUY) 
        
        # Resolve P2 actions
        orders, guys_to_hire = p2_actions
        for (x, y), action in orders:
            quantity = int(orders[((x, y), action)])
            if action not in actions.ALL_ACTIONS: continue
            if self.p2_guys[x][y] >= quantity:
                if action in actions.MOVE_ACTIONS:
                    # Resolve movement
                    new_x, new_y = actions.next_pos((x, y), action)
                    if self.__is_on_board((new_x, new_y)):
                        new_p2_guys[new_x][new_y] += quantity
                        self.p2_guys[x][y] -= quantity
                elif action == actions.PLANT:
                    # Plant a plant if there's no plant already here and they
                    # have enough seeds.
                    if self.p2_plants[x][y] < 0 and self.p1_plants[x][y] < 0 and self.p2_seeds > 0:
                        self.p2_plants[x][y] = turn
                        self.p2_seeds = self.p2_seeds - 1
                elif action == actions.HARVEST:
                    # Harvest a plant
                    if self.p2_plants[x][y] >= 0 and self.p2_plants[x][y] != turn:
                        gold, seeds = actions.get_plant_payout(turn - self.p2_plants[x][y], True)
                        self.p2_gold = self.p2_gold + gold
                        self.p2_seeds = self.p2_seeds + seeds
                        self.p2_plants[x][y] = None                        
                    elif self.p1_plants[x][y] >= 0 and self.p1_plants[x][y] != turn:
                        gold, seeds = actions.get_plant_payout(turn - self.p1_plants[x][y], False)
                        self.p2_gold = self.p2_gold + gold
                        self.p2_seeds = self.p2_seeds + seeds
                        self.p1_plants[x][y] = None                     
        # Hire more guys for P2
        if self.p2_gold >= (guys_to_hire * actions.GOLD_PER_GUY):
            self.p2_guys_to_spawn = guys_to_hire
            self.p2_gold = self.p2_gold - (guys_to_hire * actions.GOLD_PER_GUY)

        for x in range(self.width):
            for y in range(self.height):
                new_p1_guys[x][y] += self.p1_guys[x][y]
                new_p2_guys[x][y] += self.p2_guys[x][y]
        self.p1_guys = new_p1_guys
        self.p2_guys = new_p2_guys
        
        # Keep track of the max gold and max seeds seen so far.  We'll
        # use this to normalize the values for the line graph in the
        # visualization.
        self.max_gold = max(self.max_gold, self.p1_gold, self.p2_gold)
        self.max_seeds = max(self.max_seeds, self.p1_seeds, self.p2_seeds)

    def resolve_combat(self):
        p1_total_guys = 0
        p2_total_guys = 0
        for x in range(self.width):
            for y in range(self.height):
                num_dead = min(self.p1_guys[x][y], self.p2_guys[x][y])
                if num_dead < 0:
                    print num_dead
                else:
                    self.p1_guys[x][y] -= num_dead
                    self.p2_guys[x][y] -= num_dead
                    # This is a convenient time to find out how many
                    # total guys each player has.
                    p1_total_guys = p1_total_guys + self.p1_guys[x][y]
                    p2_total_guys = p2_total_guys + self.p2_guys[x][y]
        
        # Now update the max number of guys we've seen so far.
        # We'll use this to normalize the guys line graph in the visualization.
        self.max_guys = max(self.max_guys, p1_total_guys, p2_total_guys)

    def __is_on_board(self, position):
        x, y = position
        if x < 0 or x >= self.width: return False
        if y < 0 or y >= self.height: return False
        return True

    def constructor_data_for_p1(self):
        return (self.p1_spawn, self.p2_spawn)

    def constructor_data_for_p2(self):
        return (self.p2_spawn, self.p1_spawn)

    def turn_data_for_p1(self, turn):
        guys = [[None] * self.height for x in range(self.width)]
        plants = [[None] * self.height for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if self.p1_guys[x][y]:
                    guys[x][y] = Population(self.p1_guys[x][y], True)
                elif self.p2_guys[x][y]:
                    guys[x][y] = Population(self.p2_guys[x][y], False)                    
                if self.p1_plants[x][y] >= 0:
                    plants[x][y] = Flora(int(turn - self.p1_plants[x][y]), True)
                elif self.p2_plants[x][y] >= 0:
                    plants[x][y] = Flora(int(turn - self.p2_plants[x][y]), False)
        return (guys, plants, self.p1_gold, self.p2_gold, self.p1_seeds)

    def turn_data_for_p2(self, turn):
        guys = [[None] * self.height for x in range(self.width)]
        plants = [[None] * self.height for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if self.p1_guys[x][y]:
                    guys[x][y] = Population(self.p1_guys[x][y], False)
                elif self.p2_guys[x][y]:
                    guys[x][y] = Population(self.p2_guys[x][y], True)
                if self.p1_plants[x][y] >= 0:
                    plants[x][y] = Flora(int(turn - self.p1_plants[x][y]), False)
                elif self.p2_plants[x][y] >= 0:
                    plants[x][y] = Flora(int(turn - self.p2_plants[x][y]), True)
        return (guys, plants, self.p2_gold, self.p1_gold, self.p2_seeds)

    def __mirror(self, x, y):
        """ Mirror a point over the diagonal of the map """
        return (self.width - x - 1, self.height - y - 1)

    def __generate_spawn_points(self):
        """ Keep trying random points until it's mirror is far enough away """
        while True:
            p1x = random.randint(0, self.width - 1)
            p1y = random.randint(0, self.height - 1)
            p2x, p2y = self.__mirror(p1x, p1y)
            d_sq = (p1x - p2x)**2 + (p1y - p2y)**2
            if d_sq >= (self.width / 2)**2:
                break
        return (p1x, p1y), (p2x, p2y)
            
    def to_struct(self):
        return {'p1_spawn': self.p1_spawn,
                'p2_spawn': self.p2_spawn}
