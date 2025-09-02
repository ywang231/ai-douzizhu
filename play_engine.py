# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring
# pylint: disable=too-many-instance-attributes

import random
from player import Player
from logger import Logging


class Doudizhu:
    players_: list[Player]
    curr_idx_: int  # The index of the current player in turn
    cards_played_: list
    is_start_: bool
    deck_: list
    first_idx_: int
    potential_idx_: int
    bid_score_: int
    # Record the bidding history, (play_id, bid_score/pass - score / pass)
    # If player bids, record the score, if passes, record 0
    bidding_history_: list[tuple[int, int]]

    def __init__(self):
        self._reset_game()

    # Set up the initial game state or reset the game states to the initial values
    def _reset_game(self):
        self.curr_idx_ = -1  # No player is selected to start bidding
        self.cards_played_ = []  # No cards have been played yet
        self.is_start_ = False
        self.deck_ = []
        self.first_idx_ = -1
        self.potential_idx_ = -1
        self.bid_score_ = 0
        self.bidding_history_ = []
        self.players_ = []

    def player_join(self, player: Player):
        Logging(f"Player {player.name} joined the game.")
        self.players_.append(player)
        Logging(f"Current players: {[p.name for p in self.players_]}")

    async def _landlord_bidding(self):
        assert len(self.players_) == 3, "There must be exactly 3 players."
        # Random pick a player to start biding processing
        self.curr_idx_ = random.randint(0, len(self.players_) - 1)
        self.first_idx_ = self.curr_idx_

        Logging('Bidding started\n')

        MAX_BID_SCORE_OF_FIRST_ROUND = 3
        for idx in range(self.curr_idx_, self.curr_idx_ + len(self.players_)):

            self.curr_idx_ = idx % len(self.players_)
            curr_player = self.players_[self.curr_idx_]

            # Get the bidding result from the current player
            bid_res = await curr_player.landlord_bidding(bidding_history=self.bidding_history_)
            # Record the bidding history
            self.bidding_history_.append((self.curr_idx_, bid_res))

            # If someone bids or someone give the maximum bidding score
            if bid_res > 0 or bid_res >= MAX_BID_SCORE_OF_FIRST_ROUND:
                self.potential_idx_ = self.curr_idx_
                self.bid_score_ = bid_res
                # If the bid reaches the maximum score, end the bidding
                if bid_res >= MAX_BID_SCORE_OF_FIRST_ROUND:
                    break

        # Someone bade, and it's not the first player
        if self.potential_idx_ not in (-1, self.first_idx_):
            final = await self.players_[self.first_idx_].final_double_bid(self.bid_score_ * 2)
            self.bidding_history_.append((self.first_idx_, final))
            if final > 0:
                self.potential_idx_ = self.first_idx_
                self.bid_score_ = final

        if self.potential_idx_ != -1:
            Logging(
                f"Final landlord is {self.players_[self.potential_idx_].name}")
        else:
            Logging("No one bid, re-deal the cards and restart bidding")

        Logging("Bidding END")

    async def _start_game(self):
        '''Starts the Doudizhu game.'''
        self.is_start_ = True
        self.deck_ = self.create_deck()
        self._shuffle_and_deal()
        await self._landlord_bidding()

    def _shuffle_and_deal(self):
        '''Shuffles and deals the cards to players.'''
        random.shuffle(self.deck_)
        # Each player gets 17 cards, 3 are left as the "landlord" cards
        for player in self.players_:
            player.accept_hands(self.deck_[0:17])
            self.deck_ = self.deck_[17:]

        # Print hand each player has
        for player in self.players_:
            Logging(f"{player.name} hands: {player.hand}")
        # Print the three landlord cards
        Logging(f"Landlord cards: {self.deck_}")

    @staticmethod
    def create_deck():
        '''
        Return a new deck of cards.
        each card is represented as a tuple (face, rank, suit)
        '''
        suits = [0, 1, 2, 3]  # '♠', '♥', '♣', '♦'
        faces = ['3', '4', '5', '6', '7',
                 '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        ranks = {rank: i for i, rank in enumerate(faces)}
        deck = [(rank, suit, ranks[rank])
                for suit in suits for rank in ranks]

        # add jokers
        deck.append(("Black Joker", -1, len(ranks)))  # Black Joker
        deck.append(("Red Joker", -1, len(ranks) + 1))  # Red Joker

        return deck

    # The main entry point to run the game
    async def run(self):
        if not self.is_start_:
            await self._start_game()


if __name__ == "__main__":
    Logging("Game started")
    Logging(Doudizhu.create_deck())

    # asyncio.run(Doudizhu().run())
