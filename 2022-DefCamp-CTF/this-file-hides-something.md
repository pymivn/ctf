# this-file-hides-something

```
author: Volf
score: 50
solved: 89/94
difficulty: medium
tags: forensics
```

## Description

There is an emergency regarding this file. We need to extract the password ASAP. It's a crash dump, but our tools are not working. Please help us, time is not on our side.

PS: Flag format is not standard.

## Got the flag

Because a provided file is crash "dump", we try opening by Volatility. Volatility is a memory forensics tool. 

We found profile of this file using command
```
volatility -f crashdump.elf imageinfo
```
Output
```
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : VirtualBoxCoreDumpElf64 (Unnamed AS)
                     AS Layer3 : FileAddressSpace (D:\DOCUMENT\RESEARCH\CTF\DefCamp\crashdump.elf)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf80002831120L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002833000L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2022-02-06 11:04:38 UTC+0000
     Image local date and time : 2022-02-06 03:04:38 -0800
```

Using LSAdump plugin to extract credential
```
volatility -f crashdump.elf --profile=Win7SP1x64 lsadump

Volatility Foundation Volatility Framework 2.6
DefaultPassword
0x00000000  1c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x00000010  53 00 74 00 72 00 30 00 6e 00 67 00 41 00 73 00   S.t.r.0.n.g.A.s.
0x00000020  41 00 52 00 30 00 63 00 6b 00 21 00 00 00 00 00   A.R.0.c.k.!.....

DPAPI_SYSTEM
0x00000000  2c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ,...............
0x00000010  01 00 00 00 26 db 41 81 81 b7 74 99 0d b8 a0 2a   ....&.A...t....*
0x00000020  0d 0f 0e d0 92 6b 77 1d 64 73 ab 60 47 1e 07 07   .....kw.ds.`G...
0x00000030  ab a8 fa dd 57 f3 6b 51 2e 0a 4f 79 00 00 00 00   ....W.kQ..Oy....
```
Flag is Str0ngAsAR0ck!
## Conclusion

This challenge introduces how to use tool to extract credentials from Windows Local Security Authority (LSA)


