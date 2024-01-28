from src.utils.region import Region
import tensorflow as tf


class Hippocampus(Region):
    """This region mimicks the hippocampus which handles memory formation and spatial navigation."""

    def __init__(self, shape: tuple) -> None:
        super().__init__("Hippocampus", shape)

        # This number was chosen because humans' memory is very limited.
        nr_units = 8**2

        self.layers = [
            # Restructure the incoming data for our purposes
            tf.keras.layers.Reshape((1, 1, nr_units)),
            #
            # Processing spatial information,
            # Commonly used for images but, we'll apply it here nonetheless
            tf.keras.layers.Conv2D(nr_units, 1, activation="relu"),
            #
            # Suitable for processing sequential data
            # tanh -> captures a range of values
            tf.keras.layers.Reshape((1, nr_units)),
            tf.keras.layers.LSTM(nr_units, activation="tanh", return_sequences=True),
            #
            # Attention mechanisms help the model focus on relevant parts of the input sequence
            # tf.keras.layers.Attention(),  # Self-attention layer, couldn't get it to work though
            #
            # Aggregate information from the (attention mechanism and) previous layers
            tf.keras.layers.Dense(nr_units, activation="relu"),
        ]

        return None
