import random

from ..entities.actor import _Actor

#set up master_order (to refer to) and modded_order (to change and run off of)
class Turn_order:
    def __init__(self):
        self.master_order = []
        self.modded_order = []
        self.current_turn = 0

    def get_current_turn(self):
        return self.modded_order[self.current_turn]
    
    def next_turn(self):
        if self.current_turn == len(self.modded_order):
            self.current_turn = 0
        else:
            self.current_turn = self.current_turn + 1

    def get_modded_turn(self):
        if self.current_turn > (len(self.modded_order) - 1):
            self.current_turn = 0
        return self.modded_order[self.current_turn]

    def add_to_master(self, actor : _Actor):
        #sets first actor to order
        if not self.master_order:
            self.master_order.append(actor)
            self.modded_order.append(actor)
        #sets actors based on speed
        else:
            x = 0
            check_speed = actor.speed
            HERE = len(self.master_order)
            while x < len(self.master_order):
                #faster actors go first
                if self.master_order[x].speed < check_speed:
                    self.master_order.insert(x, actor)
                    self.modded_order.insert(x, actor)
                    return
                #same speed actors get put in random order (only looks at first instence of same speed)
                elif self.master_order[x].speed == check_speed:
                    num = random.randint(0,1)
                    self.master_order.insert(x + num, actor)
                    self.modded_order.insert(x + num, actor)
                    return
                #slower speeds move down the list by one and check again
                else:
                    x = x + 1
            self.master_order.append(actor)
            self.modded_order.append(actor)

    #remove from master and mod
    def remove_from_master(self, actor : _Actor):
        for actors in self.master_order:
            if actors == actor:
                self.master_order.remove(actors)
        for actors in self.modded_order:
            if actors == actor:
                self.modded_order.remove(actors)

    #change mod without effecting master
    def add_to_modded(self, actor : _Actor):
        i = False
        x = 0
        check_speed = actor.speed
        while i == False:
            #faster actors go first
            if self.master_order[x].speed < check_speed:
                self.master_order.insert(x, actor)
                i = True
            #same speed actors get put in random order (only looks at first instence of same speed)
            elif self.master_order[x].speed == check_speed:
                num = random.randint(0,1)
                self.master_order.insert(x + num, actor)
            #slower speeds move down the list by one and check again
            else:
                x = x + 1
    
    #set mod base to master
    def refresh_order(self):
        self.modded_order = self.master_order

    #reset both lists
    def reset_order(self):
        self.master_order = []
        self.modded_order = []
        self.current_turn = 0