from src.utils.region import Region
import tensorflow as tf


class Amygdala(Region):
    def __init__(self, shape: tuple) -> None:
        super().__init__("Amygdala", shape)

        nr_units = 8**2

        self.layers = [
            # Capture high-level relationships or associations in the input features that are not necessarily spatial or sequential.
            # Non-linearity and computational simplicity -> relu
            tf.keras.layers.Dense(units=nr_units, activation="relu"),
            tf.keras.layers.Reshape((1, 1, nr_units)),
            # Conv layers can help capture spatial relationships within the features.
            tf.keras.layers.Conv2D(
                filters=nr_units,
                kernel_size=1,
                activation="relu",
            ),
            tf.keras.layers.Reshape((-1, nr_units)),
            # Data is sequential in nature, LSTM layers can capture the temporal dynamics of these features.
            # Mixed emotions -> tanh
            tf.keras.layers.LSTM(
                units=nr_units,
                activation="tanh",
                return_sequences=True,
            ),
        ]

        return None
