class Region:
    """
    Base class for a single region in the brain.
    All regions in the brain must inherit from this class.
    """

    def __init__(self, name: str) -> None:
        """Constructs a brain region with the specified name.

        Parameters:
            - name: str -> The name of this region of the brain

        Return: None
        """

        self.name: str = name
        self.signals: list[int]

    def input(self, signals: list[int]) -> None:
        """Accepts the forwarded inputs into this region of the brain.

        Parameters:
            - signals: list[int] -> The impulses/data of the previous layer

            Return: None
        """

        self.signals = signals

    def output(self) -> list[int]:
        """Transfers the signals out.

        Parameters: None

        Returns: list[int] -> The modified signals
        """

        return self.signals
