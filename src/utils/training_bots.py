import random
from typing import Optional
from schnapsen.game import (
    Bot,
    PlayerPerspective,
    Move,
    GameState,
    GamePlayEngine,
    RegularMove,
    TrumpExchange,
    Marriage,
)
from src.utils.VU.ml_utils import get_move_feature_vector, get_state_feature_vector
from schnapsen.bots import RandBot as rb
from src.utils.logger import Log
from src.utils.CONSTANTS import GLOBAL_SETTINGS

SETTINGS: GLOBAL_SETTINGS = GLOBAL_SETTINGS()

# Initiliaze logger to be used as a singleton
g_logger = Log()

# Used for encoding our moves
move_to_int: dict[Move, int] = {
    RegularMove: 0,
    TrumpExchange: 1,
    Marriage: 2,
}


class RandBot(Bot):
    """This bot plays random moves, deterministically using the random number generator provided."""

    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        """Initiliazer for randbot.

        Arguments:
            rand (random.Random): The random number generator used to make the random choice of cards
            name (Optional[str]): The optional name of this bot

        Returns:
            None
        """

        super().__init__(name)

        self.rng = rand

        # variables to be tested
        self.ppt: list[int] = []  # Points per trick
        self.mtpr: list[int] = []  # Move type per round
        self.lr: list[int] = []  # Leader rate
        self.wr: list[int] = []  # Lead rate

    def get_move(
        self,
        perspective: PlayerPerspective,
        leader_move: Optional[Move],
    ) -> Move:
        moves: list[Move] = perspective.valid_moves()
        move: Move = self.rng.choice(moves)

        # Capture information for logging
        # All information is relevant to the human and AI, hence the usage of "opponent"
        opp_score: int = perspective.get_opponent_score().direct_points
        self.ppt.append(opp_score)

        if leader_move:
            self.mtpr.append(move_to_int[type(leader_move)])
            self.lr.append(1)
        else:
            self.mtpr.append(-1)
            self.lr.append(0)

        if opp_score > perspective.get_my_score().direct_points:
            self.wr.append(1)
        else:
            self.wr.append(0)

        return move

    def notify_game_end(self, won: bool, perspective: PlayerPerspective) -> None:
        # Add all relevant constants
        g_logger.log_to_file("SEED USED", str(SETTINGS.SEED), is_entry=False)
        g_logger.log_to_file(
            "TRAINING_SIZE_CAP USED", str(SETTINGS.TRAINING_SIZE_CAP), is_entry=False
        )
        g_logger.log_to_file(
            "TRAINING_ITERATIONS USED",
            str(SETTINGS.TRAINING_ITERATIONS),
            is_entry=False,
        )

        # Log all the game's information to the file
        g_logger.log_to_file("rand", str(self.ppt))
        g_logger.log_to_file("rand", str(self.mtpr))
        g_logger.log_to_file("rand", str(self.lr))
        g_logger.log_to_file("rand", str(self.wr))
        g_logger.log_to_file("rand", str(not won))

        return None

    def update_seed(self, seed: int) -> None:
        """Update the seed of this bot's randomness."""

        self.rng = random.Random(seed)

        return None


