# Equality

```
score: 271
solved: xx/104
difficulty: NA
tags: crypto, RSA
```

## Problem

```
Perfectly balanced, as all things should be!

Download link: equality.txt
Flag format: 1337UP{}
Created by Piyush Paliwal
```

```txt
{â€™nâ€™ = â€˜0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875â€™, â€˜eâ€™ = â€˜0x3045â€™, â€˜ctâ€™ = â€˜0x5d1e39bc751108ec0a1397d79e63c013d238915d13380ae649e84d7d85ebcffbbc35ebb18d2218ccbc5409290dfa8a4847e5923c3420e83b1a9d7aa67190dc0d34711cce261665c64c28ed2834394d4b181926febf7eb685f9ce81f36c7fb72798da3a14a123287171d26e084948aab0fba81c53f10b5696fc291006254ee690â€™}

{â€™nâ€™ = â€˜0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875â€™, â€˜eâ€™ = â€˜0xff4dâ€™, â€˜ctâ€™ = â€˜0x3d90f2bec4fe02d8ce4cece3ddb6baed99337f7e6856eef255445741b5cfe378390f058679d70236e51be4746db4c207f274c40b092e24f8c155a0957867e84dca48e27980af488d2615a280c6eadec2f1d30b95653b1ee3135e2edff100dd2c529994f846722f811348b082d0bec7cfab579a4bd0ab789928b1bebed68d628fâ€™}
```
## Got the flag
Removing all "equal" parts from both sides we got two set values of n, e, ct.
This is an RSA problem, with `n` `e` and `ct`

It's not 100% equal, e.g we see `™n = ˜0xa62...` in the first set, we not sure
what is correct way they remove it, we just remove these TM and ~ part and try.

```py
n = 0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875
e1 = 0x3045
ct1 = 0x5d1e39bc751108ec0a1397d79e63c013d238915d13380ae649e84d7d85ebcffbbc35ebb18d2218ccbc5409290dfa8a4847e5923c3420e83b1a9d7aa67190dc0d34711cce261665c64c28ed2834394d4b181926febf7eb685f9ce81f36c7fb72798da3a14a123287171d26e084948aab0fba81c53f10b5696fc291006254ee690

n = 0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875
e = 0xff4d
ct2 = 0x3d90f2bec4fe02d8ce4cece3ddb6baed99337f7e6856eef255445741b5cfe378390f058679d70236e51be4746db4c207f274c40b092e24f8c155a0957867e84dca48e27980af488d2615a280c6eadec2f1d30b95653b1ee3135e2edff100dd2c529994f846722f811348b082d0bec7cfab579a4bd0ab789928b1bebed68d628f
```

We have same `n`, different normal `e` and different ct1 ct2.
Searching for cracking RSA same n different e, we got [https://crypto.stackexchange.com/a/1616/12448](https://crypto.stackexchange.com/a/1616/12448), which says: there will be a and b such that `ae1 + be2 == 1`,
then get the message by `m ≡ c1**a * c2**b (modn)`

Solve this by hand or use Z3, we got a solution:

```py
import z3
a, b = z3.Ints('a b')
solver = z3.Solver()
solver.add(12357 * a + 65357 * b == 1)
solver.check()
solver.model()
```

[b = -1747, a = 9240]

```py
flag = pow(ct1, 9240, n) * pow(ct2,  -1747, n) % n
from Crypto.Util.number import long_to_bytes
long_to_bytes(flag)
```

got the flag `b'1337UP{c0mm0n_m0dulu5_4774ck_15_n07_50_c0mm0n}'`
