from src.utils.region import Region
import tensorflow as tf


class InsularCortex(Region):
    def __init__(self, shape: tuple) -> None:
        super().__init__("Ïnsular Cortex", shape)

        nr_units = 8**2

        self.layers = [
            tf.keras.layers.Reshape((1, nr_units)),
            # Convolutional layers for processing 1D spatial data
            # tf.keras.layers.Conv1D(nr_units, 1, activation="relu"), # Are detrimental to performance, if winning is key reduce cnn's as much as possible
            # Reduce spatial dimensions.
            # tf.keras.layers.MaxPooling1D(1),
            tf.keras.layers.Conv1D(nr_units, 1, activation="tanh"),
            # tf.keras.layers.MaxPooling1D(1), # introduces more "noise"
            # tf.keras.layers.Flatten(),
            tf.keras.layers.Reshape((1, nr_units)),
            # LSTM layer for processing sequential data
            tf.keras.layers.LSTM(nr_units, activation="relu", return_sequences=True),
            # Dense layers for processing flattened and sequential data
            # tf.keras.layers.Dense(nr_units, activation="relu"),
            # tf.keras.layers.Dense(5, activation="relu"),
            # Output layer (adjust units and activation based on your task)
            tf.keras.layers.Reshape((nr_units,)),
            tf.keras.layers.Dense(2, activation="tanh"),
        ]

        return None
