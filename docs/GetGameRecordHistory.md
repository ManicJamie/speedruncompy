Parameters are wrapped inside `params`, except `page`.

# Parameters (some may be opt.)
- categoryId
- emulator
- gameId
- obsolete
- platformIds[]
- regionIds[]
- timer
- verified
- values[]
    {variableId, valueIds[]}
- video
- page

# Response
```
playerList[]
    id
    name
    url
    powerLevel
    color1Id
    color2Id
    colorAnimate
    areaId
runList[]
    id
    gameId
    categoryId
    time
    timeWithLoads
    platformId
    emulator
    video
    comment
    submittedById
    verified
    verifiedById
    date
    dateSubmitted
    dateVerified
    hasSplits
    issues
    playerIds[str]
    valueIds[str]
```