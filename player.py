# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring

import asyncio
import json
import random
from typing import Callable
from logger import Logging
from prompt import Prompt
from utility import extract_json


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

    @property
    def brain(self):
        return self.brain_

    @brain.setter
    def brain(self, brain):
        self.brain_ = brain

    def accept_hands(self, hands: list):
        '''Accepts the initial hands for the player.'''
        self.hand_ = hands

    @property
    def hand(self):
        return self.hand_

    def append_landlord_cards(self, cards: list):
        '''Appends the landlord cards to the player's hand.'''
        self.hand_.extend(cards)
        self.is_landlord_ = True

    async def landlord_bidding(self, bidding_history: list):
        '''Makes a bidding decision for the player.'''
        Logging(f"{self.name} is making a bidding decision.")

        Logging(
            f"User prompts: {Prompt().get_bidding_prompt(bidding_history=bidding_history,
                                                         card_combination=self.hand_)}")
        result = await self.brain_([
            {
                "role": "system",
                "content": Prompt().get_system_prompt()
            },
            {

                "role": "user",
                "content": Prompt().get_bidding_prompt(bidding_history=bidding_history,
                                                       card_combination=self.hand_)
            }
        ])

        Logging(f"current brain is: {self.brain_}")
        Logging(f"{self.name} bidding result: {result} \n")

        extracted_json = extract_json(result.strip())
        if extracted_json is None:
            raise ValueError("Failed to extract JSON from result.")
        Logging(f"extracted json string is: {extracted_json}")
        json_result = json.loads(extracted_json)
        Logging(f"After parsing the bidding result: {json_result}")
        final_bid = json_result["action"]

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
