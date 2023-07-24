## Required Parameters
- query

## Optional Parameters
- limit = 500 `max 500`
- includeGames = false
- includeNews = false
- includePages = false
- includeSeries = false
- includeUsers = false

# Response
```
gameList[]
    id
    name
    url
    type
    loadtimes
    milliseconds
    igt
    verification
    autoVerify
    requireVideo
    emulator
    defaultTimer
    validTimers[]
    releaseDate
    addedDate
    touchDate
    coverPath
    trophy1stPath
    trophy2ndPath
    trophy3rdPath
    runCommentsMode
    runCount
    activePlayerCount
    totalPlayerCount
    boostReceivedCount
    boostDistinctDonorsCount
    rules
    viewPowerLevel
    platformIds[str]
    regionIds[]
    gameTypeIds[]
    websiteUrl
    discordUrl
    defaultView
    guidePermissionType
    resourcePermissionType
    staticAssets[]
        assetType
        path
newsList[]
    id
    slug
    title
    summary
    body
    userId
    createDate
    updateDate
    publishDate
    publishTarget
    publishTags[str]
    coverImagePath
    commentsCount
pageList[]
    id
    slug
    title
    summary
    body
    userId
    createDate
    updateDate
    publishDate
    publishTarget
    publishTags[]
    commentsCount
seriesList[]
    id
    name
    url
    addedDate
    touchDate
    websiteUrl
    discordUrl
    runCount
    activePlayerCount
    totalPlayerCount
    officialGameCount
    staticAssets[]
        assetType
        path
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
```