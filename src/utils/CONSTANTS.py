class GLOBAL_SETTINGS:
    _instance = None

    def __init__(self) -> None:
        self._SEED: int = 42
        self._TRAINING_SIZE_CAP: int = 20000
        self._TRAINING_SET_FILE_PATH: str = "ml_data/random_random_10k_games.txt"
        self._TRAINING_ITERATIONS: int = 20
        self._MODEL_SAVE_PATH: str = "ml_data/brain.keras"
        self._MODEL_WEIGHTS_PATH: str = "ml_data/weights"
        self._HUMAN_LOGS_FILE_PATH: str = "logs/"
        self._ML_LOGS_FILE_PATH: str = "ml_data/logs/"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GLOBAL_SETTINGS, cls).__new__(cls)

        return cls._instance

    # Getter and Setter for SEED
    @property
    def SEED(self):
        return self._SEED

    @SEED.setter
    def SEED(self, value):
        self._SEED = value

    # Getter and Setter for TRAINING_SIZE_CAP
    @property
    def TRAINING_SIZE_CAP(self):
        return self._TRAINING_SIZE_CAP

    @TRAINING_SIZE_CAP.setter
    def TRAINING_SIZE_CAP(self, value):
        self._TRAINING_SIZE_CAP = value

    # Getter and Setter for TRAINING_SET_FILE_PATH
    @property
    def TRAINING_SET_FILE_PATH(self):
        return self._TRAINING_SET_FILE_PATH

    @TRAINING_SET_FILE_PATH.setter
    def TRAINING_SET_FILE_PATH(self, value):
        self._TRAINING_SET_FILE_PATH = value

    # Getter and Setter for TRAINING_ITERATIONS
    @property
    def TRAINING_ITERATIONS(self):
        return self._TRAINING_ITERATIONS

    @TRAINING_ITERATIONS.setter
    def TRAINING_ITERATIONS(self, value):
        self._TRAINING_ITERATIONS = value

    # Getter and Setter for MODEL_SAVE_PATH
    @property
    def MODEL_SAVE_PATH(self):
        return self._MODEL_SAVE_PATH

    @MODEL_SAVE_PATH.setter
    def MODEL_SAVE_PATH(self, value):
        self._MODEL_SAVE_PATH = value

    # Getter and Setter for MODEL_WEIGHTS_PATH
    @property
    def MODEL_WEIGHTS_PATH(self):
        return self._MODEL_WEIGHTS_PATH

    @MODEL_WEIGHTS_PATH.setter
    def MODEL_WEIGHTS_PATH(self, value):
        self._MODEL_WEIGHTS_PATH = value

    # Getter and Setter for HUMAN_LOGS_FILE_PATH
    @property
    def HUMAN_LOGS_FILE_PATH(self):
        return self._HUMAN_LOGS_FILE_PATH

    @HUMAN_LOGS_FILE_PATH.setter
    def HUMAN_LOGS_FILE_PATH(self, value):
        self._HUMAN_LOGS_FILE_PATH = value

    # Getter and Setter for ML_LOGS_FILE_PATH
    @property
    def ML_LOGS_FILE_PATH(self):
        return self._ML_LOGS_FILE_PATH

    @ML_LOGS_FILE_PATH.setter
    def ML_LOGS_FILE_PATH(self, value):
        self._ML_LOGS_FILE_PATH = value
