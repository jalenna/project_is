from src.utils.region import Region
import tensorflow as tf


class BasalGanglia(Region):
    def __init__(self, shape: tuple) -> None:
        super().__init__("Basal Ganglia", shape)
        nr_units = 8**2

        self.layers = [
            # Capture temporal dependencies in sequential data
            tf.keras.layers.LSTM(nr_units, return_sequences=True),
            # Promote more robust learning
            tf.keras.layers.Dropout(0.2),
            # Can improve the convergence but, not recommend for sequential data
            # tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LSTM(nr_units, return_sequences=True),
            # tf.keras.layers.Dropout(0.2),
            # tf.keras.layers.BatchNormalization(),
        ]

        return None
