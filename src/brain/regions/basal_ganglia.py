from src.utils.region import Region
import tensorflow as tf


class BasalGanglia(Region):
    """
    This region mimmicks the role of the basal ganglia in handling procedural learning, habit formation, motor functions.
    """

    def __init__(self, shape: tuple) -> None:
        super().__init__("Basal Ganglia", shape)
        nr_units = 8**2

        # Motor functions aren't really relevant to our network since it's only concerned about "what" it should play
        # and not "how" it should play

        self.layers = [
            # Procedural learning and habit formation of very sequential in nature
            # so it makes sense for us to use a layer that does just that
            #
            # We're also using "relu" because the person would be "eager" or more inclined to play a move at this point
            # since it's part of their habit (and in a broader sense, the (procedural) learning process)
            #
            # Capture temporal dependencies in sequential data
            tf.keras.layers.LSTM(nr_units, activation="relu", return_sequences=True),
            #
            # Promote more robust learning
            tf.keras.layers.Dropout(0.2),
            #
            # Can improve the convergence but, not recommend for sequential data
            # tf.keras.layers.BatchNormalization(),
            #
            tf.keras.layers.LSTM(nr_units, activation="relu", return_sequences=True),
            #
            # Again, can improve the convergence but, not recommend for sequential data
            # tf.keras.layers.Dropout(0.2),
            # tf.keras.layers.BatchNormalization(),
        ]

        return None
