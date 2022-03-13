# Binomial Ways
```
score: 215
solved: xx/142
difficulty: NA
tags: python, crypto
```

## Problem

```
There is only one way! The binomial way!

Download link: challenge.py
Download link: output.txt
Flag format: 1337UP{}
Created by Shyam Sunder Saravanan
```

```py
from secret import flag
val = []
flag_length = len(flag)
print(flag_length)

def factorial(n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f

def series(A, X, n):
    nFact = factorial(n)
    for i in range(0, n + 1):
        niFact = factorial(n - i)
        iFact = factorial(i)
        aPow = pow(A, n - i)
        xPow = pow(X, i)
        val.append(int((nFact * aPow * xPow) / (niFact * iFact)))

A = 1; X = 1; n = 30
series(A, X, n)
ct = []
for i in range(len(flag)):
    ct.append(chr(ord(flag[i])+val[i]%26))
print(''.join(ct))
```

Output
```
31
27F;VPbAs>clu}={9ln=_o1{0n5tp~
```

## Got the flag
It's just reverse each steps to get the original flag. `series` with a fixed
arguments, means `val` list is static.
With known `val`, we can get flag:

```py
ct = '27F;VPbAs>clu}={9ln=_o1{0n5tp~'
print(len(ct))
ns = [ord(i) for i in ct]
fs = []
for i in range(len(ns)):
    fs.append(ns[i]-val[i]%26)
print(''.join([chr(i) for i in fs]))

# 1337UPUAf>Vlh{(o$ja=Ro${#n4p]z
```

output now contains the flag prefix `1337UP` but the remain looks not right.
The output string has only 30 chars, while the flag has 31 chars as hinted in
the output file. So 1 char is missing. Why a char is missing? it may because
it is not an "printable" ASCII value, thus it outputs "empty".

We just bruteforce some non printable characters, insert it in each position from
pre-output list:

```py
for i in range(6, 32):
    # char that looks like empty
    for ordinal in range(127, 161):
        ps = ns[:]
        ps.insert(i, ordinal)
        fs = []
        for i in range(len(ps)):
            fs.append(ps[i]-val[i]%26)
        maybe = (''.join([chr(i) for i in fs]))
        # if '_b1n0m1al}' in maybe:
        #     print(maybe)
        if maybe.startswith('1337UP{') and maybe.endswith("}"):
            print(maybe)
            exit()
```

We got many output, some looks like

```
1337UPUAf>Vlh{(o$ja=Ro${#n4p]z
1337UPrb4s1c_sh1f7_n0_b1n0m1al}
1337UPU4s1c_sh1f7_n0_b1n0m1al}
1337UPUArs1c_sh1f7_n0_b1n0m1al}
1337UPUAf1c_sh1f7_n0_b1n0m1al}
1337UPUAf>rc_sh1f7_n0_b1n0m1al}
1337UPUAf>V_sh1f7_n0_b1n0m1al}
1337UPUAf>Vlrsh1f7_n0_b1n0m1al}
1337UPUAf>Vlh}h1f7_n0_b1n0m1al}
```

that looks like flag, we added

```py
        if '_b1n0m1al}' in maybe:
            print(maybe)
```
to above code to get a shorter list, then manually change
`1337UPrb4s1c_sh1f7_n0_b1n0m1al}`

r to { and got the flag `1337UP{b4s1c_sh1f7_n0_b1n0m1al}` .

## Conclusion
We got some **luck** here but if that not work out, try full range of ASCII
would sure get the flag.
