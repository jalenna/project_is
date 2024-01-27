import tensorflow as tf
import numpy as np


class FirstLayer:
    """Receives the input."""

    def __init__(self) -> None:
        self.layer: any
        # features
        self.X: list[list[int]]
        # won labels
        self.y: list[int]
        return None

    def input(self, signals_path: str) -> None:
        self.handle_input(signals_path)

        return None

    def handle_input(self, signals_path: str):
        data: list[list[int]] = []
        targets: list[int] = []

        with open(file=signals_path, mode="r") as replay_memory_file:
            CAP: int = 0
            for line in replay_memory_file:
                # TODO
                if CAP > 20000:
                    break
                CAP += 1
                feature_string, won_label_str = line.split("||")
                feature_list_strings: list[str] = feature_string.split(",")
                feature_list = [int(feature) for feature in feature_list_strings]
                won_label = int(won_label_str)
                data.append(feature_list)
                targets.append(won_label)

        # self.X = np.array(data).reshape((len(data), -1, len(data[0])))
        self.X = np.array(data).reshape((len(data), -1, len(data[0])))
        # self.X = np.array(data)
        # self.X = np.array(data)
        self.y = np.array(targets).reshape((-1, 1))
        # self.y = np.array(targets)

        self.layer = tf.keras.layers.InputLayer(
            input_shape=(len(self.X[0]), len(self.X[0][0]))
        )

    def get_features_and_labels(self) -> tuple[list[list[int]], list[int]]:
        return self.X, self.y

    def get_layer(self) -> any:
        return self.layer
