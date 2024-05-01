# Speedrun.com v2 API wrapper

A WIP python wrapper for speedrun.com's new backend API.

WIP documentation for the API can be found in [speedruncom-apiv2-docs](https://github.com/ManicJamie/speedruncom-apiv2-docs)

## Usage
`pip install speedruncompy`, then `import speedruncompy`.

Default namespace contains all endpoints. Login flow in `speedruncompy.auth`. Other notable fields include `enums` and `exceptions`. `data_structures` is currently unused, but may be useful to help construct common data structures.

## Authorisation
Note that this uses the API in the same way as https://speedrun.com. The v2 API does not currently accept the Bearer token the v1 API can use - but v2 is also not half-broken, and contains most of the new features SRC has added over the years.

As such, authorisation requires your username & password (and 2FA token). ***This means logging in requires a massive leap of trust***, and so I encourage you to [inspect the auth module](src/speedruncompy/auth.py), and if you're very concerned consider either changing your SRC password or manually get an authed PHPSESSID with your own requests, then use `auth.loginSESSID`. 

## Omissions
Admin-only endpoints will not be added due to lack of testability and usability. These include:
- GetAdminStatusSummary
- GetTicketQueueCounts
- GetTicketStatusCounts
- PutGameDelete

## Goals
Future versions will aim to assist further in development;
- Complete datatype coverage & testing to detect regressions & SRC-side additions
- Document more enums
- Convenience properties potentially exploiting cached data?