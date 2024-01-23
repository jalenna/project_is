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
        pfc: PFC = PFC((len(self.X[0]), len(self.y)))
        for NN in pfc.get_layer():
            self.regions.add(NN)

        return None

    def train(self) -> None:
        self.regions.compile(optimizer="adam", loss="mean_squared_error")
        self.regions.fit(self.X, self.y, epochs=20)
        self.regions.summary()
        return None

    def save_model(self) -> None:
        self.regions.save("ml_data/brain.keras")
        return None

    def save_weights(self) -> None:
        self.regions.save_weights("ml_data/weights")
        return None

    def load_model(self) -> None:
        self.regions = tf.keras.models.load_model("ml_data/brain.keras")
        return None

    def load_weights(self) -> None:
        if self.regions is None:
            return None
        self.regions.load_weights("ml_data/weights")
        return None

    def run_all(self) -> int:
        print("Running all methods...")
        self.train()
        self.save_model()
        self.save_weights()
        self.load_model()
        self.load_weights()
        print("Ran all methods successfully.")
        return 0
