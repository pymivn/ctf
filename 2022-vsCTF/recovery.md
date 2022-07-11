# Recovery

```
score: 357
solved: xx/163
difficulty: easy
tags: crypto, python
```

## Problem

I forgot the password to the View Source flag vault! Thankfully, I still have
access to the password checker. Can you help me recover my password?

![PassChecker2000.py](./recovery.py)

## Got the flag
The only function used to validate password does 3 checks, our goal is
to make it return True, means, pass 3 checks.

```py
def validate(password: str) -> bool:
    if len(password) != 49:
        return False

    key = ['vs'.join(str(randint(7, 9)) for _ in range(ord(i))) + 'vs' for i in password[::-2]]
    gate = [118, 140, 231, 176, 205, 480, 308, 872, 702, 820, 1034, 1176, 1339, 1232, 1605, 1792, 782, 810, 1197, 880,
            924, 1694, 2185, 2208, 2775]
    if [randint(a, b[0]) for a, b in enumerate(zip(gate, key), 1) if len(b[1]) != 3 * (b[0] + 7 * a) // a]:
        return False

    hammer = {str(a): password[a] + password[a + len(password) // 2] for a in range(1, len(password) // 2, 2)}
    block = b'c3MxLnRkMy57XzUuaE83LjVfOS5faDExLkxfMTMuR0gxNS5fTDE3LjNfMTkuMzEyMS5pMzIz'
    if b64encode(b'.'.join([((b + a).encode()) for a, b in hammer.items()])) != block:
        return False

    return True
```

Firstly, password must has length of 49
```py
    if len(password) != 49:
        return False
```

Secondly, it must not return False here

```py
key = ['vs'.join(str(randint(7, 9)) for _ in range(ord(i))) + 'vs' for i in password[::-2]]
gate = [118, 140, 231, 176, 205, 480, 308, 872, 702, 820, 1034, 1176, 1339, 1232, 1605, 1792, 782, 810, 1197, 880,
        924, 1694, 2185, 2208, 2775]
if [randint(a, b[0]) for a, b in enumerate(zip(gate, key), 1) if len(b[1]) != 3 * (b[0] + 7 * a) // a]:
    return False
```

This is a great example of when list comprehension be over-used/abused, the
code become hard to read.

To not return False, the condition after if must be an empty list.

```py
[randint(a, b[0]) for a, b in enumerate(zip(gate, key), 1) if len(b[1]) != 3 * (b[0] + 7 * a) // a]
```

means all the items have to fail the condition `if len(b[1]) != 3 * (b[0] + 7 * a) // a`,
or, all of them must satisfy `len(b[1]) == 3 * (b[0] + 7 * a) // a`.

`for a, b in enumerate(zip(gate, key), 1)`, a is index, starts from 1,
b is a tuple of nth elements from gate and key, thus, b[0] is value from gate,
b[1] is value from key. Since we have b[1] (from gate) and a, we can calculate b[0]
to recover password[::-2].

```py
password = [None] * 49
half = [chr(3 * (g + 7 * a) // a //3) for a, g in enumerate(gate, 1)]
password[::-2] = half
print(''.join([k if k else '_' for k in password]))
# v_c_f_T_3_3_F_4_5_w_r___n_i_e_Y_U_t_3_W_0_3_T_M_}
```

We can see `vsctf{...}` format of the password, now get the other half:

```py
hammer = {str(a): password[a] + password[a + len(password) // 2] for a in range(1, len(password) // 2, 2)}
block = b'c3MxLnRkMy57XzUuaE83LjVfOS5faDExLkxfMTMuR0gxNS5fTDE3LjNfMTkuMzEyMS5pMzIz'
if b64encode(b'.'.join([((b + a).encode()) for a, b in hammer.items()])) != block:
    return False
```

to make the condition not return False,
`b64encode(b'.'.join([((b + a).encode()) for a, b in hammer.items()])) == block`
or `[((b + a).encode()) for a, b in hammer.items()] = b64decode(block).split(b'.')`

```py
import base64
ps = base64.b64decode(block).split(b'.')
# [b'ss1', b'td3', b'{_5', b'hO7', b'5_9', b'_h11', b'L_13', b'GH15', b'_L17', b'3_19', b'3121', b'i323']
```

each element created by concatenate string b and a, which is value + key from hammer dict.
Having each value are string of 2 chars: `password[a] + password[a + len(password) // 2]`,
the remain is the index acts as key,
we take out that value and key from the above list:

```py
hammer = {i[2:]: i[:2] for i in ps}
# {b'1': b'ss', b'3': b'td', b'5': b'{_', b'7': b'hO', b'9': b'5_', b'11': b'_h', b'13': b'L_', b'15': b'GH', b'17': b'_L', b'19': b'3_', b'21': b'31', b'23': b'i3'}
```

Rebuilding odd-th elements of password:

```py
for k, v in hammer.items():
    i = int(k)
    first, second = v
    password[i] = chr(first)
    password[i+plen//2] = chr(second)

print(''.join(password))
```

Full solving code at [recovery_sol.py](./recovery_sol.py)

We got the flag: `vsctf{Th353_FL4G5_w3r3_inside_YOU_th3_WH0L3_T1M3}`.
