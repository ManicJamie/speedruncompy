Gets conversations belonging to authed user.

# Response
```
conversations[]
    id
    participantUserIds[]
    lastMessageId
    lastMessageUser
    lastMessageText
    lastMessageDate
    readDate
participants[]
    conversationId
    userId
    joinedDate
    leftDate
users[]
    id
    name
    url
    powerLevel
    pronouns[str]
    areaId
    color1Id
    color2Id
    iconType
    onlineDate
    signupDate
    touchDate
    staticAssets[]
        assetType
        path
```