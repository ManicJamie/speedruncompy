from api import GetRequest, PostRequest

"""
GET requests are all unauthed & do not require PHPSESSID.
"""

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

"""
POST requests may require auth
"""

class PutAuthLogin(PostRequest):
    def __init__(self, name, password, token=None, **params) -> None:
        params["name"] = name
        params["password"] = password
        params["token"] = token
        super().__init__("PutAuthLogin", **params)

class PutAuthLogout(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("PutAuthLogout", **params)

class GetSession(PostRequest):
    def __init__(self, **params) -> None:
        super().__init__("GetSession", **params)