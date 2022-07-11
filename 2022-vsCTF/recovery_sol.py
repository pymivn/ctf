import base64

gate = [118, 140, 231, 176, 205, 480, 308, 872, 702, 820, 1034, 1176, 1339, 1232, 1605, 1792, 782, 810, 1197, 880, 924, 1694, 2185, 2208, 2775]
block = b"c3MxLnRkMy57XzUuaE83LjVfOS5faDExLkxfMTMuR0gxNS5fTDE3LjNfMTkuMzEyMS5pMzIz"
plen = 49
password = [None] * plen
half = [chr(3 * (g + 7 * a) // a // 3) for a, g in enumerate(gate, 1)]
password[::-2] = half

ps = base64.b64decode(block).split(b".")

hammer = {i[2:]: i[:2] for i in ps}

for k, v in hammer.items():
    i = int(k)
    first, second = v
    password[i] = chr(first)
    password[i + plen // 2] = chr(second)

print("".join(password))
