from typing import Union, Any

class Datatype():
    def __repr__(self) -> str:
        return str(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value

class VariableValue(Datatype):
    def __init__(self, construct:Union[tuple[str, str], dict[str, str]]) -> None:
        if type(construct) is tuple:
            self.variableId = construct[0]
            self.valueId = construct[1]
        elif type(construct) is dict:
            self.variableId = dict.get("variableId", "")
            self.valueId = dict.get("valueId", "")
        
    def __str__(self):
        return f"Var {self.variableId} = {self.valueId}"

class RuntimeTuple(Datatype):
    def __init__(self, construct:Union[tuple[int, int, int, int], dict[str, int]]):
        if type(construct) is tuple:
            self.hour = construct[0]
            self.minute = construct[1]
            self.second = construct[2]
            self.millisecond = construct[3]
        elif type(construct) is dict:
            self.hour = construct.get("hour", 0)
            self.minute = construct.get("minute", 0)
            self.second = construct.get("second", 0)
            self.millisecond = construct.get("millisecond", 0)
    
    def __str__(self):
        return ("" if self.hour == 0 else f"{self.hour}:") + f"{self.minute:02}:{self.second:02}.{self.millisecond:03}" 

class RunSettings(Datatype):
    def __init__(self, dict:dict[str, Any] = {}) -> None:
        self.runId = dict.get("runId", "")
        self.gameId = dict.get("gameId", "")
        self.categoryId = dict.get("categoryId", "")
        self.playerNames: list[str] = dict.get("playerNames", [])
        self.time = RuntimeTuple(dict.get("time", (0,0,0,0)))
        self.platformId = dict.get("platformId", 0)
        self.emulator = dict.get("emulator", 0)
        self.video = dict.get("video", 0)
        self.comment = dict.get("comment", "")
        self.date = dict.get("date", "")
        self.values: list[VariableValue] = VariableValue(dict.get("values", []))