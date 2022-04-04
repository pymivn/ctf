# !pip install pwntools
import pwn
import time
import string


def try_pad(pad):

    c = pwn.connect("0.cloud.chals.io", 27602)
    c.readline()
    c.readuntil("Enter pad >")

    c.sendline(pad.encode("utf-8"))
    time.sleep(2)
    # c.readline()
    s = c.readline()
    return s.decode("utf-8"), c


i = 0
j = 0
while True:
    first = string.ascii_uppercase[i : i + 20]
    if len(first) < 20:
        break

    while True:

        second = string.ascii_lowercase[j : j + 18]
        if len(second) < 18:
            i = i + 1
            print("NEW ", i)
            j = 0
            break

        pad = first + second[::-1]
        r, c = try_pad(pad)

        print("try", pad, "result", r)
        if "keep fighting" in r:
            j = j + 1
        else:
            print(r)
            c.interactive()
