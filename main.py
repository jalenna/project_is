from src.brain.brain import Brain, BrainPlayingBot

# Change settings in src.utils.CONSTANTS.py


def test_brain() -> int:
    """Run methods/tests for the brain.

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


# Comment this file if you don't want to train the brain
# test_brain()

# Gameplay related code for gathering logs

from src.utils.training_bots import RdeepBot, RandBot
from schnapsen.bots.gui.guibot import SchnapsenServer
import random
from schnapsen.game import SchnapsenGamePlayEngine
from src.utils.CONSTANTS import GLOBAL_SETTINGS

SETTINGS: GLOBAL_SETTINGS = GLOBAL_SETTINGS()

myrepeats = 300

bot1 = BrainPlayingBot(name="BrainBot")
bot2 = RandBot(rand=random.Random(SETTINGS.SEED), name="RandBot")
bot3 = RdeepBot(10, 6, random.Random(SETTINGS.SEED), "RDeep")

engine = SchnapsenGamePlayEngine()

is_human: bool = True
is_bot: bool = True

is_playing_human: bool = False
is_playing_bot: bool = False

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

    while playedgames < myrepeats // 2:
        engine = SchnapsenGamePlayEngine()
        winner_id, game_points, score = engine.play_game(
            bot1, bot2, random.Random(SETTINGS.SEED)
        )

        bot2.to_log()

        print(SETTINGS.SEED)
        print("Played {} out of {:.0f} games \r".format(playedgames, myrepeats // 2))

        if playedgames > 0 and playedgames % 75 == 0:
            SETTINGS.SEED += 1
            bot2.update_seed(SETTINGS.SEED)

        playedgames += 1

    playedgames = 0

    while playedgames < myrepeats // 2:
        engine = SchnapsenGamePlayEngine()
        winner_id, game_points, score = engine.play_game(
            bot1, bot3, random.Random(SETTINGS.SEED)
        )

        bot3.to_log()

        print(SETTINGS.SEED)
        print("Played {} out of {:.0f} games \r".format(playedgames, myrepeats // 2))

        if playedgames > 0 and playedgames % 25 == 0:
            SETTINGS.SEED += 1
            bot3.update_seed(SETTINGS.SEED)

        playedgames += 1

# Format logs

import os


def logs_parser(line: str) -> list[int]:
    return [
        int(number)
        for number in line[len("YYYY-MM-DD HH:MM:SS: ") + len(bot_name) + len(" - ") :]
        .strip()
        .removesuffix("]")
        .removeprefix("[")
        .split(",")
    ]


matches: list[dict[str, dict[int, list[list[list[int] | bool]]]]] = []

if is_human:
    log_file_paths: list[str] = os.listdir(SETTINGS._HUMAN_LOGS_FILE_PATH)

    # Key: bot name, value -> Key: seed, value -> The match information, ending with a win or loss
    matches.append({})

    for log_file_name in log_file_paths:
        full_path: str = os.path.join(SETTINGS._HUMAN_LOGS_FILE_PATH, log_file_name)

        # Simple error check
        if os.path.isfile(full_path):
            if log_file_name.endswith(".txt"):
                with open(full_path) as log_file:
                    lines: list[str] = log_file.readlines()

                    seed_used: int = int(lines[0][len("SEED USED:") :].strip())
                    bot_name: str = lines[1][21:].split("-")[0].strip()

                    points_per_round: list[int] = logs_parser(lines[1])
                    move_types_per_round: list[int] = logs_parser(lines[2])
                    leader_rate: list[int] = logs_parser(lines[3])
                    lead_rate: list[int] = logs_parser(lines[4])
                    has_won_str: str = lines[5].strip()
                    has_won_str = has_won_str[len(has_won_str) - 5 :].strip()
                    has_won: bool = True if has_won_str == "True" else False

                    match_bot = matches[0].get(bot_name, {})
                    if len(match_bot):
                        match_info = match_bot.get(seed_used, [])
                        if len(match_info):
                            match_info.append(
                                [
                                    points_per_round,
                                    move_types_per_round,
                                    leader_rate,
                                    lead_rate,
                                    has_won,
                                ]
                            )
                        else:
                            match_bot[seed_used] = [
                                [
                                    points_per_round,
                                    move_types_per_round,
                                    leader_rate,
                                    lead_rate,
                                    has_won,
                                ]
                            ]
                    else:
                        matches[0][bot_name] = {
                            seed_used: [
                                [
                                    points_per_round,
                                    move_types_per_round,
                                    leader_rate,
                                    lead_rate,
                                    has_won,
                                ]
                            ]
                        }

if is_bot:
    log_file_name = os.listdir(SETTINGS._ML_LOGS_FILE_PATH)[-1]

    full_path: str = os.path.join(SETTINGS._ML_LOGS_FILE_PATH, log_file_name)

    if len(matches) < 2:
        matches.append({})
        matches.append({})

    # Simple error check
    if os.path.isfile(full_path):
        if log_file_name.endswith(".txt"):
            with open(full_path) as log_file:
                all_lines: list[str] = log_file.readlines()
                line_counter: int = 0

                while line_counter < len(all_lines):
                    lines = all_lines[line_counter:]

                    seed_used: int = int(lines[0][len("SEED USED:") :].strip())
                    bot_name: str = lines[3][21:].split("-")[0].strip()

                    points_per_round: list[int] = logs_parser(lines[3])
                    move_types_per_round: list[int] = logs_parser(lines[4])
                    leader_rate: list[int] = logs_parser(lines[5])
                    lead_rate: list[int] = logs_parser(lines[6])
                    has_won_str: str = lines[7].strip()
                    has_won_str = has_won_str[len(has_won_str) - 5 :].strip()
                    has_won: bool = True if has_won_str == "True" else False

                    match_bot = matches[1].get(bot_name, {})
                    if len(match_bot):
                        match_info = match_bot.get(seed_used, [])
                        if len(match_info):
                            match_info.append(
                                [
                                    points_per_round,
                                    move_types_per_round,
                                    leader_rate,
                                    lead_rate,
                                    has_won,
                                ]
                            )
                        else:
                            match_bot[seed_used] = [
                                [
                                    points_per_round,
                                    move_types_per_round,
                                    leader_rate,
                                    lead_rate,
                                    has_won,
                                ]
                            ]
                    else:
                        matches[1][bot_name] = {
                            seed_used: [
                                [
                                    points_per_round,
                                    move_types_per_round,
                                    leader_rate,
                                    lead_rate,
                                    has_won,
                                ]
                            ]
                        }
                    line_counter += 8


# Display logs

import matplotlib.pyplot as plt
import numpy as np

# We plot for each seed separately


def plot_avg_ppr(was_human: bool, bot_name: str) -> None:
    """Plots the average number of points per round."""

    avg_results: list[float] = []
    nr_tricks: dict[int, int] = {}
    max_trick: int = 0

    match_idx: int = 0 if was_human else 1

    for _, match_info in matches[match_idx].get(bot_name, {}).items():
        for match in match_info:
            for trick, point in enumerate(match[0]):
                if max_trick <= trick:
                    max_trick = trick

                nr_tricks[trick] = nr_tricks.get(trick, 0) + 1
                # If this number of trick(s) isn't yet in the list
                if len(avg_results) <= trick:
                    avg_results.append(point)
                else:
                    avg_results[trick] += point

    for idx in range(max_trick):
        avg_results[idx] = avg_results[idx] / nr_tricks[idx]

    plt.plot(
        np.arange(len(avg_results)),
        avg_results,
        label="points",
        color="orange",
    )

    # Add labels and title
    plt.xlabel("Number of tricks")
    plt.ylabel("Number of points")
    plt.title(
        f"{'Human'if was_human else 'Bot'} | {bot_name} | Average points per round"
    )

    # Add a legend
    plt.legend()

    plt.show()


def print_avg_mtpr(was_human: bool, bot_name: str) -> None:
    """Plots the average number of move types per round."""

    match_idx: int = 0 if was_human else 1

    avg_results: dict[int, float] = {
        0: 0.0,
        1: 0.0,
        2: 0.0,
    }

    nr_rounds: int = 0

    for _, match_info in matches[match_idx].get(bot_name, {}).items():
        nr_rounds += len(match_info)

        avg_results[0] += sum(match[1].count(0) for match in match_info)
        avg_results[1] += sum(match[1].count(1) for match in match_info)
        avg_results[2] += sum(match[1].count(2) for match in match_info)

    avg_results[0] = avg_results.get(0, 0) / nr_rounds
    avg_results[1] = avg_results.get(1, 0) / nr_rounds
    avg_results[2] = avg_results.get(2, 0) / nr_rounds

    print("Average number of regular moves per round:", round(avg_results.get(0, 0), 3))
    print(
        "Average number of trump exchange moves per round:",
        round(avg_results.get(1, 0), 3),
    )
    print(
        "Average number of marriage moves per round:", round(avg_results.get(2, 0), 3)
    )


def plot_avg_leader_rates(was_human: bool, bot_name: str) -> None:
    """Plots the average number of times you were a leader in a round."""

    match_idx: int = 0 if was_human else 1

    avg_results: list[float] = []
    nr_tricks: dict[int, int] = {}
    max_trick: int = 0

    for _, match_info in matches[match_idx].get(bot_name, {}).items():
        for match in match_info:
            for trick, point in enumerate(match[2]):
                if max_trick <= trick:
                    max_trick = trick

                nr_tricks[trick] = nr_tricks.get(trick, 0) + 1
                # If this number of trick(s) isn't yet in the list
                if len(avg_results) <= trick:
                    avg_results.append(point)
                else:
                    avg_results[trick] += point

    # Average their points
    for idx in range(max_trick):
        avg_results[idx] = avg_results[idx] / nr_tricks[idx]

    plt.plot(
        np.arange(len(avg_results)),
        avg_results,
        label="Player",
        color="green",
    )

    # Add labels and title
    plt.xlabel("Number of tricks")
    plt.ylabel("Leader rate")
    plt.title(
        f"{'Human'if was_human else 'Bot'} | {bot_name} | Average number of times you were leader per trick."
    )

    # Add a legend
    plt.legend()

    plt.show()


def plot_avg_lead_rates(was_human: bool, bot_name: str) -> None:
    """Plots the average number of times you were in the lead per trick."""

    match_idx: int = 0 if was_human else 1

    avg_results: list[float] = []
    nr_tricks: dict[int, int] = {}
    max_trick: int = 0

    for _, match_info in matches[match_idx].get(bot_name, {}).items():
        nr_tricks: dict[int, int] = {}

        for match in match_info:
            for trick, point in enumerate(match[3]):
                if max_trick <= trick:
                    max_trick = trick

                nr_tricks[trick] = nr_tricks.get(trick, 0) + 1
                # If this number of trick(s) isn't yet in the list
                if len(avg_results) <= trick:
                    avg_results.append(point)
                else:
                    avg_results[trick] += point

    # Average their points
    for idx in range(max_trick):
        avg_results[idx] = avg_results[idx] / nr_tricks[idx]

    plt.plot(
        np.arange(len(avg_results)),
        avg_results,
        label="Player",
        color="blue",
    )

    # Add labels and title
    plt.xlabel("Number of tricks")
    plt.ylabel("Lead rate")
    plt.title(
        f"{'Human'if was_human else 'Bot'} | {bot_name} | Average number of times you were in the lead per trick."
    )

    # Add a legend
    plt.legend()

    plt.show()


def print_avg_win_ratio(was_human: bool, bot_name: str) -> None:
    """Prints the average win ratio."""

    match_idx: int = 0 if was_human else 1

    avg_win: float = 0
    avg_loss: float = 0
    nr_matches: int = 0

    for _, match_info in matches[match_idx].get(bot_name, {}).items():
        nr_matches += len(match_info)

        avg_win += sum(1 for match in match_info if match[4])
        avg_loss += sum(1 for match in match_info if not match[4])

    avg_win /= nr_matches
    avg_loss /= nr_matches

    print("Average win rate:", round(avg_win, 3))
    print("Average loss rate:", round(avg_loss, 3))


if is_human:
    # Printing

    # Randbot
    print("#-----------------Stats Against Randbot-----------------#")
    print_avg_win_ratio(is_human, "rand")
    print_avg_mtpr(is_human, "rand")

    print()

    # Rdeep
    print("#-----------------Stats Against Rdeep-------------------#")
    print_avg_win_ratio(is_human, "rdeep")
    print_avg_mtpr(is_human, "rdeep")

    # Plotting

    # Randbot
    plot_avg_ppr(is_human, "rand")
    plot_avg_leader_rates(is_human, "rand")
    plot_avg_lead_rates(is_human, "rand")

    # Rdeep
    plot_avg_ppr(is_human, "rdeep")
    plot_avg_leader_rates(is_human, "rdeep")
    plot_avg_lead_rates(is_human, "rdeep")

    print()

if is_bot:
    # Printing

    # Randbot
    print("#-----------------Stats Against Randbot-----------------#")
    print_avg_win_ratio(False, "rand")
    print_avg_mtpr(False, "rand")

    print()

    # Rdeep
    print("#-----------------Stats Against Rdeep-------------------#")
    print_avg_win_ratio(False, "rdeep")
    print_avg_mtpr(False, "rdeep")

    # Plotting

    # Randbot
    plot_avg_ppr(False, "rand")
    plot_avg_leader_rates(False, "rand")
    plot_avg_lead_rates(False, "rand")

    # Rdeep
    plot_avg_ppr(False, "rdeep")
    plot_avg_leader_rates(False, "rdeep")
    plot_avg_lead_rates(False, "rdeep")

    print()
