# ss-puzzle

```
score: 100
solved: xx/221
difficulty: easy
tags: crypto, xor
```

## Problem

I had stored this FLAG securely in five separate locations. However, three of the shares were lost and one was partially broken. Can you restore flag?

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 64 bytes
FLAG = b'LINECTF{...}'

def xor(a:bytes, b:bytes) -> bytes:
    return bytes(i^j for i, j in zip(a, b))


S = [None]*4
R = [None]*4
Share = [None]*5

S[0] = FLAG[0:8]
S[1] = FLAG[8:16]
S[2] = FLAG[16:24]
S[3] = FLAG[24:32]

# Ideally, R should be random stream. (Not hint)
R[0] = FLAG[32:40]
R[1] = FLAG[40:48]
R[2] = FLAG[48:56]
R[3] = FLAG[56:64]

Share[0] = R[0]            + xor(R[1], S[3]) + xor(R[2], S[2]) + xor(R[3],S[1])
Share[1] = xor(R[0], S[0]) + R[1]            + xor(R[2], S[3]) + xor(R[3],S[2])
Share[2] = xor(R[0], S[1]) + xor(R[1], S[0]) + R[2]            + xor(R[3],S[3])
Share[3] = xor(R[0], S[2]) + xor(R[1], S[1]) + xor(R[2], S[0]) + R[3]
Share[4] = xor(R[0], S[3]) + xor(R[1], S[2]) + xor(R[2], S[1]) + xor(R[3],S[0])


# This share is partially broken.
Share[1] = Share[1][0:8]   + b'\x00'*8       + Share[1][16:24] + Share[1][24:32]

with open('./Share1', 'wb') as f:
    f.write(Share[1])
    f.close()

with open('./Share4', 'wb') as f:
    f.write(Share[4])
```

## Got the flag

Given share 1 and share 4, using xor to recover 7/8 parts of the flag. As A xor B == C then
C xor B == A, the S[0] is known and is `LINECTF{`, we can get R0, then S3, then S2 ...

```py
#Share[4] = xor(R[0], S[3]) + xor(R[1], S[2]) + xor(R[2], S[1]) + xor(R[3],S[0])
#Share[1] = xor(R[0], S[0]) + R[1]            + xor(R[2], S[3]) + xor(R[3],S[2])

share1 = open('Share1', 'rb').read()
share4 = open('Share4', 'rb').read()

S0 = b'LINECTF{'
R3 = xor(share4[-8:], S0)
S2 = xor(R3, share1[-8:])
R1 = xor(share4[8:16], S2)
R0 = xor(share1[:8], S0)
S3 = xor(R0, share4[:8])
R2 = xor(share1[16:24], S3)
S1 = xor(R2, share4[16:24])
S3 = xor(R2, share1[16:24])
print(S0 + S1 + S2 + S3 + R0 + R1 + R2 + R3)
```

We got the flag.
