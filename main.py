from src.brain.brain import Brain, BrainPlayingBot
from src.utils.CONSTANTS import GLOBAL_SETTINGS

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


# Comment this line if you don't want to train the brain
# test_brain()

# Comment these lines if you don't want to play games and already have log files to test on
# from src.utils.play_games import play_games

# play_games(300)

# Format logs

import os

SETTINGS: GLOBAL_SETTINGS = GLOBAL_SETTINGS()


def logs_parser(line: str, bot_name: str) -> list[int]:
    return [
        int(number)
        for number in line[len("YYYY-MM-DD HH:MM:SS: ") + len(bot_name) + len(" - ") :]
        .strip()
        .removesuffix("]")
        .removeprefix("[")
        .split(",")
    ]


# Key: bot name, value -> Key: seed, value -> The match information, ending with a win or loss
matches: list[dict[str, dict[int, list[list[list[int] | bool]]]]] = [{}, {}]


def file_to_match_dict(log_file, is_bot: bool) -> None:
    """Formats the provided log file into a dictionary."""

    global matches

    line_indeces: dict[str, int]

    if is_bot:
        line_indeces = {
            "ppr": 3,
            "mtpr": 4,
            "lr": 5,
            "ldr": 6,
            "w": 7,
        }
    else:
        line_indeces = {
            "ppr": 1,
            "mtpr": 2,
            "lr": 3,
            "ldr": 4,
            "w": 5,
        }

    all_lines: list[str] = log_file.readlines()
    line_counter: int = 0

    # Line counter is only relevant to the bot's log file
    while line_counter < len(all_lines):
        lines = all_lines[line_counter:]

        seed_used: int = int(lines[0][len("SEED USED:") :].strip())
        bot_name: str = lines[line_indeces["ppr"]][21:].split("-")[0].strip()

        points_per_round: list[int] = logs_parser(lines[line_indeces["ppr"]], bot_name)

        move_types_per_round: list[int] = logs_parser(
            lines[line_indeces["mtpr"]], bot_name
        )
        leader_rate: list[int] = logs_parser(lines[line_indeces["lr"]], bot_name)
        lead_rate: list[int] = logs_parser(lines[line_indeces["ldr"]], bot_name)
        has_won_str: str = lines[line_indeces["w"]].strip()
        has_won_str = has_won_str[len(has_won_str) - 5 :].strip()
        has_won: bool = True if has_won_str == "True" else False

        bot_idx: int = 0

        if is_bot:
            bot_idx = 1

        match_bot = matches[bot_idx].get(bot_name, {})

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
            matches[bot_idx][bot_name] = {
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


is_human: bool = True
is_bot: bool = True

if is_human:
    log_file_paths: list[str] = os.listdir(SETTINGS.HUMAN_LOGS_FILE_PATH)

    for log_file_name in log_file_paths:
        full_path: str = os.path.join(SETTINGS.HUMAN_LOGS_FILE_PATH, log_file_name)

        # Simple error check
        if os.path.isfile(full_path):
            if log_file_name.endswith(".txt"):
                with open(full_path) as log_file:
                    file_to_match_dict(log_file, False)

if is_bot:
    log_file_name = os.listdir(SETTINGS.ML_LOGS_FILE_PATH)[-1]

    full_path: str = os.path.join(SETTINGS.ML_LOGS_FILE_PATH, log_file_name)

    # Simple error check
    if os.path.isfile(full_path):
        if log_file_name.endswith(".txt"):
            with open(full_path) as log_file:
                file_to_match_dict(log_file, True)

# Display logs

import matplotlib.pyplot as plt
import numpy as np

# We plot for each seed separately


def plot_avg_ppr(was_human: bool, bot_name: str) -> None:
    """Plots the average number of points per round."""

    global matches

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

    for idx in range(max_trick + 1):
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

    # Save image
    plt.savefig(
        f'docs/images/{"human" if was_human else "bot"}/{bot_name}_avg_ppr.png',
        bbox_inches="tight",
    )

    plt.show()


def print_avg_mtpr(was_human: bool, bot_name: str) -> None:
    """Plots the average number of move types per round."""

    global matches

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

    global matches

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
    for idx in range(max_trick + 1):
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

    # Save image
    plt.savefig(
        f'docs/images/{"human" if was_human else "bot"}/{bot_name}_avg_lr.png',
        bbox_inches="tight",
    )

    plt.show()


def plot_avg_lead_rates(was_human: bool, bot_name: str) -> None:
    """Plots the average number of times you were in the lead per trick."""

    global matches

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
    for idx in range(max_trick + 1):
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

    # Save image
    plt.savefig(
        f'docs/images/{"human" if was_human else "bot"}/{bot_name}_avg_ldr.png',
        bbox_inches="tight",
    )

    plt.show()


def print_avg_win_ratio(was_human: bool, bot_name: str) -> None:
    """Prints the average win ratio."""

    global matches

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
    print("#                     Human Stats                       #\n")

    # Randbot
    print("#-----------------Stats Against Randbot-----------------#")
    print_avg_win_ratio(True, "rand")
    print_avg_mtpr(True, "rand")

    print()

    # Rdeep
    print("#-----------------Stats Against Rdeep-------------------#")
    print_avg_win_ratio(True, "rdeep")
    print_avg_mtpr(True, "rdeep")

    # Plotting

    # Randbot
    plot_avg_ppr(True, "rand")
    plot_avg_leader_rates(True, "rand")
    plot_avg_lead_rates(True, "rand")

    # Rdeep
    plot_avg_ppr(True, "rdeep")
    plot_avg_leader_rates(True, "rdeep")
    plot_avg_lead_rates(True, "rdeep")

    print()

if is_bot:
    # Printing
    print("#                    Brainbot Stats                     #\n")

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