class RdeepBot(Bot):
    """
    Rdeep bot is a bot which performs many random rollouts of the game to decide which move to play.
    """

    def __init__(
        self,
        num_samples: int,
        depth: int,
        rand: random.Random,
        name: Optional[str] = None,
    ) -> None:
        """
        Create a new rdeep bot.

        :param num_samples: how many samples to take per move
        :param depth: how deep to sample
        :param rand: the source of randomness for this Bot
        :param name: the name of this Bot
        """
        super().__init__(name)
        assert (
            num_samples >= 1
        ), f"we cannot work with less than one sample, got {num_samples}"
        assert depth >= 1, f"it does not make sense to use a dept <1. got {depth}"
        self.__num_samples = num_samples
        self.__depth = depth
        self.__rand = rand

        self.ppt: list[int] = []  # Points per trick
        self.mtpr: list[int] = []  # Move type per round
        self.lr: list[int] = []  # Leader rate
        self.wr: list[int] = []  # Lead rate

    def get_move(
        self, perspective: PlayerPerspective, leader_move: Optional[Move]
    ) -> Move:
        # get the list of valid moves, and shuffle it such
        # that we get a random move of the highest scoring
        # ones if there are multiple highest scoring moves.
        moves = perspective.valid_moves()
        self.__rand.shuffle(moves)

        best_score = float("-inf")
        best_move = None
        chosen_i = 0
        for i, move in enumerate(moves):
            sum_of_scores = 0.0
            for _ in range(self.__num_samples):
                gamestate = perspective.make_assumption(
                    leader_move=leader_move, rand=self.__rand
                )
                score = self.__evaluate(
                    gamestate, perspective.get_engine(), leader_move, move
                )
                sum_of_scores += score
            average_score = sum_of_scores / self.__num_samples
            if average_score > best_score:
                best_score = average_score
                best_move = move
                chosen_i = i

        assert best_move is not None

        # Capture information for logging
        # All information is relevant to the human and AI, hence the usage of "opponent"
        opp_score: int = perspective.get_opponent_score().direct_points
        self.ppt.append(opp_score)

        if leader_move:
            self.mtpr.append(move_to_int[type(leader_move)])
            self.lr.append(1)
        else:
            self.mtpr.append(-1)
            self.lr.append(0)

        if opp_score > perspective.get_my_score().direct_points:
            self.wr.append(1)
        else:
            self.wr.append(0)

        return best_move

    def notify_game_end(self, won: bool, perspective: PlayerPerspective) -> None:
        # Add all relevant constants
        g_logger.log_to_file("SEED USED", str(SETTINGS.SEED), is_entry=False)
        g_logger.log_to_file(
            "TRAINING_SIZE_CAP USED", str(SETTINGS.TRAINING_SIZE_CAP), is_entry=False
        )
        g_logger.log_to_file(
            "TRAINING_ITERATIONS USED",
            str(SETTINGS.TRAINING_ITERATIONS),
            is_entry=False,
        )

        # Log all the game's information to the file
        g_logger.log_to_file("rdeep", str(self.ppt))
        g_logger.log_to_file("rdeep", str(self.mtpr))
        g_logger.log_to_file("rdeep", str(self.lr))
        g_logger.log_to_file("rdeep", str(self.wr))
        g_logger.log_to_file("rdeep", str(not won))

        return None

    def __evaluate(
        self,
        gamestate: GameState,
        engine: GamePlayEngine,
        leader_move: Optional[Move],
        my_move: Move,
    ) -> float:
        """
        Evaluates the value of the given state for the given player
        :param state: The state to evaluate
        :param player: The player for whom to evaluate this state (1 or 2)
        :return: A float representing the value of this state for the given player. The higher the value, the better the
                state is for the player.
        """
        me: Bot
        leader_bot: Bot
        follower_bot: Bot

        if leader_move:
            # we know what the other bot played
            leader_bot = FirstFixedMoveThenBaseBot(rb(rand=self.__rand), leader_move)
            # I am the follower
            me = follower_bot = FirstFixedMoveThenBaseBot(rb(rand=self.__rand), my_move)
        else:
            # I am the leader bot
            me = leader_bot = FirstFixedMoveThenBaseBot(rb(rand=self.__rand), my_move)
            # We assume the other bot just random
            follower_bot = rb(self.__rand)

        new_game_state, _ = engine.play_at_most_n_tricks(
            game_state=gamestate,
            new_leader=leader_bot,
            new_follower=follower_bot,
            n=self.__depth,
        )

        if new_game_state.leader.implementation is me:
            my_score = new_game_state.leader.score.direct_points
            opponent_score = new_game_state.follower.score.direct_points
        else:
            my_score = new_game_state.follower.score.direct_points
            opponent_score = new_game_state.leader.score.direct_points

        heuristic = my_score / (my_score + opponent_score)
        return heuristic

    def update_seed(self, seed: int) -> None:
        """Update the seed of this bot's randomness."""

        self.__rand = random.Random(seed)

        return None


class FirstFixedMoveThenBaseBot(Bot):
    def __init__(self, base_bot: Bot, first_move: Move) -> None:
        self.first_move = first_move
        self.first_move_played = False
        self.base_bot = base_bot

    def get_move(
        self, perspective: PlayerPerspective, leader_move: Optional[Move]
    ) -> Move:
        if not self.first_move_played:
            self.first_move_played = True
            return self.first_move
        return self.base_bot.get_move(perspective=perspective, leader_move=leader_move)
