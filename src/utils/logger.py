import datetime
from .CONSTANTS import SEED


class Log:
    def __init__(self) -> None:
        self.filename = (
            f"logs\\log_{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
        )
        self.file = open(self.filename, "x")
        self.file.write(f"SEED USED: {SEED}\n")
        self.file.flush()
        self.file.close()

    def log_to_file(self, name: str, text: str) -> None:
        try:
            self.file = open(self.filename, "a")
        except:
            print("ERROR Opening file")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}: {name} - {text}\n"
        self.file.write(log_entry)
        self.file.flush()
        self.close_log()

    def close_log(self) -> None:
        self.file.close()
