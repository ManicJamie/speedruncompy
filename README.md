# Speedrun.com v2 API wrapper

A WIP python wrapper for speedrun.com's new backend API. This should also double as basic documentation for these endpoints.

I believe that where calls are paginated, parameter structure becomes `{params: {...}, page: 1}`. Only confirmed this for one endpoint so far, but would make a little sense.

## TODO:
Endpoints that should be documented:

- [ ] GetAuditLogList
- [ ] GetCommentable
- [x] GetCommentList (POST)
- [x] GetConversationMessages (POST)
- [x] GetConversations (POST)
- [x] GetForumList (POST)
- [x] GetForumReadStatus (POST)
- [x] GetGameData
- [x] GetGameLeaderboard2
- [x] GetGameRecordHistory
- [x] GetGameSettings (POST)
- [x] GetModerationGames (POST)
- [x] GetModerationRuns (POST)
- [x] GetNotifications (POST)
- [x] GetSearch
- [x] GetSession (POST)
- [ ] GetThemeSettings
- [ ] GetThread
- [ ] GetThreadReadStatus
- [x] GetUserBlocks (POST)
- [x] GetUserSettings (POST)
- [ ] PutAuthSignup (POST)
- [ ] PutCommentableSettings (POST)
- [ ] PutGameBoostGrant (POST)
- [ ] PutGameSettings (POST)
- [ ] PutRunAssignee (POST)
- [ ] PutRunSettings (POST)
- [ ] PutSessionPing (POST)
- [ ] PutThreadRead (POST)
