class Region:
    """
    Base class for a single region in the brain.
    All regions in the brain must inherit from this class.
    """

    def __init__(self, name: str) -> None:
        """Constructs a brain region with the specified name.

        Arguments:
            name (str): The name of this region of the brain

        Returns:
            None
        """

        self.name: str = name
        self.signals: list[int]

    def input(self, signals: list[int]) -> None:
        """Accepts the forwarded inputs into this region of the brain.

        Arguments:
            signals (list[int]): The impulses/data of the previous layer

        Returns:
            None
        """

        self.signals = signals

    def output(self) -> list[int]:
        """Transfers the signals out.

        Arguments:
            None

        Returns:
            list[int]: The modified signals
        """

        return self.signals
