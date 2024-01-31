# Gameplay related code for gathering logs

from src.brain.brain import BrainPlayingBot
from src.utils.training_bots import RdeepBot, RandBot
from schnapsen.bots.gui.guibot import SchnapsenServer
import random
from schnapsen.game import SchnapsenGamePlayEngine
from src.utils.CONSTANTS import GLOBAL_SETTINGS

SETTINGS: GLOBAL_SETTINGS = GLOBAL_SETTINGS()


def play_games(nr_matches: int):
    """Helper function to play the required games for research."""

    myrepeats = nr_matches

    bot1 = BrainPlayingBot(name="BrainBot")
    bot2 = RandBot(rand=random.Random(SETTINGS.SEED), name="RandBot")
    bot3 = RdeepBot(10, 6, random.Random(SETTINGS.SEED), "RDeep")

    engine = SchnapsenGamePlayEngine()

    is_playing_human: bool = False
    is_playing_bot: bool = True

    if is_playing_human:
        with SchnapsenServer() as s:
            # Play 75 matches for each
            # RandBot
            # Follower first
            bot1 = RandBot(random.Random(SETTINGS.SEED))
            bot2 = s.make_gui_bot(name="Human")
            engine.play_game(bot1, bot2, random.Random(SETTINGS.SEED))
            #
            # # Leader first
            # bot2 = RandBot(random.Random(SEED))
            # bot1 = s.make_gui_bot(name="Human")
            # engine.play_game(bot1, bot2, random.Random(SEED))
            #
            # # RdeepBot
            # # Follower first
            # bot1 = bot3
            # bot2 = s.make_gui_bot(name="Human")
            # engine.play_game(bot1, bot2, random.Random(SEED))
            #
            # # Leader first
            # bot2 = bot3
            # bot1 = s.make_gui_bot(name="Human")
            # engine.play_game(bot1, bot2, random.Random(SEED))
    elif is_playing_bot:
        playedgames: int = 0

        # Brainbot starts as the leader
        bot_order = [0, 1, 2]
        bots = [bot1, bot2, bot3]

        engine = SchnapsenGamePlayEngine()

        while playedgames < myrepeats // 2:
            engine.play_game(
                bots[bot_order[0]], bots[bot_order[1]], random.Random(SETTINGS.SEED)
            )

            bot2.to_log()

            print(
                "Played {} out of {:.0f} games | Seed used: {}".format(
                    playedgames,
                    myrepeats // 2,
                    SETTINGS.SEED,
                ),
                end="\r",
            )

            if playedgames > 0 and playedgames % 75 == 0:
                SETTINGS.SEED += 1
                bot2.update_seed(SETTINGS.SEED)

                # Start as a follower now
                bot_order[0], bot_order[1] = bot_order[1], bot_order[0]

            playedgames += 1

        # Switch them back to their original positions
        bot_order[0], bot_order[1] = bot_order[1], bot_order[0]

        # Flush the screen
        print("                                                       ", end="\r")

        playedgames = 0

        while playedgames < myrepeats // 2:
            engine.play_game(
                bots[bot_order[0]], bots[bot_order[2]], random.Random(SETTINGS.SEED)
            )

            bot3.to_log()

            print(
                "Played {} out of {:.0f} games | Seed used: {}".format(
                    playedgames,
                    myrepeats // 2,
                    SETTINGS.SEED,
                ),
                end="\r",
            )

            if playedgames > 0 and playedgames % 75 == 0:
                SETTINGS.SEED += 1
                bot3.update_seed(SETTINGS.SEED)

                # Start as the follower now
                bot_order[0], bot_order[2] = bot_order[2], bot_order[0]

            playedgames += 1

        # For completeness swap them back _--(-_-)__-
        bot_order[0], bot_order[2] = bot_order[2], bot_order[0]
