# Parameters
- conversationId
- markAsRead

# Response
```
conversation
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
messages[]
    id
    conversationId
    userId
    text
    date
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
userBlocks[]
```