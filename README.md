# When Pythonistas meet 1337 H4x0r
A collection of CTF write-up by [PYMI team](https://ctftime.org/team/175619).

## Check-list tips
- Challenge desciptions may be **INTENDED** be misleading. A problem with "backup is important", may have no bug in backup part, just to be misleading.
- Double check code edge-cases.
- Use the same platform the challenge run on. E.g Docker, because there are different when using on different OSes, on Linux newline is `\n` on Windows is `\r\n`.
- Look from far before zooming in details. Some results may show up if look
from far, not close. Example: ASCII art, or this string `|][]¥°|_|7#][\\]X'/[](_):-:∂|/€|†` - it is [`DOYOUTHINKYOUHAVEIT`](https://www.dcode.fr/cipher-identifier).
- Normal browsers do not display non valid HTML, use curl/BurpSuite/requests/other programming clients...
- Reading used library source code to find special case, e.g URI in Java can use `url:file://` which by-pass the check for `startswith("file://")`, or Python `ipaddress` library allow `127.0.0.01` and treat it same as `127.0.0.1`.
- On web challenges, especially those with many solves, highly chance the exploit is simple such as server-side template injection (SSTI), not cracking AES 128 or find bug in JWT. Notice the (unusual) usage of template, or unnecessary passing secret around.
- Try some (3, 5) inputs, not only one. Luck matters. E.g CyberChef could not decode this `eJwrzy_Kji8oys9Ps81MTUkpT7FISTXLMC03tkw1M8uwAIoZphmkFVuYpWYAAGHLDyw=` (need remove = to work) but could do this `eJwrzy_Kji8oys9Psy1MSjQ2NDIwyzQysSg2TMtItchIMSlOzEwySzXIsEzJAABNuw6j`.

## Tools
### Cipher identifier
- https://gchq.github.io/CyberChef > Magic
- https://www.dcode.fr/cipher-identifier - turn off adblock first.

### Java decompilers
- http://www.javadecompilers.com/

### Binary, crypto
- [pwn](https://docs.pwntools.com/en/stable/)
### Other
- Kali on VirtualMachine (VirtualBox, VMWare...)
