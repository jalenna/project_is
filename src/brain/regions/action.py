from utils.region import Region


class Action(Region):
    """Performs the most probable action based on the conclusion drawn by all the regions."""

    def __init__(self) -> None:
        super().__init__("Hand")

        return None
