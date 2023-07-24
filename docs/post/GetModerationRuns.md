Get moderation data

# Parameters
- gameId
- limit
- page
- search
- verified
- verifiedById

# Response
```
categories[]
    id
    name
    url
    pos
    gameId
    isMisc
    isPerLevel
    numPlayers
    exactPlayers
    playerMatchMode
    timeDirection
    enforceMs
    archived
    rules
games[]
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
levels[]
    id
    gameId
    name
    url
    pos
    rules
    archived
pagination
    count
    page
    pages
    per
```