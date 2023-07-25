# Speedrun.com v2 API wrapper

A WIP python wrapper for speedrun.com's new backend API. This should also double as basic documentation for these endpoints.

I believe that where calls are paginated, parameter structure becomes `{params: {...}, page: 1}`. Only confirmed this for one endpoint so far, but would make a little sense.

## TODO:
Enums that need to be documented:
- itemType (eg. GetCommentable)

Endpoints that should be documented:

- [ ] GetAuditLogList
- [x] GetCommentable (POST)
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
- [x] GetRunSettings (POST)
- [x] GetSearch
- [x] GetSession (POST)
- [x] GetThemeSettings (POST)
- [ ] GetThread
- [x] GetThreadReadStatus (POST)
- [x] GetUserBlocks (POST)
- [x] GetUserSettings (POST)
- [x] PutAuthSignup (POST)
- [x] PutAuthLogin (POST)
- [x] PutAuthLogout (POST)
- [x] PutCommentableSettings (POST)
- [ ] PutGameBoostGrant (POST)
- [x] PutGameSettings (POST)
- [x] PutRunAssignee (POST)
- [x] PutRunSettings (POST)
- [x] PutSessionPing (POST)
- [x] PutThreadRead (POST)

Please note that any documented endpoints are documented entirely by trial & error. They may be missing potential arguments, or edge response cases.
