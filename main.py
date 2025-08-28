
# A game emulator for Doudizhu (Chinese Poker)
import asyncio
# from play_engine import Doudizhu
# from logger import Logging
from play_engine import Doudizhu


async def main():
    '''Main entry point for the Doudizhu game.'''
    await Doudizhu().run()


if __name__ == "__main__":
    asyncio.run(main())
