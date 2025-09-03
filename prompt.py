# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long

# from player import Player
from logger import Logging


class Prompt:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            print("Creating Prompt instance")
            cls._instance = super(Prompt, cls).__new__(cls)
        return cls._instance

    def get_system_prompt(self):
        return (
            "You are playing a popular Chinese poker card game called “斗地主”. Your response must have to be in JSON format. No explanations, comments, or extra text. The rules are as follows:\n"
            "1. Basics\n"
            "   • Deck: 54 cards (52 standard cards + 2 jokers).\n"
            "   • Players: 3 players.\n"
            "   • Roles: 1 Landlord vs. 2 Farmers (farmers cooperate against landlord).\n"
            "   • Win condition:\n"
            "     - Landlord wins if the landlord plays all cards first.\n"
            "     - Farmers win if either farmer plays all cards first.\n\n"
            "2. Dealing & Bidding\n"
            "   • Each player is dealt 17 cards. The remaining 3 cards are set aside as the landlord's bottom cards.\n"
            "   • Bidding for landlord:\n"
            "     1. A random player starts with 1 point and decides to 'Bid' or 'Pass'.\n"
            "        The first can get the landlord role by bidding 3 points (the maximum points).\n"
            "     2. If 'Bid' with a lower than 3 points, it temporarily becomes the landlord; the next player can bid higher or pass. If 'Pass', the next player decides and so on.\n"
            "     3. During the first round, if all players pass, the cards are reshuffled and redealt.\n"
            "     4. After a round of bidding ends, if the highest bid is not the first player, the first player still has the final chance to get the landlord role by double the current highest bidding points.\n"
            "In this case, if the first player choose to pass, the previous highest bidder gets the landlord role. bidding phase ends.\n"
            "     5. Once a landlord is confirmed, they take the 3 bottom cards and start the game.\n\n"
            "3. Card Combinations\n"
            "   The valid combinations are:\n"
            "   3.1 Single: Any single card. Example: 3, J, Red Joker.\n"
            "   3.2 Pair: Two cards of the same rank. Example: (5,5), (K,K).\n"
            "   3.3 Triple: Three cards of the same rank. Example: (7,7,7).\n"
            "   3.4 Triple with Single / Triple with Pair: Three cards of the same rank + one single or one pair. Example: (7,7,7)+(9), (8,8,8)+(4,4).\n"
            "   3.5 Straight: At least five consecutive cards (cannot include 2 or jokers). Example: (4,5,6,7,8), (9,10,J,Q,K).\n"
            "   3.6 Double Sequence: Three or more consecutive pairs (cannot include 2 or jokers). Example: (3,3,4,4,5,5), (7,7,8,8,9,9,10,10).\n"
            "   3.7 Plane (Airplane): Two or more consecutive triples (cannot include 2 or jokers), optionally with the same number of singles or pairs as “wings.” Example: (3,3,3)(4,4,4)+(5,5), (6,6,6)(7,7,7)(8,8,8)+(4,4)(5,5)(6,6).\n"
            "   3.8 Four with Two: Four cards of the same rank + two singles or two pairs. Example: (9,9,9,9)+(5,6), (J,J,J,J)+(4,4)(5,5).\n"
            "   3.9 Bomb: Four of a kind. Example: (4,4,4,4), (A,A,A,A).\n"
            "   3.10 Joker Bomb: Both jokers together. Highest combination in the game.\n\n"
            "4. Playing Rules\n"
            "   1. The landlord plays first, then play goes clockwise.\n"
            "   2. On each turn, a player can:\n"
            "      • Play a higher combination of the same type.\n"
            "      • Pass, skipping their turn.\n"
            "   3. Bombs and Joker Bombs can beat any combination.\n"
            "   4. When two players pass, the round resets, and the last successful player can play any valid combination again.\n\n"
            "5. Card Ranking\n"
            "   • Ranking: Joker (Red > Black) > 2 > A > K > ... > 3.\n"
            "   • For pairs, triples, straights, etc., only the rank matters; suits are irrelevant.\n"
            "   • Bombs beat everything except Joker Bombs.\n"
            "   • Joker Bomb is unbeatable.\n\n"
            "6. Winning & Scoring\n"
            "   • Landlord wins if they finish its cards first.\n"
            "   • Farmers win if either farmer finishes first.\n"
            "   • Scoring (common in online versions):\n"
            "     - Each time when Bomb/Joker Bomb is played, it doubles the base points.\n"
            "     - If the landlord wins, it gets the double points of the base points."
            " 		- if the farmer wins, each farmer gets the base points."
            "7. Card Representation\n"
            "   • Each card is represented as a tuple of (face,suit, rank).\n"
            "   • Suits are represented as ints: 0, 1, 2, 3 for 'Hearts', 'Diamonds', 'Clubs', 'Spades'.\n"
            "   • Jokers are represented as (-1, 'Black Joker', 14) for the red joker and (-1, 'Red Joker', 15) for the black joker.\n"
            "   • Example: (3, 'Hearts', 3), (13, 'Spades', 14).\n"
            "   • Ranking is from 3 to 15 (face 3 is the lowest(0) , Red Joker is the highest(15)).\n\n"
            "   • The ranking is used to compare cards during gameplay. The higher the rank, the stronger the card.\n"
            "8. Strategy Tips\n"
            "   • During bidding phase, if you think your cards are good, becoming the landlord can help you get more points if winning the games.\n"
            "   • Becoming landlord takes more risk, if lose, lose more points, if win, gain more points.\n"
            "   • For the farmers, cooperating and communicating with each other is key to defeating the landlord.\n"
            "   • During playing the cards, using bombs and joker bombs strategically can turn the tide of the game and get more points if win, lose more if lose\n"
            "   • Farmers should work together to beat the landlord, using their cards strategically.\n"
        )

    def get_bidding_prompt(self, bidding_history: list, card_combination: list[tuple[str, int, int]]) -> str:
        bprompt = "You are current in landlord bidding phase.\n"
        if not bidding_history:
            bprompt += "It is your turn to bid and you are the first bidder.\n"
        else:
            bprompt += f"You are the {len(bidding_history) + 1} bidder.\n"
            bprompt += f"The current highest bid is {bidding_history[-1][1]} points.\n"
        bprompt += f"Your cards are: {card_combination}\n"
        bprompt += "Based on the information given above, you are giving your decision. \n"
        bprompt += "The response must be a raw JSON object, start with '{' and end with '}'. nothing else.\n"
        bprompt += "The example response is given below for your reference:\n"
        bprompt += '{ "action": 0, "reason": "How you made the action?" }\n'
        bprompt += "The JSON response has to include the 'action' and 'reason' fields.\n"
        bprompt += "The 'action' field can only be 0, 1, 2, or 3. 0 means you want to pass, 1 means you want to bid 1 point, and so on.\n"
        bprompt += "The 'reason' field includes the details of your decision-making process in a few sentences.\n"

        return bprompt

    def get_doubling_prompt(self, bidding_history: list, card_combination: list[tuple[str, int, int]]) -> str:
        bprompt = "You are currently in the final landlord bidding phase.\n"
        bprompt += f"The current highest bid is {bidding_history[-1][1]} points.\n"
        bprompt += "You can only bid with double points of current highest bid or pass.\n"
        bprompt += f"Your cards are: {card_combination}\n"
        bprompt += "Based on the information given above, you are giving your decision. \n"
        bprompt += "Your response has to be in JSON format. The example response is given below for your reference:\n"
        bprompt += '{ "action": 0, "reason": "How you made the action?" }\n'
        bprompt += "Your response has to include the 'action' and 'reason' fields.\n"
        bprompt += f"The 'action' field can only be 0 or {bidding_history[-1][1] * 2}. 0 means you want to pass, otherwise you want to bid with double the current highest bid.\n"
        bprompt += "The 'reason' field should explain your decision-making process in a few sentences.\n"
        return bprompt

    def assembly_prompt(self, user_prompt: str, system_prompt: str, assistant_data: str = "") -> list:
        return [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": assistant_data}]

    # euWarningignore
    def history_prompt(self, player_idx: int, players: list, history_bid: list, history_played: list) -> str:
        prompt = "Here is the history of the landlord bidding:\n"

        for idx, bidding in enumerate(history_bid):
            if bidding[1] > 0:
                prompt += f"Round {idx + 1}: {'You' if player_idx == bidding[0] else players[bidding[0]].name} bid {bidding[1]} points.\n"
            else:
                prompt += f"Round {idx + 1}: {'You' if player_idx == bidding[0] else players[bidding[0]].name} passed.\n"

        if len(history_played) == 0:
            return prompt

        prompt += "Here is the history of played cards of each round:\n"
        # History of played cards
        for idx, play in enumerate(history_played):
            prompt += f"Round {idx + 1}: {'You' if player_idx == play[0] else players[play[0]].name} played {play[1]}.\n"
        return prompt


if __name__ == "__main__":
    # Logging(Prompt().get_system_prompt())
    # Logging(Prompt().get_bidding_prompt(
    #     [], [('3', 0, 0), ('3', 1, 0), ('3', 2, 0)]))

    Logging(Prompt().history_prompt(0, ['Player 1', 'Player 2', 'Player 3'],
                                    [('3', 0, 0), ('3', 1, 0), ('3', 2, 0)], [('3', 0, 0), ('3', 1, 0), ('3', 2, 0)]))
