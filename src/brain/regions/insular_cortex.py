from src.utils.region import Region
import tensorflow as tf


class InsularCortex(Region):
    def __init__(self, shape: tuple) -> None:
        super().__init__("Ïnsular Cortex", shape)

        self.layers = [
            # Convolutional layers for processing 2D spatial data (e.g., images)
            tf.keras.layers.Conv2D(8**3, 1, activation="relu"),
            # Reduce spatial dimensions.
            tf.keras.layers.MaxPooling2D((1, 8)),
            tf.keras.layers.Conv2D(8**3, 1, activation="relu"),
            tf.keras.layers.MaxPooling2D((1, 8)),
            tf.keras.layers.Flatten(),
            # LSTM layer for processing sequential data
            tf.keras.layers.LSTM(8**4, activation="relu", return_sequences=True),
            # Dense layers for processing flattened and sequential data
            tf.keras.layers.Dense(8**3, activation="relu"),
            tf.keras.layers.Dense(8**2, activation="relu"),
            # Output layer (adjust units and activation based on your task)
            tf.keras.layers.Dense(8, activation="softmax"),
        ]

        return None
