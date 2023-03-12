# class _hand:
#     def __init__(self, *cards):
#         self.cards = list(cards)
#
#     def hand_update(self, events):
#         action = self.ui_input_handler.handle_input(events)
#         pass
import pygame

from data.engine import gfxengine
from data.entities.actor import _Actor
from data.entities.card import _Card, Indicator


class Hand:
    def __init__(self, owner: _Actor):
        owner.give_hand(self)
        self.x, self.y = 0, 433
        self.card_width = 31
        self.card_height = 47
        self.card_gap = 10
        self.owner = owner
        self.cards = []
        self.card_rects = []
        self.selected_card = None
        self.indicators = []

    def add_rect(self):
        left = (len(self.cards) - 1) * (self.card_width + self.card_gap) + self.x
        top = self.y
        width = self.card_width
        height = self.card_height
        new_rect = pygame.Rect(left, top, width, height)
        self.card_rects.append(new_rect)

    def remove_rect(self):
        self.card_rects.pop()

    def add_card(self, card: _Card):
        self.cards.append(card)
        self.add_rect()
        card.owner = self.owner
        self.cards.sort(key=lambda c: c.name)

    def remove_card(self, card: _Card):
        if card in self.cards:
            card.owner = None
            self.cards.remove(card)
            self.remove_rect()
            if card == self.selected_card:
                self.deselect_card()

    def deselect_card(self):
        self.selected_card = None
        self.indicators.clear()

    def select_card(self, card: _Card):
        if self.selected_card != card:
            self.deselect_card()
            self.selected_card = card
            card.activate(self.indicators)

    def click(self, x, y):
        for index, rect in enumerate(self.card_rects):
            if rect.collidepoint(x, y):
                self.select_card(self.cards[index])
                return
        for indicator in self.indicators:
            tile_clicked_x = int(x / 32)
            tile_clicked_y = int(y / 32)
            if tile_clicked_x == indicator.x and tile_clicked_y == indicator.y:
                indicator.activate()
                self.indicators.clear()
                self.remove_card(self.selected_card)
                return
        self.deselect_card()

    # def get_clicked_card(self, mouse_x, mouse_y):
    #     for index, rect in enumerate(self.card_rects):
    #         if rect.collidepoint(mouse_x, mouse_y):
    #             return self.cards[index]
    #     return None

    def draw(self, screen):
        for index, card in enumerate(self.cards):
            x = index * (self.card_width + self.card_gap) + self.x
            gfxengine.draw(screen, card.texture_id, x, self.y)

        for indicator in self.indicators:
            gfxengine.draw_on_grid(screen, indicator.indicator_type, indicator.x, indicator.y)
