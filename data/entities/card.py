from data.entities.action import _Action


#This will be what used to write the validating functaions for the diffrent result types
class validator:
    def __init__(self, arg):
        pass
    
    def location_validator():
        pass
        


#The result types are what allow the cards to do actions
class Result:
    def __init__(self, move_loc = None, damage_loc = None, stage_mod_loc = None, summon_loc = None, debuff_loc = None, buff_loc = None):
        
        pass
    
    def movement(self, valid_movement):        
        #store valid move, damage, summon, stage_mod and rules for use
        #check validity of result through custom fuctions and rules of use
        #follow through
        pass
    
    def damage(self, valid_damage):
        pass
    
    def stage_mod(self, valid_stage_mod):
        pass
    
    def summon(self, valid_summon):
        pass
    
    def debuff(self, valid_debuff):
        pass
    
    def buff(self, valid_buff):
        pass


#card class that will list the cards types, text description of what the card will do, and the cards "result" or calculated action
class _card:
    def __init__(self, card_type: str, description: str, result: Result):
        pass