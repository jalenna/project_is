from src.brain.regions.first_layer import FirstLayer
from src.brain.regions.prefrontal_cortex import PFC

import tensorflow as tf


class Brain:
    """
    The neural network comprised of "brain-regions."
    """

    def __init__(self) -> None:
        """Constructs the brain of this neural network."""
        input_layer: FirstLayer = FirstLayer()
        input_layer.input("ml_data/random_random_10k_games.txt")

        self.X, self.y = input_layer.get_features_and_labels()

        self.dataset = tf.data.Dataset.from_tensor_slices((self.X, self.y))

        self.regions: tf.keras.Sequential = tf.keras.Sequential()

        self.regions.add(input_layer.get_layer())

        # Add brain regions here
        self.regions.add(PFC((len(self.X[0]), len(self.y))).get_layer())

    def train(self):
        self.regions.compile(optimizer="adam", loss="mean_squared_error")
        self.regions.fit(self.X, self.y, epochs=10)
        self.regions.summary()
