Attempt login. Note this is the only POST that appears to be accessible without a PHPSESSID.

# Parameters
- name
- password
- token (OPT; 2fa sent after successful password auth)

# Response
Successful login response includes a set-cookie header with appropriate PHPSESSID;
`PHPSESSID=xxxx; Path=/; Domain=speedrun.com; Expires=Tue, 23 Jul 2024 22:52:09 GMT; HttpOnly`
### Content
```
loggedIn
tokenChallengeSent
```