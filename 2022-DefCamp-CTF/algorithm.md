# algorithm

```
author: T3jv1l
score: 50
solved: xx/94
difficulty: medium
type: Reverse Engineering, Cryptography
```

## Problem
Hello friends. Just a regular algorithm

Flag format: `CTF{sha256(message_decrypt)}`

Given a python2 code file in chall.py

```py
flag = ' [test]'
hflag = flag.encode('hex')
iflag = int(hflag[2:], 16)

def polinom(n, m):
   i = 0
   z = []
   s = 0
   while n > 0:
    if n % 2 != 0:
     z.append(2 - (n % 4))
    else:
     z.append(0)
    n = (n - z[i])/2
    i = i + 1
   z = z[::-1]
   l = len(z)
   for i in range(0, l):
       s += z[i] * m ** (l - 1 - i)
   return s

i = 0
r = ''
while i < len(str(iflag)):
   d = str(iflag)[i:i+2]
   nf = polinom(int(d), 3)
   r += str(nf)
   i += 2

print r
# r = '242712673639869973827786401934639193473972235217215301'
```

it output `r = '242712673639869973827786401934639193473972235217215301'`, find the flag used.

## Got the flag

The code file used Python2 - which is deprecated since 2020, thus in solution, we use Python3 instead.
The main different is: instead of `/` we would use `//`, and instead of `print message`, we would use `print(message)`.

The algorithm creates a string `r` by iterating through the integer `iflag` by each 2 characters, and transforms that 2 characters to some other characters using `polinom` function.

The `polinom` function takes 2 inputs `n=int(d), m=3`, and do some calculations we dont' need go into details.

Given that m is hardcoded = 3, and n is number with 1 to 2 digits, we can create all possible transformshere. From 00, 01.. to 99. Notice that `01` would be convert to `1` before called by `polinom`

```py
m = {}
for i in range(100):
    if len(str(i)) == 1:
        m[str(polinom(i, 3))] = f"0{i}"
    else:
        m[str(polinom(i, 3))] = i
```

This `m` dictionary is a reverse output to input of polinom function. Print the `m` dictionary, we can see that output of polinom may have 1, 2, 3 or 4 characters.

To reverse `r = '242712673639869973827786401934639193473972235217215301'`, to it source, it needs to try all possible group of output. E.g:

`2427` could be `24` and `27`, or `242` and `7`, or `2` and `427`,...

As `r` was created left-to-right, in reverse, we do from right-to-left. This function used DFS (depth first search) algorithm to collect all possible cases into `rs`:

```py
rs = []

def find_flag(r, result=None):
    if result is None:
        result = []

    if len(r) == 0:
        if result[::-1] not in rs:
            rs.append(result[::-1])
        return

    possible = []
    for i in range(1, 5):
        check = r[-i:]

        if check in m:
            possible.append(check)

    for c in possible:
        find_flag(r[:len(r)-len(c)], result + [m[c]])

find_flag(r)
print(rs)
```

This found all input combinations that can create the output `r`, since the algorithm used 2 digits **NOTE: except the last digit**, following code create all inputs number (iflag):

```py
flags = []
for i in rs:
    n = int("".join([str(c) for c in i]))
    flags.append(n)
```

This is important "twist", we always take 2 digits and input to `polinom` but if the number has odd digits, the last one would be 1 digits. Here converts all flags to new version where it has only one digit (no padding 0).

```py
for f in flags[:]:
    if str(f).endswith("01"):
        flags.append(int(str(f)[:-2] +  "1"))
```
1 because all possible flags ends with 1.

Now, reverse the original code to get the flag:

```py
flag = ' [test]'
hflag = flag.encode('hex')
iflag = int(hflag[2:], 16)
```

This is Python2 uses `str.encode('hex')`, in Python3, use `binascii.hexlify`.

`iflag = int(hflag[2:], 16)` => `hflag = hex(iflag)[2:]`

`hflag = flag.encode('hex')` => `flag = binascii.unhexlify(hflag)`

Do this to all possible iflag, got a readable output:

```py
import binascii
for i in flags:
    try:
        print(binascii.unhexlify(hex(i)[2:]))
    except Exception:
        pass
```

```py
...
b'#\xb6\x9d\xf2\x0fn\xcf\xf4@\xba\xe9\x12\x05\xf2\xde0l]'
b'[ola_th1s_1s_p0l]'
b'\x12\xd95j\xf0\x1c`\x9f\xb4*\xeag\x9fp0l]'
```

Get sha256 of `[ola_th1s_1s_p0l]`, got the flag.

Full code at ![here](algorithm.py).

## Conclusion
We solved this quite late due to missed the edge-case, the twist "all input are 2 digits maybe except the last one". In normal algorithm code, pay attention to edge-case, and in CTF, pay double attentions.
