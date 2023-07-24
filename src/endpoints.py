from api import BaseRequest

class GetGameLeaderboard2(BaseRequest):
    def __init__(self, params=...) -> None:
        super().__init__("GetGameLeaderboard2", params, method="GET")