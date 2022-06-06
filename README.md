# When Pythonistas meet 1337 H4x0r
A collection of CTF write-up by [PYMI team](https://ctftime.org/team/175619).

## Check-list tips
- Challenge desciptions may **INTENDED** be misleading. A problem with "backup is important", may have no bug in backup part, just to be misleading. So does the difficulty, "easy" one maybe hard and "hard" one may be easy.
- Low-effort solutions (5-10 mins) should be tried what-so-ever. Over-thinking
is a problem. E.g: a problem gives 3000 pictures and ask to find unique one. Using hash of image can easily solve, but
if after viewing some images and see they are differents noises images, one
could think the real one is uniq real photo has content and use object
recognition (deep learning) to solve is way over thinking, and wrong.
- Again, low effort methods should be tried, e.g XOR with 6 first chars of flag
  while easy, could be solution (and no tool can auto-decrypt that)
- When writing code search for flag (e.g in many webpages), the flag may start with `sdctf`,
  but as nothing says flag would in the pages, try check shorter word, e.g
  `sdc` is the domain name of the CTF site.
- Double check code edge-cases.
- Use the same platform the challenge run on. E.g Docker, because there are different when using on different OSes, on Linux newline is `\n` on Windows is `\r\n`.
- Look from far before zooming in details. Some results may show up if look
from far, not close. Example: ASCII art, or this string `|][]¥°|_|7#][\\]X'/[](_):-:∂|/€|†` - it is [`DOYOUTHINKYOUHAVEIT`](https://www.dcode.fr/cipher-identifier).
- Normal browsers do not display non valid HTML, use curl/BurpSuite/requests/other programming clients...
- Reading used library source code to find special case, e.g URI in Java can use `url:file://` which by-pass the check for `startswith("file://")`, or Python `ipaddress` library allow `127.0.0.01` and treat it same as `127.0.0.1`.
- On web challenges, especially those with many solves, highly chance the exploit is simple such as server-side template injection (SSTI), not cracking AES 128 or find bug in JWT. Notice the (unusual) usage of template, or unnecessary passing secret around.
- Try some (3, 5) inputs, not only one. Luck matters. E.g CyberChef could not decode this `eJwrzy_Kji8oys9Ps81MTUkpT7FISTXLMC03tkw1M8uwAIoZphmkFVuYpWYAAGHLDyw=` (need remove = to work) but could do this `eJwrzy_Kji8oys9Psy1MSjQ2NDIwyzQysSg2TMtItchIMSlOzEwySzXIsEzJAABNuw6j`.
- When see a command `git commit -m 'abc'`, ask first question: what this does
  then ask again: what else can happen when this run (git hook).

## Problem categories
### Crypto
- Classic crypto are all solved problems. It's more to find "what it is" then use
tool to solve it, than to find "how to solve it".
- Modern crypto might requires thinking, reading papers/blogs, guessing a lot, e.g
RSA/ECC.

### Web
Find flag hiding somewhere just need to think differently to find:
- (s/d/c/t/f on URL),
- or in robots.txt
- or in many files then some "secret" hide
- "leaked" in source code (HTML) or git "deleted" secrets.

Bypass mechanism, real hacking: harder, need to understand mechanism or source code
etc...
### Forensics
- Corrupted files: use tools or write code to fix headers
- Hidden files: read file headers to find hidden files, use tools.

## Tools
### Cipher identifier
- https://gchq.github.io/CyberChef > Magic
- https://www.dcode.fr/cipher-identifier - turn off adblock first.
- https://www.boxentriq.com/code-breaking/cipher-identifier

### Online decompilers
- Java/Python/Lua/C# decompilers https://www.decompiler.com/
- Java http://www.javadecompilers.com/
- Binary https://binary.ninja/

### Offline decompilers
- radare2 & Cutter UI
- ghidra

### Android tools
- anbox for emulator
- adbcat to view log

### Generate shellcode (asm)
- pwnlib.asm (belongs to pwntools)

### Binary, crypto
- [pwn](https://docs.pwntools.com/en/stable/)

### Re
- angr to "auto" solve re challs

### Other
- Kali on VirtualMachine (VirtualBox, VMWare...) because its repo has many
tools that not available on Ubuntu repo. E.g ghidra

### Forensics
- https://gchq.github.io/CyberChef - can find hidden files base on magic headers,
choose specific type (image/audio...) to find more accurate.
- binwalk - note sometimes binwalk may not work (e.g to find hidden jpeg image)

### OSINT
- https://github.com/sherlock-project/sherlock - run this by
  `python3 sherlock USERNAME --print-all --timeout 10` to see which sites failed/blocked, set timeout to not stuck forever (e.g TikTok may fail). NOTE: this not search discord, so search in discord manually.
- https://github.com/mxrch/ghunt - investigate google accounts
