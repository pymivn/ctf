# JaWT that down!

```
score: 200
solved: xx/xx
difficulty: easy
tags: web
```

## Problem
```
The new ultra maximum security plugin I installed on my website is so good that even I can’t log in. Hackers don’t stand a chance.
Website https://jawt.sdc.tf/
```

https://github.com/acmucsd/sdctf-2022/tree/main/web/easy%20-%20jawt%20that%20down!

## Got the flag

Go to https://jawt.sdc.tf/login, read https://jawt.sdc.tf/js/login.js, we get login credentials (u: `AzureDiamond`, p: `hunter2`)
```js
render() {
        return r.createElement("form", {
            action: "/login",
            method: "POST",
            className: "login-form"
        }, r.createElement("span", {
            className: "heading"
        }, "Admin Sign In"), r.createElement("label", {
            htmlFor: "username",
            dangerouslySetInnerHTML: {
                __html: "\x3c!-- REMOVE ME IN PUBLISHED SITE! Username: AzureDiamond --\x3eUsername"
            }
        }), r.createElement("input", {
            type: "text",
            id: "username",
            name: "username"
        }), r.createElement("label", {
            htmlFor: "password",
            dangerouslySetInnerHTML: {
                __html: "\x3c!-- REMOVE ME IN PUBLISHED SITE! Password: hunter2 --\x3ePassword"
            }
        }), r.createElement("input", {
            type: "password",
            id: "password",
            name: "password"
        }), r.createElement("button", {
            type: "submit"
        }, "Sign In"))
    }
```

After logging in manually, there's a Flag url on the top nav (next to About): `https://jawt.sdc.tf/s`. This url must be accessed before `exp` in `jwt` cookie which is set to 2 seconds.

Response from `https://jawt.sdc.tf/s` is `d`. Tried going to `https://jawt.sdc.tf/s/d` (tried `https://jawt.sdc.tf/sd` first but 403), got `c`. So there need a script to get full flag:
```python
import requests
def login():
    s = requests.session()
    s.post("https://jawt.sdc.tf/login", data={"username": "AzureDiamond", "password": "hunter2"})
    return s


s = requests.session()
start = time.time()
url = "https://jawt.sdc.tf/s"
while True:
    r = s.get(url)
    if r.status_code != 200:
        s = login()
        continue
    url += f"/{r.text}"
    # print every url to get the satisfaction on the way
    print(url)
    if "}" in r.text:
        break
```

Final url: `https://jawt.sdc.tf/s/d/c/t/f/{/T/h/3/_/m/0/r/3/_/t/0/k/3/n/s/_/t/h/e/_/l/e/5/5/_/p/r/0/b/l/3/m/s/_/a/d/f/3/d/}`

So the flag is: `sdctf{Th3_m0r3_t0k3ns_the_le55_pr0bl3ms_adf3d}`
