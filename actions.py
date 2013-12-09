from collections import namedtuple

Order = namedtuple('Order', ['starting_position', 'quantity', 'direction'])
TurnActions = namedtuple('TurnActions', ['orders', 'guys_to_hire'])

""" Gold prices to hire new guys """
GOLD_PER_GUY = 10

""" Action codes """
STAY = 0
PLANT = 1
HARVEST = 2
UP = 3
RIGHT = 4
DOWN = 5
LEFT = 6

ALL_ACTIONS = [ STAY, PLANT, HARVEST, UP, RIGHT, DOWN, LEFT ]
MOVE_ACTIONS = [ UP, RIGHT, DOWN, LEFT ]

OFFSETS = {
    STAY: (0, 0),
    PLANT: (0, 0),
    HARVEST: (0, 0),
    UP: (0, 1),
    RIGHT: (1, 0),
    DOWN: (0, -1),
    LEFT: (-1, 0)
}

ACTION_STRINGS = {
    STAY: "STAY",
    PLANT: "PLANT",
    HARVEST: "HARVEST",
    UP: "UP",
    RIGHT: "RIGHT",
    DOWN: "DOWN",
    LEFT: "LEFT"   
}
        
def next_pos(starting_pos, direction):
    if direction not in ALL_ACTIONS:
        return starting_pos
    x_off, y_off = OFFSETS[direction]
    x, y = starting_pos
    return x + x_off, y + y_off
    
# Returns the amount of gold and the number of seeds
# a plant may "pay out" if harvested at a given age.
def get_plant_payout(age, is_mine):
    gold_payouts = [10, 10, 10, 7, 7, 7, 3, 3, 3, 1, 1, 1,  0,  0,  0]
    seed_payouts = [ 0,  0,  0, 1, 1, 1, 3, 3, 3, 7, 7, 7, 10, 10, 10]
    gold = 0
    seeds = 0
    multiplier = 1
    if is_mine == False:
        multiplier = 3
    if 1 <= age and age < len(gold_payouts):
        gold = gold_payouts[(age - 1)]
        seeds = seed_payouts[(age - 1)]
    elif age >= len(gold_payouts):
        gold = gold_payouts[len(gold_payouts) - 1]
        seeds = seed_payouts[len(gold_payouts) - 1]    
    return (gold * multiplier, seeds)

