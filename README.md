Spazzberry
=============
This repo contains the client code for the AI Showdown competition Spazzberry.  Please contribute back with improvements.


Story
--------------------------
You just returned to your farm from your trip to Vegas.  Unfortunately you weren't so lucky at the slot machines and you kinda owe some guys a bunch of money so you decide to supplement your income by growing spazzberries.

Young spazzberries are the juiciest and most delicious.  Thus, the younger the spazzberry bush, the more gold it will earn you at market when harvested. As a spazzberry bush gets older, its berries become tough and bitter and are not worth very much.  At a certain point no one will even buy old spazzberries.  Seriously, they're gross.  Blegh!
    
Old spazzberry bushes aren't completely worthless, however.  You need them for seeds.  Spazzberry seeds are actually highly hallucinogenic and therefore cannot be (legally) bought or sold.  The only way you can get more spazzberry seeds is by harvesting them from existing plants.
   
You manage to procure a handful of spazzberry seeds (no easy task), hire some workers to plant and harvest, and get to farming.
   
Wait, what's this? Some other jerk has started another spazzberry farm near yours!
    
Actually, that's not so bad because purloined spazzberries are even sweeter.  We aren't really sure how that works, but we know better than to ask.  A farmer who harvests another farmer's spazzberries will earn 3 times as much gold at market for those tender, succulent fruits.
    
Of course that means you may need to have your workers guard your own plants.  You can spend some of your gold to hire more workers to expand your operation.
    
The game ends after 1000 turns and the farmer who has earned the most gold wins.
   
Files
--------------------------

    github: https://github.com/aishowdown/spazzberry
    download: https://github.com/aishowdown/spazzberry/archive/master.zip

    I would recommend using git to clone the project so that you can easily ‘git pull’ down any bug fixes or updates that may be made throughout the week.

Game details
--------------------------
Each player starts with:
* 10 Seeds
* 5 Workers
* 0 Gold

Players' spawn points are placed randomly, but will be sufficiently distant and mirrored about the center of the grid.

On each turn, each player gets to know:
* How many seeds they have
* How much gold they have
* How much gold their opponent has
* The positions of all workers (both players')
* The positions and ages of all plants (both players').  A plant's value can be derived from its age.

On each turn, each player gets to:
* Order their workers to take various actions (see below).
* Hire more workers.
     
For any given turn, any guy may take any one of the following actions:
* STAY - Stay on the current square and do nothing.
* UP - Move up a square.
* DOWN - Move down a square.
* LEFT - Move left a square.
* RIGHT - Move right a square.
* PLANT - Spend 1 Seed and plant a spazzberry bush on the current square.
* HARVEST - Harvest the spazzberry bush on the current square.
        
API
--------------------------
Packaged with the game are two sample bots randomplayer.py and moochplayer.py.  Use these as a jumping off point.  There are somewhat extensive comments in the example bots explaining how to program your bot.  If you would like to write your bot in a different language see below.

Running a game
--------------------------
Put your bot in the same directory as the given code and simply run game.py with the filenames of the two bots you want to use as the arguments.

    python game.py mybot1.py mybot2.py

If you open viz.html in your browser you can see a game unfold.

Competition
--------------------------
The final competition will take place TBD.  It will be a double elimination style competition, and the results of each round will be viewable on www.aishowdown.com.  Every evening preceding the competition we will run practice rounds.  Upload your bot to the website to get insight in what other people are creating.


Other Languages
--------------------------
We allow players to write clients in other languages.  To do this, you will need to write a script that takes in a port via command line.  Listen on this port for POST requests containing json data.  The map will be sent at the beginning of the game to /map,  each round a post will be made to / with the current game state and expect json to be returned.  You can test these bots by running

    python game.py nonnetworkedBot.py 2103

where 2103 is the port your bot is listening on.







