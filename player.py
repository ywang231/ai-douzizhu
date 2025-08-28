# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring

import asyncio
import random
from typing import Callable
from logger import Logging


class Player:

    name: str
    hand_: list
    cards_played_: list
    is_landlord_: bool
    brain_: Callable[[list], asyncio.Future]

    def __init__(self, name):
        self.name = name
        self.hand_ = []
        self.cards_played_ = []
        self.is_landlord_ = False
        self.brain_ = None  # The AI brain for the player

    @property
    def brain(self):
        return self.brain_

    @brain.setter
    def brain(self, brain):
        self.brain_ = brain

    def accept_hands(self, hands: list):
        '''Accepts the initial hands for the player.'''
        self.hand_ = hands

    def append_landlord_cards(self, cards: list):
        '''Appends the landlord cards to the player's hand.'''
        self.hand_.extend(cards)
        self.is_landlord_ = True

    async def landlord_bidding(self, min_score: int = 1):
        '''Makes a bidding decision for the player.'''
        Logging(f"{self.name} is making a bidding decision.")

        await asyncio.sleep(2)  # Simulate thinking time
        score_bid = random.randint(min_score, 3)
        # random pick either 0 or score_bid
        final_bid = random.choice([0, score_bid])

        if final_bid > 0:
            Logging(
                f"{self.name} choose to bid with {final_bid} "
                f"{'points' if final_bid > 1 else 'point'}")
        else:
            Logging(f"{self.name} choose to pass")
        return final_bid

    async def final_double_bid(self, final_score: int):
        '''Makes a final double bidding decision for the player.'''
        Logging(
            f"{self.name} is making a bidding decision for the final round ")

        await asyncio.sleep(2)  # Simulate thinking time
        bid = random.choice([0, final_score])

        if bid > 0:
            Logging(
                f"{self.name} final bid: {bid} "
                f"{'points' if bid > 1 else 'point'}")
        else:
            Logging(f"{self.name} choose to pass")
        return bid

    async def play_card(self, previous_played_cards: list[tuple]):
        '''Plays a card from the player's hand.'''
        if len(previous_played_cards) > 0:
            print(
                f"{self.name} sees previous played cards: {previous_played_cards}")

        if self.hand_:
            card = self.hand_.pop()
            self.cards_played_.append(card)
            return card
        return None
