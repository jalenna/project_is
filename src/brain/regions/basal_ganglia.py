from src.utils.region import Region
import tensorflow as tf


class BasalGanglia(Region):
    def __init__(self, shape: tuple) -> None:
        super().__init__("Basal Ganglia", shape)

        self.layers = [
            # Capture temporal dependencies in sequential data
            tf.keras.layers.LSTM(8**4, return_sequences=True),
            # Promote more robust learning
            tf.keras.layers.Dropout(0.2),
            # Can improve the convergence
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LSTM(8**4, return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.BatchNormalization(),
        ]

        return None
