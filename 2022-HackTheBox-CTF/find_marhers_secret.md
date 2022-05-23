# Find Marher's Secret

```
score: 300
solved: xx/xx
difficulty: easy
tags: crypto, FMS, RC4
```

## Problem

[code](./fms.py)

```py
def encrypt(key, iv, pt):
    return ARC4.new(iv + key).encrypt(pt).hex()
```

The encryption uses RC4 cipher, and allow use to control the iv.
After some research, this seems the flaw that used to crack Wifi WEP, which
was so... classic. The algorithm called "FMS", also hinted in the chall title.

We found a PoC attack [here](https://github.com/jvdsn/crypto-attacks/tree/master/attacks/rc4), modified it to send IV to server and feed the result into the attack algorithm.

```
from pwn import *

import json
def create_payload(iv, p):
    payload = {'option': 'encrypt',
        'iv': bytes(iv).hex(),
               'pt': bytes(p).hex()}
    r =  json.dumps((payload))
    return r


def oracle(iv, p):
    r = c.readuntil(b'Claim the key.\n')
    print(r)
    pl= create_payload(
        iv,
        p
    )
    print(pl)
    c.sendline(pl)
    r = c.readline()

    return bytes.fromhex(json.loads(r.decode()[2:].strip())['ct'])

#c = connect("localhost", 1337)
c = connect('178.62.73.26',31947)
r = attack(oracle, 27)
key = bytes(r).hex()
print(key)
payload = {'option': 'claim', 'key':key }
p =  json.dumps((payload))
r = c.readuntil(b'Claim the key.\n')
print(r)
c.sendline(p)
print(c.readline())
```

After about 10 minutes running, we got the flag.

`HTB{f1uhr3r_m4n71n_p1u5_5h4m1r_15_4_cl4ss1c_0n3!!!}`
