from src.utils.region import Region
import tensorflow as tf


class Amygdala(Region):
    def __init__(self, shape: tuple) -> None:
        super().__init__("Amygdala", shape)

        self.layers = [
            # Capture high-level relationships or associations in the input features that are not necessarily spatial or sequential.
            # Non-linearity and computational simplicity -> relu
            tf.keras.layers.Dense(units=8**3, activation="relu"),
            tf.keras.layers.Reshape((-1, 1, 8**3)),
            # Conv layers can help capture spatial relationships within the features.
            tf.keras.layers.Conv2D(
                filters=8**3,
                kernel_size=1,
                activation="relu",
            ),
            tf.keras.layers.Reshape((-1, 8**3)),
            # Data is sequential in nature, LSTM layers can capture the temporal dynamics of these features.
            # Mixed emotions -> tanh
            tf.keras.layers.LSTM(
                units=8**2,
                activation="tanh",
                return_sequences=True,
            ),
        ]

        return None
