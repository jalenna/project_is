from src.utils.region import Region
import tensorflow as tf


class PFC(Region):
    """
    The initial game state and relevant information are processed first,
    mimicking the role of the prefrontal cortex in handling executive functions and initial decision-making processes.
    """

    def __init__(self, shape: tuple) -> None:
        super().__init__("Prefrontal Cortex", shape)

        nr_units = 8**2

        self.layer = [
            # Handle initial decision making (Initial impressions)
            # tf.keras.layers.Reshape((173, 1)),
            tf.keras.layers.SimpleRNN(
                units=nr_units,
                activation="tanh",
                input_shape=shape,
                return_sequences=True,
            ),
            # Tailor decision to a more specific outcome (Deeper analysis)
            tf.keras.layers.LSTM(
                units=nr_units,
                activation="tanh",
                # input_shape=shape,
                return_sequences=True,
            ),
        ]

        return None

    def output(self) -> list[int]:
        return super().output()

    def get_layer(self) -> list[any]:
        return super().get_layer()
