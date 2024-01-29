from src.brain.regions.insular_cortex import InsularCortex
from src.brain.regions.basal_ganglia import BasalGanglia
from src.brain.regions.hippocampus import Hippocampus
from src.brain.regions.amygdala import Amygdala
from src.brain.regions.first_layer import FirstLayer
from src.brain.regions.prefrontal_cortex import PFC
from src.utils.CONSTANTS import GLOBAL_SETTINGS

import tensorflow as tf

SETTINGS: GLOBAL_SETTINGS = GLOBAL_SETTINGS()


class Brain:
    """
    The neural network comprised of "brain-regions."
    """

    def __init__(self) -> None:
        """Constructs the brain of this neural network."""

        input_layer: FirstLayer = FirstLayer()
        input_layer._input(SETTINGS.TRAINING_SET_FILE_PATH)

        self.X, self.y = input_layer.get_features_and_labels()

        # Initialize the model
        self.regions: tf.keras.Sequential = tf.keras.Sequential()

        self.regions.add(input_layer.get_layer())

        # Define the shape of our data
        shape = (len(self.X[0]), len(self.X[0][0]))

        # Add brain regions here
        # The order can be found in BRAIN_OVERVIEW.md

        pfc: PFC = PFC(shape)
        for NN in pfc.get_layer():
            self.regions.add(NN)

        amygdala: Amygdala = Amygdala(shape)
        for NN in amygdala.get_layers():
            self.regions.add(NN)

        hippocampus: Hippocampus = Hippocampus(shape)
        for NN in hippocampus.get_layers():
            self.regions.add(NN)

        basal_ganglia: BasalGanglia = BasalGanglia(shape)
        for NN in basal_ganglia.get_layers():
            self.regions.add(NN)

        insular_cortex: InsularCortex = InsularCortex(shape)
        for NN in insular_cortex.get_layers():
            self.regions.add(NN)

        return None

    def train(self) -> None:
        """Trains the model."""

        self.regions.compile(
            optimizer="adam", loss="mean_squared_error", metrics=["accuracy"]
        )
        self.regions.fit(self.X, self.y, epochs=SETTINGS.TRAINING_ITERATIONS)

        # Optional, print the overview of the model
        self.regions.summary()

        return None

    def save_model(self) -> None:
        """Saves the model.

        Saves the model to the specified path in src.utils.CONSTANTS.py
        """

        self.regions.save(SETTINGS.MODEL_SAVE_PATH)

        return None

    def save_weights(self) -> None:
        """Saves the weights of the model.

        Useful for analyzing individual weights/connections.

        Saves the weights to the specified path in src.utils.CONSTANTS.py
        """

        self.regions.save_weights(SETTINGS.MODEL_WEIGHTS_PATH)

        return None

    def load_model(self) -> None:
        """Loads and sets the model of this instance of the brain."""

        self.regions = tf.keras.models.load_model(SETTINGS.MODEL_SAVE_PATH)

        return None

    def load_weights(self) -> None:
        """Loads the weights of the model in case the model is loaded into memory."""

        if self.regions is None:
            return None

        self.regions.load_weights(SETTINGS.MODEL_WEIGHTS_PATH)

        return None

    def run_all(self) -> int:
        """Runs all methods.

        Useful for debugging and experimenting.

        Arguments:
            None
        Returns:
            int: Exit code
        """

        print("Running all methods...")

        self.train()
        self.save_model()
        self.save_weights()
        self.load_model()
        self.load_weights()

        print("Ran all methods successfully.")

        return 0


# Code relevant to the bot

from schnapsen.game import Bot, PlayerPerspective, Move
import src.utils.VU.ml_utils as ml_utils
import numpy as np


class BrainPlayingBot(Bot, Brain):
    """
    This class loads a trained ML model and uses it to play.
    """

    def __init__(self, name: str = "BrainBot") -> None:
        """
        Create a new MLPlayingBot which uses the model stored in the model's location.

        Arguments:
            name optional(str): The name of the bot, default = "BrainBot"

        Returns:
            None
        """

        super().__init__(name)

        # load model
        self.load_model()

        # Or load the weights
        # self.load_weights()

    def get_move(
        self, perspective: PlayerPerspective, leader_move: Move | None
    ) -> Move:
        # get the sate feature representation
        state_representation = ml_utils.get_state_feature_vector(perspective)

        # get the leader's move representation, even if it is None
        leader_move_representation = ml_utils.get_move_feature_vector(leader_move)

        # get all my valid moves
        my_valid_moves = perspective.valid_moves()

        # get the feature representations for all my valid moves
        my_move_representations: list[list[int]] = []
        for my_move in my_valid_moves:
            my_move_representations.append(ml_utils.get_move_feature_vector(my_move))

        # create all model inputs, for all bot's valid moves
        action_state_representations: list[list[int]] = []

        if perspective.am_i_leader():
            follower_move_representation = ml_utils.get_move_feature_vector(None)
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

        # Convert actions to a numpy array
        action_state_representations_np = np.array(
            action_state_representations, dtype=np.float32
        )

        action_state_representations_np = np.expand_dims(
            np.array(action_state_representations_np), axis=1
        )

        model_output = self.regions.predict(action_state_representations_np, verbose=0)

        winning_probabilities_of_moves = [
            outcome_prob[1] for outcome_prob in model_output
        ]

        # Find the move with the highest probability of winning
        highest_value: float = -1
        best_move: Move = my_valid_moves[0]

        for index, value in enumerate(winning_probabilities_of_moves):
            if value > highest_value:
                highest_value = value
                best_move = my_valid_moves[index]

        return best_move
