import json

import httplib, urllib

class NetworkPlayer():
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}

    def __init__(self, port, money_payout_rates, my_spawn_point, their_spawn_point):
        print "initing with %s" % port
        self.port = port
        conn = httplib.HTTPConnection("127.0.0.1:%s" % self.port)

        jsonmap = json.dumps({
            "my_spawn_point": my_spawn_point,
            "their_spawn_point": their_spawn_point
            });
        conn.request("POST", "/map", urllib.urlencode({'data': jsonmap}), self.headers)



    def take_turn(self, guys, plants, my_gold, their_gold, my_seeds):
        conn = httplib.HTTPConnection("127.0.0.1:%s" % self.port)

        jsonmap = json.dumps({
            "guys": guys,
            "plants": plants,
            "my_gold": my_gold,
            "their_gold": their_gold,
            "my_seeds": my_seeds
        });
        conn.request("POST", "/", urllib.urlencode({'data': jsonmap}), self.headers)
        resp = conn.getresponse()
        jsonOrders = json.load(resp)
        orders = {}
        #This can be cleaned up

        for order in jsonOrders:
            orders[(order[0], order[1]), order[2]] = order[3]
            guys_to_hire = order[4]

        return (orders, guys_to_hire);
