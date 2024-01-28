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
        self.layer: any = None
        self.layers: list[any] = []
        self.shape = shape
        self.signals: list[int]
        self.signals_path: str

        return None

    def _input(self, signals_path: str) -> None:
        """Accepts the forwarded inputs into this region of the brain.

        Arguments:
            signals (list[int]): The impulses/data of the previous layer

        Returns:
            None
        """

        self.signals = signals_path

        return None

    def get_layer(self) -> any:
        """Getter for our layer."""

        return self.layer

    def get_layers(self) -> list[any]:
        """Getter for our layers."""

        if len(self.layers) == 0 and self.layer:
            return [self.layer]

        return self.layers
