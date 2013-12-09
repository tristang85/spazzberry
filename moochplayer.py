import actions
import random
import math

class Player:
    #Get passed all the board information that never changes throughout the game.
    #It is recommended that you store these in member variables since you will probably need to look at them later.
    # PARAMS:

    #  my_spawn_point:
    #   An (x, y) tuple of where your new chickens will hatch each turn

    #  their_spawn_point:
    #   An (x, y) tuple of where your opponent's chickens will hatch each turn

    def __init__(self, my_spawn_point, their_spawn_point):
        self.my_spawn_point = my_spawn_point
        self.their_spawn_point = their_spawn_point

    # Gets called each turn and where you decide what actions your guys take and if you
    # hire more guys or buy more seeds.
    # PARAMS:

    #   guys:
    #       A 50x50 2D matrix showing where all the guys are on the board.
    #       An entry of 'None' indicates an unoccupied spot.
    #       A space with guys will be an object with "num_guys" and "is_mine" properties.

    #   plants:
    #       A 50x50 2D matrix showing where all the plants are on the board.
    #       An entry of 'None' indicates an unoccupied spot.
    #       A space with plant will be an object with "age" and "is_mine" properties.
    
    #   my_gold:
    #       An integer indicating how much gold you currently have.

    #   their_gold:
    #       An integer indicating how much gold your opponent currently has.

    #   my_seeds:
    #       An integer indicating how many seeds you currently have.

    # RETURN:
    #   A tuple consisting of (orders, guys_to_hire) where
    #   orders is a python dict that takes the position and action as a key
    #   and whose value indicates the number of guys to apply that action.

    def take_turn(self, guys, plants, my_gold, their_gold, my_seeds):
        self.width = len(guys)
        self.height = len(guys[0])
        orders = {}
        guys_to_hire = 0
        total_guys = 0

        for x in range(self.width):
            for y in range(self.height):
            
                if guys[x][y] == None: continue
                num_guys, is_mine = guys[x][y]
                if not is_mine: continue
                
                total_guys = total_guys + num_guys
                
                # This is the super-aggressive strategy.
                # Send all guys after the enemy's plants and harvest them.
                # Buy some guys when we hit certain gold levels.
                
                # First, see if there's a plant to harvest.
                if plants[x][y] != None:
                    age, plant_is_mine = plants[x][y]
                    # We don't really care if this plant is ours or is any good, just harvest it.
                    orders[(x,y), actions.HARVEST] = 1
                    num_guys = num_guys - 1
                
                # Move remaining guys towards closest good enemy plant.
                if num_guys > 0:
                    target = self.__get_closest_square((x,y), self.__is_good_enemy_plant, guys, plants)
                    
                    # The enemy doesn't have any plants so move towards their spawn point instead.
                    if target == None:
                        target = self.their_spawn_point
                    
                    move_action = self.__get_direction((x,y), target)
                    orders[(x,y), move_action] = num_guys                

        # Hire a new guy?
        if my_gold > (total_guys * actions.GOLD_PER_GUY * 100):
            guys_to_hire = 1
        
        return (orders, guys_to_hire)

    # For a given x,y and a target x,y, this returns a movement action (see action.py)
    # that will get the guy at the x,y closer to the target x,y
    def __get_direction(self, cur_pos, target_pos):
        x_diff = cur_pos[0] - target_pos[0]
        y_diff = cur_pos[1] - target_pos[1]
        
        # If the position is the same, stay put.
        if x_diff == 0 and y_diff == 0 or not self.__is_on_board(target_pos):
            return actions.STAY
            
        # If the x distance is longer, move along the x-axis
        if math.fabs(x_diff) > math.fabs(y_diff):
            if x_diff < 0: return actions.RIGHT
            else: return actions.LEFT
        elif math.fabs(x_diff) == math.fabs(y_diff):
            # The difference in x and y is the same, pick which
            # direction to go at random.
            choose_x = random.randint(0,1)
            if choose_x == 1:
                if x_diff < 0: return actions.RIGHT
                else: return actions.LEFT
            else:
                if y_diff < 0: return actions.UP
                else: return actions.DOWN
        else:
            if y_diff < 0: return actions.UP
            else: return actions.DOWN                
        return actions.STAY

    # Returns if a given position is on the board or not.
    def __is_on_board(self, position):
        x, y = position
        if x < 0 or x >= self.width: return False
        if y < 0 or y >= self.height: return False
        return True

    # Returns the distance between two points.
    def __get_distance(self, start, end):
        # Guys can't move diagonally so the effective distance is simply the
        # x difference plus the y difference.
        return math.fabs(start[0] - end[0]) + math.fabs(start[1] - end[1])
        
    # Returns True if there is an enemy plant at a given position and that plant
    # will pay out some non-zero amount of gold.
    def __is_good_enemy_plant(self, pos, guys, plants):
        x, y = pos
        if plants[x][y] != None:
            age, is_mine = plants[x][y]
            if is_mine == False:
                gold, seeds = actions.get_plant_payout(age, is_mine)
                if gold > 0:
                    return True
        return False
                   
    # This function does a fast search outwards, starting at a given position and
    # returns whichever is the closest square that satisfies the "is_candidate_function".
    # The is_candidate_function is passed an (x,y), the guys array, and the plants
    # array and must return True or False.
    # If it returns True then that square is a candidate and may be chosen if its the
    # closest candidate square to the given position.
    def __get_closest_square(self, pos, is_candidate_function, guys, plants):
        width = self.width
        height = self.height
        offset = 1
        searching = True
        posx, posy = pos
        
        best_distance = width + height
        best_x = -1
        best_y = -1
        
        while searching:
            xstart = posx - offset
            if xstart < 0: xstart = 0
            xend = posx + offset
            if xend >= width: xend = width - 1
            for x in range(xstart, xend):
                y = posy - offset
                if y < 0: y = 0
                if is_candidate_function((x,y), guys, plants):
                    distance = self.__get_distance(pos, (x,y))
                    if distance < best_distance:
                        best_distance = distance
                        best_x = x
                        best_y = y
                        
                y = posy + offset
                if y >= height: y = height - 1
                if is_candidate_function((x,y), guys, plants):
                    distance = self.__get_distance(pos, (x,y))
                    if distance < best_distance:
                        best_distance = distance
                        best_x = x
                        best_y = y
                        
            ystart = posy - offset
            if ystart < 0: ystart = 0
            yend = posy + offset
            if yend >= height: yend = height - 1
            for y in range(ystart,yend):
                x = posx - offset + 1
                if x < 0: x = 0
                if is_candidate_function((x,y), guys, plants):
                    distance = self.__get_distance(pos, (x,y))
                    if distance < best_distance:
                        best_distance = distance
                        best_x = x
                        best_y = y
                        
                x = posx + offset - 1
                if x >= width: x = width - 1
                if is_candidate_function((x,y), guys, plants):
                    distance = self.__get_distance(pos, (x,y))
                    if distance < best_distance:
                        best_distance = distance
                        best_x = x
                        best_y = y
                        
            # Found the closest spot, done searching.
            if best_x != -1:
                searching = False
                        
            # Search area is as big as the grid itself, done searching.
            if xstart == 0 and xend == (width - 1) and ystart == 0 and yend == (height - 1):
                searching = False
                
            offset = offset + 1         
            
        if best_x == -1:
            return None
        else:
            return (best_x, best_y)
