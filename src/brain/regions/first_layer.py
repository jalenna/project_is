import tensorflow as tf
import numpy as np
from src.utils.CONSTANTS import GLOBAL_SETTINGS
from src.utils.region import Region

SETTINGS: GLOBAL_SETTINGS = GLOBAL_SETTINGS()


class FirstLayer(Region):
    """Receives the input.
    Useful for formatting our data.
    """

    def __init__(self) -> None:
        # features
        self.X: list[list[int]]
        # won labels
        self.y: list[int]
        return None

    # @override
    def _input(self, signals_path: str) -> None:
        """Entry point of this layer.

        Arguments:
            signals_path (str): The file path of the input data.

        Returns:
            None
        """

        self._handle_input(signals_path)

        return None

    def _handle_input(self, signals_path: str):
        """Formats the input for further use."""

        # Our features will be stored here (game/move encoding)
        data: list[list[int]] = []
        # Our labels will be stored here (W/L)
        targets: list[int] = []

        with open(file=signals_path, mode="r") as replay_memory_file:
            # Restrict training size for quick experimentation
            capacity: int = 0
            if SETTINGS.TRAINING_SIZE_CAP == -1:
                capacity = -1

            for line in replay_memory_file:
                if capacity > SETTINGS.TRAINING_SIZE_CAP:
                    break

                if capacity != -1:
                    capacity += 1

                # Parse the data
                feature_string, won_label_str = line.split("||")
                feature_list_strings: list[str] = feature_string.split(",")
                feature_list = [int(feature) for feature in feature_list_strings]
                won_label = int(won_label_str)
                data.append(feature_list)
                targets.append(won_label)

        # Reshape the data so they fit through the different regions
        self.X = np.array(data).reshape((len(data), -1, len(data[0])))
        self.y = np.array(targets).reshape((-1, 1))

        # Simply an input layer
        self.layer = tf.keras.layers.InputLayer(
            input_shape=(len(self.X[0]), len(self.X[0][0]))
        )

    def get_features_and_labels(self) -> tuple[list[list[int]], list[int]]:
        """Getter for the features and labels.

        Arguments:
            None

        Returns:
            tuple[list[list[int]], list[int]]: The features and labels as a tuple
        """

        return self.X, self.y
