class Region:
    """
    Base class for a single region in the brain.
    All regions in the brain must inherit from this class.
    """

    def __init__(self, name: str, shape: tuple) -> None:
        """Constructs a brain region with the specified name.

        Arguments:
            name (str): The name of this region of the brain

        Returns:
            None
        """

        self.name: str = name
        self.layer: list[any]
        self.shape = shape
        self.signals: list[int]
        self.signals_path: str

        return None

    def input(self, signals_path: str) -> None:
        """Accepts the forwarded inputs into this region of the brain.

        Arguments:
            signals (list[int]): The impulses/data of the previous layer

        Returns:
            None
        """

        self.signals = signals_path

        return None

    def classify(self) -> None:
        """Classification method of this region.
        Add your checks and conditions here.
        """

        return None

    def activation_function(self) -> any:
        """Activation function used by this region.

        Arguments:
            None

        Returns:
            any: Depends on your implementation
        """

        return 0

    def output(self) -> list[int]:
        """Transfers the signals out.

        Arguments:
            None

        Returns:
            list[int]: The modified signals
        """

        return self.signals

    def get_layer(self) -> list[any]:
        return self.layer
