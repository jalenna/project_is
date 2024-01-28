from src.utils.region import Region
import tensorflow as tf


class PFC(Region):
    """
    The initial game state and relevant information are processed first,
    mimicking the role of the prefrontal cortex in handling executive functions and initial decision-making processes.
    """

    def __init__(self, shape: tuple) -> None:
        super().__init__("Prefrontal Cortex", shape)

        # This number was chosen because we think the initial impressions should be kept to a small number
        # of "judgements" so to speak.
        nr_units = 8**2

        self.layer = [
            # Handle initial decision making (Initial impressions)
            # We're using "tanh" here because it can represent a positive and negative range (of emotions)
            tf.keras.layers.SimpleRNN(
                units=nr_units,
                activation="tanh",
                input_shape=shape,
                return_sequences=True,
            ),
            # Tailor decision to a more specific outcome (Deeper analysis)
            # Again, we're using "tanh" here because it can represent a positive and negative range (of emotions)
            tf.keras.layers.LSTM(
                units=nr_units,
                activation="tanh",
                return_sequences=True,
            ),
        ]

        return None
