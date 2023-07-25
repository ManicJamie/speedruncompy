Returns a list of world record runs, from lowest time to highest.

Parameters are wrapped inside `params`, except `page`.

Note that parameters gameId and categoryId are not required for a successful response, but without them the response will be empty. For this reason, this wrapper will consider them mandatory.

# Parameters (required)
- gameId
- categoryId

# Parameters (some may be opt.)
- values[]
    {variableId, valueIds[]}
- emulator
- obsolete
- platformIds[]
- regionIds[]
- timer
- verified
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