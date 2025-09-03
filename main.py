# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=consider-using-f-string
import asyncio
from play_engine import Doudizhu
from ai_models import llama_3_3, deepseek_r1t_chimera, gemini_2_5_flash
from player import Player
from logger import Logging


async def main():
    Logging("Starting Doudizhu Game Emulator")
    game = Doudizhu()

    # Player setup
    for i, brain in enumerate([llama_3_3, deepseek_r1t_chimera, gemini_2_5_flash]):
        player = Player(f"Player {i + 1}")
        player.brain = brain
        player.idx = i  # Must have unique index for each player
        game.player_join(player)

    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
