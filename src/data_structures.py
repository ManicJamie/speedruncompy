class VariableValue():
    variableId = ""
    valueId = ""

    def __init__(self, dict:dict = {}) -> None:
        self.variableId = dict.get("variableId")
        self.valueId = dict.get("valueId")

class RuntimeTuple():
    hour = 0
    minute = 0
    second = 0
    millisecond = 0

    def __init__(self, tuple:tuple[int]) -> None:
        self.hour = tuple[0]
        self.minute = tuple[1]
        self.second = tuple[2]
        self.millisecond = tuple[3]
    
    def __init__(self, dict:dict) -> None:
        self.hour = dict.get("hour")
        self.minute = dict.get("minute")
        self.second = dict.get("second")
        self.millisecond = dict.get("millisecond")
"""
class RunSettings():
    runId = ""
    gameId = ""
    categoryId = ""
    playerNames: list[str] = []
    time = (0, 0, 0, 0)
    platformId = 0
    emulator = 0
    video = 0
    comment = ""
    date = ""
    values: list[VariableValue] = []

    def __init__(self, dict:dict = {}) -> None:
        self.runId = dict.get("runId")
        self.gameId = dict.get("gameId")
        self.categoryId = dict.get("categoryId")
        self.playerNames: list[str] = dict.get("playerNames")
        self.time = dict.get("time")
        self.platformId = dict.get("platformId")
        self.emulator = dict.get("emulator")
        self.video = dict.get("video")
        self.comment = dict.get("cpmment")
        self.date = dict.get("date")
        self.values: list[VariableValue] = dict.get("values")
"""
class RunSettings():
    def __init__(self, dict:dict = {}) -> None:
        self.__dict__ = dict