def polinom(n, m):
    i = 0
    z = []
    s = 0
    while n > 0:
        if n % 2 != 0:
            z.append(2 - (n % 4))
        else:
            z.append(0)

        n = (n - z[i])//2
        i = i + 1

    z = z[::-1]
    l = len(z)
    for i in range(0, l):
        s += z[i] * m ** (l - 1 - i)
    return s

m = {}
r = '242712673639869973827786401934639193473972235217215301'

for i in range(100):
    if len(str(i)) == 1:
        m[str(polinom(i, 3))] = f"0{i}"
    else:
        m[str(polinom(i, 3))] = i

rs = []
def find_flag(r, result=None):
    #print("r", r)
    if result is None:
        result = []
    if len(r) == 0:

        if result[::-1] not in rs:
            #print(result[::-1])

            rs.append(result[::-1])
        return

    possible = []
    for i in range(1, 5):
        check = r[-i:]

        if check in m:
            possible.append(check)
    #print("pos", possible)
    for c in possible:

        find_flag(r[:len(r)-len(c)], result + [m[c]])



find_flag(r)
print(rs)

flags = []
print(r)
for i in rs:
    n = int("".join([str(c) for c in i]))
    flags.append(n)

print(flags)

for f in flags[:]:
    if str(f).endswith("01"):
        flags.append(int(str(f)[:-2] +  "1"))

import binascii
for i in flags:
    try:
        print(binascii.unhexlify(hex(i)[2:]))
    except Exception:
        pass
