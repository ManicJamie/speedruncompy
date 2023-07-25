from api import GetRequest, PostRequest, LoginRequest, AuthedRequest

class GetGameLeaderboard2(GetRequest):
    def __init__(self, gameId, categoryId, **params: str) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        if page is not None: 
            param_construct["page"] = page
        super().__init__("GetGameLeaderboard2", **param_construct)

class GetGameData(GetRequest):
    def __init__(self, gameId, **params) -> None:
        params["gameId"] = gameId
        super().__init__("GetGameData", **params)

class GetGameRecordHistory(GetRequest):
    def __init__(self, gameId, categoryId, **params) -> None:
        page = params.pop("page", None)
        param_construct = {"params": {"gameId": gameId, "categoryId": categoryId}}
        param_construct["params"].update(params)
        if page is not None: 
            param_construct["page"] = page
        super().__init__("GetGameLeaderboard2", **param_construct)

class GetSearch(GetRequest):
    def __init__(self, query, **params) -> None:
        params["query"] = query
        super().__init__("GetSearch", **params)