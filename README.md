# Speedrun.com v2 API wrapper

A WIP python wrapper for speedrun.com's new backend API. This should also double as basic documentation for these endpoints.

I believe that where calls are paginated, parameter structure becomes `{params: {...}, page: 1}`.

## TODO:
Endpoints that should be documented:

- [ ] GetSearch
- [ ] GetCommentList (POST)
- [ ] PutAuthSignup
- [ ] PutGameBoostGrant
- [x] GetGameData
- [ ] GetConversations
- [ ] GetNotifications
- [ ] GetModerationGames (POST)
- [ ] GetSession
- [ ] GetGameSettings
- [ ] PutGameSettings
- [ ] GetThemeSettings
- [ ] GetAuditLogList
- [ ] GetModerationRuns
- [ ] PutSessionPing (POST)
- [x] GetGameLeaderboard2
- [ ] GetGameRecordHistory
- [ ] GetConversationMessages
- [ ] GetForumList
- [ ] GetForumReadStatus
- [ ] GetThreadReadStatus
- [ ] GetCommentable
- [ ] PutThreadRead
- [ ] GetThread
- [ ] GetUserBlocks
- [ ] PutRunSettings
- [ ] PutRunAssignee