import datetime


class Log:
    """Used for logging.
    Intended to be used as a singleton.
    """

    _instance = None

    def __init__(self) -> None:
        """Initializes a log class."""

        # Create the file to be used throughout
        self.filename = (
            f"logs\\log_{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
        )
        self.file = open(self.filename, "x")

        self.file.close()

        return None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)

        return cls._instance

    def log_to_file(self, name: str, text: str, is_entry: bool = True) -> None:
        """Logs the given text to the file.

        Arguments:
            name (str): The suffix of the line(s) of text to be added
            text (str): The text to be added
            is_entry (bool): If a timestamp should be added

        Returns:
            None
        """

        try:
            self.file = open(self.filename, "a")
        except:
            print("ERROR Opening file")

        if is_entry:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: {name} - {text}\n"
        else:
            log_entry = f"{name}: {text}\n"

        self.file.write(log_entry)
        self.file.flush()

        self.close_log()

        return None

    def close_log(self) -> None:
        """Closes the file used for logging."""

        self.file.close()

        return None
