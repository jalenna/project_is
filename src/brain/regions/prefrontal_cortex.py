from src.utils.region import Region
import tensorflow as tf


class PFC(Region):
    """
    The initial game state and relevant information are processed first,
    mimicking the role of the prefrontal cortex in handling executive functions and initial decision-making processes.
    """

    def __init__(self, shape: tuple) -> None:
        super().__init__("Prefrontal Cortex", shape)
        self.layer = tf.keras.layers.LSTM(
            units=shape[1], activation="relu", input_shape=shape
        )
        return None

    def output(self) -> list[int]:
        return super().output()

    def get_layer(self) -> any:
        return super().get_layer()
