

class _hand:
    def __init__(self, *cards):
        self.cards = list(cards)
        
    def hand_update(self, events):
        action = self.ui_input_handler.handle_input(events)
        pass