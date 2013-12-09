import actions
import random

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
        orders = {}
        guys_to_hire = 0
        total_guys = 0
        
        width = len(guys)
        height = len(guys[0])
        
        for x in range(width):
            for y in range(height):
            
                if guys[x][y] == None: continue
                num_guys, is_mine = guys[x][y]
                if not is_mine: continue
                                
                total_guys = total_guys + num_guys
                
                # Algorithm:
                # If there is NOT a plant on this square:
                #   Leave one guy here.
                #   If we have any seeds, plant a plant here.
                #   Move any remaining guys in random directions.
                # If there IS a plant on this square:
                #   Harvest the plant if we get some gold and some seeds.
                #   Move any remaining guys in random directions.
                if plants[x][y] == None:
                    if my_seeds > 0:
                        orders[((x,y), actions.PLANT)] = 1
                        num_guys = num_guys - 1                     
                else:
                    age, plant_is_mine = plants[x][y]
                    gold, seeds = actions.get_plant_payout(age, plant_is_mine)
                    if age >= 5:
                        orders[((x,y), actions.HARVEST)] = 1
                        num_guys = num_guys - 1
                
                # Any remaining guys get moved in random directions.
                if num_guys > 0:
                    for g in range(num_guys):
                        a = random.choice(actions.MOVE_ACTIONS)
                        if ((x, y), a) not in orders:
                            orders[((x, y), a)] = 1
                        else:
                            orders[((x, y), a)] = orders[((x, y), a)] + 1
                            
        # If we have enough gold, hire a new guy.
        if my_gold > (total_guys * actions.GOLD_PER_GUY * 100):
            guys_to_hire = 1

        return (orders, guys_to_hire)
