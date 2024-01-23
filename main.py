from src.brain.brain import Brain


def main() -> int:
    """Main application entry point.

    Arguments:
        None

    Returns:
        int: Exit code
    """

    brain: Brain = Brain()
    brain.run_all()

    return 0


main()
