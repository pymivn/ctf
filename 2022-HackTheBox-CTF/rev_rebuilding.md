# rev_rebuilding

```
score: 300
solved: xx/xx
difficulty: easy
tags: re
```

## Problem
[file](./rebuilding)

## Got the flag
Decompile the binary in Ghidra, we see the code would xor the decrypted bytes
with user input value - len 6 chars.

![ghidra](./rebuilding.jpeg)

Open with radare2: r2 rebuilding, aaaa, afl, s main, pdf:

```asm
│     ╎││   0x00000964      488d05b50620.  lea rax, qword obj.encrypted ; 0x201020 ; ")8+\x1e\x06B\x05]\a\x021B\x0f3\nU"
```

Before xor, the code load an object with values "humans":

```asm
│     ╎││   0x00000991      488d05a90620.  lea rax, qword obj.key      ; 0x201041 ; "humans"
│     ╎││   0x00000998      0fb60402       movzx eax, byte [rdx + rax]
│     ╎││   0x0000099c      31c6           xor esi, eax
```

But xor it with the obj.encrypted didn't give the flag. After stucking for awhile,
we try to run it with pwndbg, before xor, the value loaded is "aliens", not
"humans". Xor "aliens" with the encrypted, we got the flag.
