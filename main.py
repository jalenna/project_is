from src.brain.brain import Brain, BrainPlayingBot


def main() -> int:
    """Main application entry point.

    Arguments:
        None

    Returns:
        int: Exit code
    """

    brain: Brain = Brain()
    brain.run_all()
    # brain.load_model()
    # brain.load_weights()

    return 0


# main()

from src.utils.training_bots import RdeepBot, RandBot
from schnapsen.bots.gui.guibot import SchnapsenServer
import random
from schnapsen.game import SchnapsenGamePlayEngine
from src.utils.CONSTANTS import SEED

myrepeats = 10

bot1 = BrainPlayingBot(name="BrainBot")
bot2 = RandBot(rand=random.Random(SEED), name="RandBot")

bot3 = RdeepBot(10, 6, random.Random(SEED), "RDeep")

engine = SchnapsenGamePlayEngine()

is_human: bool = True

if is_human:
    with SchnapsenServer() as s:
        # Play 25 matches for each
        # RandBot
        # Follower first
        bot1 = RandBot(random.Random(SEED))
        bot2 = s.make_gui_bot(name="Human")
        engine.play_game(bot1, bot2, random.Random(SEED))
        # Exit
        # # Leader first
        # bot2 = RandBot(random.Random(SEED))
        # bot1 = s.make_gui_bot(name="Human")
        # engine.play_game(bot1, bot2, random.Random(SEED))
        # # Exit
        # # RdeepBot
        # # Follower first
        # bot1 = bot3
        # bot2 = s.make_gui_bot(name="Human")
        # engine.play_game(bot1, bot2, random.Random(SEED))
        # # Exit
        # # Leader first
        # bot2 = bot3
        # bot1 = s.make_gui_bot(name="Human")
        # engine.play_game(bot1, bot2, random.Random(SEED))
        # # Exit
else:
    bots = [bot1, bot2, bot3]
    n = len(bots)
    wins = {str(bot): 0 for bot in bots}
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n * n - n) / 2 * myrepeats
    playedgames = 0

    print("Playing {} games:".format(int(totalgames)))
    for a, b in matches:
        for r in range(myrepeats):
            if random.choice([True, False]):
                p = [a, b]
            else:
                p = [b, a]

            winner_id, game_points, score = engine.play_game(
                bots[p[0]], bots[p[1]], random.Random(SEED)
            )

            wins[str(winner_id)] += game_points

            playedgames += 1
            print(
                "Played {} out of {:.0f} games ({:.0f}%): {} \r".format(
                    playedgames, totalgames, playedgames / float(totalgames) * 100, wins
                )
            )
