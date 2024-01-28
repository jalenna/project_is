from src.utils.region import Region
import tensorflow as tf


class Amygdala(Region):
    """This region mimicks the behavior of the amygdala which handles emotion processing, especially fear and reward."""

    def __init__(self, shape: tuple) -> None:
        super().__init__("Amygdala", shape)

        # This number was chosen beause we although we may think we have a lot of fears and rewards,
        # They can be represented just the same and mean the opposite
        # If 1 means that I like something (reward),
        # than it can be implied that a different number means I don't like it as much (fear/less rewarding)
        nr_units = 8**2

        self.layers = [
            # Capture high-level relationships or associations in the input features that are not necessarily spatial or sequential.
            # Balanced emotions -> sigmoid
            tf.keras.layers.Dense(units=nr_units, activation="sigmoid"),
            tf.keras.layers.Reshape((1, -1, nr_units)),
            #
            # Non-linearity and computational simplicity -> relu
            # Conv layers can help capture spatial relationships within the features.
            tf.keras.layers.Conv2D(
                filters=nr_units,
                kernel_size=1,
                activation="relu",
            ),
            tf.keras.layers.Reshape((-1, nr_units)),
            #
            # Data is sequential in nature, LSTM layers can capture the temporal dynamics of these features.
            # Mixed emotions -> tanh
            tf.keras.layers.LSTM(
                units=nr_units,
                activation="tanh",
                return_sequences=True,
            ),
        ]

        return None
