# Parameters
- itemId
- itemType
- page

# Response
```
commentable
    itemType
    itemId
    properties
        disabled
        locked
    permissions
        canManage
        canViewcomments
        canPostComments
        canEditComments
        canDeleteComments
        cannotViewReasons[str]
        cannotPostReasons[str]
commentList[]
    id
    itemType
    itemId
    date
    userId
    text
    parentId
    deleted
likeList[]
    itemType
    itemId
    userId
    date
userList[]
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
pagination
    count
    page
    pages
    per
```