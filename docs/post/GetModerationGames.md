Gets games moderated by this user

# Parameters
- includeAll
- includeGameUrls

# Response
```
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
gameModerationStats[]
    gameId
    state
    count
    minDate
    maxDate
```