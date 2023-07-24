Parameters are wrapped inside `params`, except `page`.

## Required parameters:
- gameID
- categoryID

## Optional parameters
- values[] TODO: document value structure
- video `0 = any, 1 = present, 2 = missing`
- verified
- timer
- obsolete
- platformIds[]
- regionIds[]
- page

# Response
```
runList [
    id
    gameId
    categoryId
    time (seconds)
    platformId
    emulator
    video
    comment
    submittedById
    verified
    verifiedById
    date
    dateVerified
    hasSplits
    obsolete
    place
    issues
    playersIds []
    valueIds []
]
playerList [
    id
    name
    url
    powerLevel (appears to be site admin? default 1, Meta is 4)
    color1Id
    color2Id
    colorAnimate
    areaId
    isSupporter
]
pagination
    count
    page
    pages
    per
```