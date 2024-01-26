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

    return 0


main()

from schnapsen.bots import RdeepBot, RandBot, example_bot
import random
from schnapsen.game import SchnapsenGamePlayEngine

myrepeats = 10

bot1 = BrainPlayingBot(name="BrainBot")
bot2 = RandBot(rand=random.Random(45), name="RandBot")
# bot2 = example_bot.ExampleBot(name="ExBot")
bot3 = RdeepBot(10, 6, random.Random(46), "RDeep")

engine = SchnapsenGamePlayEngine()

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
            bots[p[0]], bots[p[1]], random.Random(45)
        )

        wins[str(winner_id)] += game_points

        playedgames += 1
        print(
            "Played {} out of {:.0f} games ({:.0f}%): {} \r".format(
                playedgames, totalgames, playedgames / float(totalgames) * 100, wins
            )
        )
