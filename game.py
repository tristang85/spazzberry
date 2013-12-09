# Spazzberry
#
#   You just moved to the country and decided to start a spazzberry farm.  You
#   start your farm with 5 workers and 10 seeds and set to planting and
#   harvesting spazzberry plants.
#    
#   Young spazzberries are the juiciest and most delicious.  Thus, the younger
#   the spazzberry bush, the more gold it will earn you at market when
#   harvested. As a spazzberry bush gets older, its berries become tough and
#   bitter and are not worth very much.  At a certain point no one will even
#   buy old spazzberries.  Seriously, they're gross.  Blegh!
#    
#   Old spazzberry bushes aren't completely worthless, however.  You need them
#   for seeds.  Spazzberry seeds are actually highly hallucinogenic and
#   therefore cannot be bought or sold.  The only way you can get more
#   spazzberry seeds is by harvesting them from existing plants.
#    
#   Wait, what's this? Some other jerk has started a farm near yours!
#    
#   Actually, that's not so bad because purloined spazzberries are even
#   sweeter.  A farmer who harvests another farmer's spazzberries will earn 3
#   times as much gold at market for those tender, succulent fruits.
#    
#   Of course that means you may need to have your workers guard your own
#   plants.  You can even spend some of your gold to hire more workers to
#   expand your operation.
#    
#   The game ends after 1000 turns and the farmer who has earned the most gold
#   wins
#
# Each player starts with:
#    * 10 Seeds
#    * 5 Workers
#    * 0 Gold
#
# Players' spawn points are placed randomly, but will be sufficiently distant
# and mirrored about the center of the grid.
#
# On each turn, each player gets to know:
#    * How many seeds they have
#    * How much gold they have
#    * How much gold their opponent has
#    * The positions of all workers(both players')
#    * The positions and ages of all plants (both players')
#
# On each turn, each player gets to:
#    * Order their workers to take various actions (see below).
#    * Hire more workers.
# 
# For any given turn, any guy may take any one of the following actions:
#    * STAY - Stay on the current square and do nothing.
#    * UP - Move up a square.
#    * DOWN - Move down a square.
#    * LEFT - Move left a square.
#    * RIGHT - Move right a square.
#    * PLANT - Spend 1 Seed and plant a spazzberry bush on the current square.
#    * HARVEST - Harvest the spazzberry bush on the current square.
#
        
import sys
import json
import re
import httplib, urllib
from functools import partial

from networkplayer import NetworkPlayer

from map import Map
import actions

NUM_TURNS = 1000

if len(sys.argv) != 3:
    print "Usage: %s player1_module player2_module" % sys.argv[0]
    sys.exit(1)


if sys.argv[1].endswith(".py"):
    exec('from %s import Player as Player1' % sys.argv[1][:-3])
else:
    Player1 = partial(NetworkPlayer, sys.argv[1])


if sys.argv[2].endswith(".py"):
    exec('from %s import Player as Player2' % sys.argv[2][:-3])
else:
    Player2 = partial(NetworkPlayer, sys.argv[2])


m = Map()
p1_crashed = False
p2_crashed = False
p1 = Player1(*m.constructor_data_for_p1())
p2 = Player2(*m.constructor_data_for_p2())


json_data = {'p1_spawn': m.p1_spawn,
             'p2_spawn': m.p2_spawn,
             'p1_name' : sys.argv[1],
             'p2_name' : sys.argv[2],
             'winner' : 0,
             'max_guys': m.max_guys,
             'max_gold': m.max_gold,
             'max_seeds': m.max_seeds,
             'turns': [m.board_state_for_json(0)]}

# Spawn some initial guys.
m.spawn_new_guys()

for turn in range(NUM_TURNS):
    print 'Turn #%d' % turn

    # Get the players' actions
    try:
        p1_actions = [] if p1_crashed else p1.take_turn(*m.turn_data_for_p1(turn))
    except:
        print "P1 Crashed!"
        p1_crashed = True

    try:
        p2_actions = [] if p2_crashed else p2.take_turn(*m.turn_data_for_p2(turn))
    except:
        print "P2 Crashed!"
        p2_crashed = True

    m.apply_actions(p1_actions, p2_actions, turn)
    m.resolve_combat()

    m.spawn_new_guys()

    m.resolve_combat() #in case the new guys spawned into combat

    json_data['turns'].append(m.board_state_for_json(turn))

json_data['max_guys'] = m.max_guys
json_data['max_gold'] = m.max_gold
json_data['max_seeds'] = m.max_seeds

print '---- FINAL SCORE ----'
print '%s:\t%d' % (sys.argv[1], m.p1_gold)
print '%s:\t%d' % (sys.argv[2], m.p2_gold)
print

winner = sys.argv[1]
if m.p1_gold > m.p2_gold:
    print 'WINNER: %s' % sys.argv[1]
    json_data['winner'] = 1
elif m.p1_gold < m.p2_gold:
    print 'WINNER: %s' % sys.argv[2]
    json_data['winner'] = 2
else:
    print 'TIED!'

# Save the game log to disk for visualization later
json_str = json.dumps(json_data)
with open('game_log.js', 'w') as f:
    f.write("window.game = %s" % json_str)



        
