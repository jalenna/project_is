import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, GameState, GamePlayEngine
from .ml_utils import get_move_feature_vector, get_state_feature_vector
from schnapsen.bots import RandBot as rb
from .logger import Log

g_logger = Log()


class RandBot(Bot):
    """This bot plays random moves, deterministically using the random number generator provided.

    Args:
        rand (random.Random): The random number generator used to make the random choice of cards
        name (Optional[str]): The optional name of this bot
    """

    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.rng = rand

    def get_move(
        self,
        perspective: PlayerPerspective,
        leader_move: Optional[Move],
    ) -> Move:
        # get the sate feature representation
        state_representation = get_state_feature_vector(perspective)
        # get the leader's move representation, even if it is None
        leader_move_representation = get_move_feature_vector(leader_move)
        # get all my valid moves
        my_valid_moves = perspective.valid_moves()
        # get the feature representations for all my valid moves
        my_move_representations: list[list[int]] = []
        for my_move in my_valid_moves:
            my_move_representations.append(get_move_feature_vector(my_move))

        # create all model inputs, for all bot's valid moves
        action_state_representations: list[list[int]] = []

        if perspective.am_i_leader():
            follower_move_representation = get_move_feature_vector(None)
            for my_move_representation in my_move_representations:
                action_state_representations.append(
                    state_representation
                    + my_move_representation
                    + follower_move_representation
                )
        else:
            for my_move_representation in my_move_representations:
                action_state_representations.append(
                    state_representation
                    + leader_move_representation
                    + my_move_representation
                )

        moves: list[Move] = perspective.valid_moves()
        # move = self.rng.choice(moves)
        chosen_i, move = self.rng.choice(list(enumerate(moves)))

        g_logger.log_to_file("rand", str(action_state_representations[chosen_i]))

        return move


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

        # get the sate feature representation
        state_representation = get_state_feature_vector(perspective)
        # get the leader's move representation, even if it is None
        leader_move_representation = get_move_feature_vector(leader_move)
        # get all my valid moves
        my_valid_moves = perspective.valid_moves()
        # get the feature representations for all my valid moves
        my_move_representations: list[list[int]] = []
        for my_move in my_valid_moves:
            my_move_representations.append(get_move_feature_vector(my_move))

        # create all model inputs, for all bot's valid moves
        action_state_representations: list[list[int]] = []

        if perspective.am_i_leader():
            follower_move_representation = get_move_feature_vector(None)
            for my_move_representation in my_move_representations:
                action_state_representations.append(
                    state_representation
                    + my_move_representation
                    + follower_move_representation
                )
        else:
            for my_move_representation in my_move_representations:
                action_state_representations.append(
                    state_representation
                    + leader_move_representation
                    + my_move_representation
                )

        g_logger.log_to_file("rdeep", str(action_state_representations[chosen_i]))

        return best_move

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
