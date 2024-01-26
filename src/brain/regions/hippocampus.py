from src.utils.region import Region
import tensorflow as tf


class Hippocampus(Region):
    def __init__(self, shape: tuple) -> None:
        super().__init__("Hippocampus", shape)

        self.layers = [
            tf.keras.layers.Reshape((1, 1, 8**2)),
            # Processing spatial information,
            # Commonly used for images but, we'll improvise
            tf.keras.layers.Conv2D(8**3, 1, activation="relu"),
            # Suitable for processing sequential data
            # tanh -> captures a range of values
            tf.keras.layers.Reshape((1, 8**3)),
            tf.keras.layers.LSTM(8**3, activation="tanh", return_sequences=True),
            # Attention mechanisms help the model focus on relevant parts of the input sequence
            # tf.keras.layers.Attention(),  # Self-attention layer
            # Aggregate information from the attention mechanism and previous layers
            tf.keras.layers.Dense(8**4, activation="relu"),
        ]

        return None
