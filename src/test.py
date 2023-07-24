import api as api

print("WARN: This tool should only be used for testing purposes")

params = {"params":{"categoryId":"02q8o4p2","emulator":0,"gameId":"76rqmld8","obsolete":0,"platformIds":[],"regionIds":[],"timer":0,"verified":1,"values":[{"variableId":"yn2p3085","valueIds":["81w7r6vq"]}],"video":0},"page":1}

r = api.doRequest("GetGameLeaderboard2", params=params)
print(r.request.url)

print(r.content)