from src.utils.region import Region
import tensorflow as tf


class InsularCortex(Region):
    """This region mimicks the role of the insular cortex in handling interoception and the processing of internal states."""

    def __init__(self, shape: tuple) -> None:
        super().__init__("Ïnsular Cortex", shape)

        # This number was chosen because we wan't to narrow down our options (interoception, that gut feeling)
        nr_units = 8**2

        self.layers = [
            # Reshape the previous layer's output to match our expected input
            tf.keras.layers.Reshape((1, nr_units)),
            #
            # Convolutional layers for processing 1D spatial data
            # tf.keras.layers.Conv1D(nr_units, 1, activation="relu"), # Are detrimental to performance, if winning is key reduce cnn's as much as possible
            #
            # Reduce spatial dimensions.
            # tf.keras.layers.MaxPooling1D(1),
            #
            tf.keras.layers.Conv1D(nr_units, 1, activation="relu"),
            #
            # Was commented out for performance, if it were an amateur/novie player we would leave this uncommented
            # tf.keras.layers.MaxPooling1D(1), # Introduces more "noise"
            # tf.keras.layers.Flatten(),
            #
            tf.keras.layers.Reshape((1, nr_units)),
            #
            # LSTM layer for final processing stage of sequential data
            tf.keras.layers.LSTM(nr_units, activation="relu", return_sequences=True),
            #
            # Dense layers for processing flattened and sequential data
            # tf.keras.layers.Dense(nr_units, activation="relu"),
            # tf.keras.layers.Dense(5, activation="relu"),
            #
            # Output layer
            tf.keras.layers.Reshape((nr_units,)),
            tf.keras.layers.Dense(2, activation="relu"),
        ]

        return None
