# https://spaceheroes.ctfd.io/challenges

Rank: [#67](https://ctftime.org/event/1567)

## Write-ups
A themed with many easy + fun chals CTF.
Because we solved too many, we would write short write-ups in this file.

### starman - #osint
```
Starman - 100 - Easy

How far away from earth was the space car on January, 20 2021 at 1515 UTC? Enter distance in terms of Million Km. (Rounded to two decimals) (e.g shctf{12.34})

Wrap in shctf{}
```
Search for Starman, found [Where is Starman? Track Elon Musk's Tesla Roadster in ...](https://www.whereisroadster.com),
the site contains plots where it is, zoom the distance plot a bit to get the AU (astronomical unit) distance,
convert to km.

### Curious? - #osint
```
100 - Easy

I've been thinking about going on vacation recently and need to know where off
Earth I can find these dunes. What sol was this image taken on?
```
with a Mars photo.

Search for `Curiousity` it's the robot running on Mars, and `sol`, which is
time unit on Mars. Then found this page
https://earthsky.org/space/where-the-curiosity-rover-is-now-on-mars/
and it says days 533.


### Launched - #osint - 100 - Easy

```
What is the name of the launch and the payload in this picture. (flag format is
shctf{rocket_payload}, spaces are underscores)
```

Download the image, there is additional information of the image, include
when it was taken and location. Search for that location show where it was launched,
the date was more important, search `11 April 2019 launch` would found Falcon 11
immediately, open wikipage https://en.wikipedia.org/wiki/Falcon_Heavy, it lists
the payload `Arabsat-6A`

### R2D2 - #web - 100

```
We wouldn't miss the opportunity to make this dad joke.

http://173.230.138.139/

Author: v10l3nt
https://spaceheroes-web-r2d2.chals.io
```
The website shows only an image of two robots in Starwar movie.
It's a hint for `robots.txt`, access the path `/robots.txt` on URL then got the flag.

### Mysterious Broadcast - #web - 100 - Hard

```
There used to be 8 Models of humanoid cylon but now there are only 7. We've located one of their broadcast nodes but we can't decode it. Are you able to decipher their technologies?

http://173.230.134.127
```

Access the page first time shows `~`, then each time return a char 0 or 1,
Looks like a binary, write a script to keep access the same page until got
"something", after a while, it shows `~` and repeat all over again.

```py
import requests
S = requests.session()

out = []
url = 'http://173.230.134.127'
for i in range(1000):

    r = S.get(url)
    print(r.text, r.url)
    out.append(r.text)
    time.sleep(1)
    url = r.url
```

Copy the binary 10..., try convert to integer then byte to get the flag but got
nothing. Paste it to dcode.fr to detect cipher https://www.dcode.fr/cipher-identifier
it returns ASCII, click decrypt and it showed a base64 string, b64decode it to get the flag.

### Space Buds - #web - 100 - Medium

```
One of the puppies got into the web server. Can you help find out who it was?

45.79.204.27
```
with an image of Space Buddies movie https://en.wikipedia.org/wiki/Space_Buddies

Get the name of each dogs, try set it as cookie then login, the correct name would
success and got the flag.

### Flag in Space - 100 - Easy

```
“The exploration of space will go ahead, whether we join in it or not.” - John F. Kennedy

http://172.105.154.14/?flag=
```
with a grid of 5x5. Try add `shctf{` to the `flag=`, shows it on the web, so
we need to bruteforce to find the flag.

```py
import string

letters = string.ascii_letters + string.digits + string.punctuation

flag = 'http://172.105.154.14/?flag=shctf{'

r = requests.get(flag)
old = r.text

while True:
    for c in letters:
        print(c, end=' ')
        url = flag + c
        #print(url)
        r = requests.get(url)
        if r.text != old:
            flag = flag + c
            old = r.text
            print(flag)
            break
```
After a short while, we got the flag.


### Space Traveler - #web - 100 - Easy

```
Explore space with us.

https://spaceheroes-web-explore.chals.io
```

The site show a button click to guess the flag, check the source code found
JS code. Paste the code to https://unminify.com/ to make code more readable.

```js
var _0xb645 = [
    "\x47\x75\x65\x73\x73\x20\x54\x68\x65\x20\x46\x6C\x61\x67",
    "\x73\x68\x63\x74\x66\x7B\x66\x6C\x61\x67\x7D",
    "\x59\x6F\x75\x20\x67\x75\x65\x73\x73\x65\x64\x20\x72\x69\x67\x68\x74\x2E",
    "\x73\x68\x63\x74\x66\x7B\x65\x69\x67\x68\x74\x79\x5F\x73\x65\x76\x65\x6E\x5F\x74\x68\x6F\x75\x73\x61\x6E\x64\x5F\x6D\x69\x6C\x6C\x69\x6F\x6E\x5F\x73\x75\x6E\x73\x7D",
    "\x59\x6F\x75\x20\x67\x75\x65\x73\x73\x65\x64\x20\x77\x72\x6F\x6E\x67\x2E",
    "\x69\x6E\x6E\x65\x72\x48\x54\x4D\x4C",
    "\x64\x65\x6D\x6F",
    "\x67\x65\x74\x45\x6C\x65\x6D\x65\x6E\x74\x42\x79\x49\x64",
];
function myFunction() {
    let _0xb729x2;
    let _0xb729x3 = prompt(_0xb645[0], _0xb645[1]);
    switch (_0xb729x3) {
        case _0xb645[3]:
            _0xb729x2 = _0xb645[2];
            break;
        default:
            _0xb729x2 = _0xb645[4];
    }
    document[_0xb645[7]](_0xb645[6])[_0xb645[5]] = _0xb729x2;
}
```

access _0xb645[3] got the flag.

### Mobile Infantry - #crypto - 100 - Medium

```
nc 0.cloud.chals.io 27602
```

Access via nc, it wants a "1-time-pads", input some text and it would fail with message
says the Python function used to validate failed. Read the code, it says the
length is 38, first 20 chars uppercase, ascending, the later 18 lowercase, descending.
But if try one solution, it says "try again".
So need to bruteforce all cases to get the flag, see pwntools code in
[mobile_infantry.py](mobile_infantry.py)

### Khaaaaaan! - #crypto - 100 - Medium

```
We have intercepted a messages from different ships, but I can't seem to dcode
what they are saying. Can you? languages.PNG

Flag format: shctf{add_after_each_word}
```
An "encrypted" message with 4 different weird font used to craft the message.
Visit dcode https://www.dcode.fr/symbols-ciphers then hand-translating them,
got the flag.

### Information Paradox - #crypto - 293 - Hard

```
Hey Dr. Cooper!

A black hole just swallowed up 63% of Stephen Hawking's private key. Is the information lost?

Please find a way to get it back and extract the flag from Hawking's machine.

Username: hawking / Server: 0.cloud.chals.io:19149
ssh hawking@0.cloud.chals.io -p 19149
```

with a snipped SSH private key file.

Luckily, we read [the blog post](https://blog.cryptohack.org/twitter-secrets) before when solving other CTF crypto chals,
about a pentester showed on
Twitter a "censored" ssh key file, the cryptohack.org community extracted information
from the remain photo, then solved to get the original private key.
Just follow the blog would get the private key, SSH into the server to get the flag.

### An Unknown Disassembly - #re - 100 - Medium

```
Can you exploit this password? We have the disassembly, but we don't recognize the language.

nc 0.cloud.chals.io 27178
```

with attached [Dis.txt](Dis.txt) file

```py
  5           0 LOAD_GLOBAL              0 (input)
              2 LOAD_CONST               1 ('Enter the super secret password:')
              4 CALL_FUNCTION            1
              6 STORE_FAST               0 (a)
...
```

it's Python `dis.dis` bytecode output. We tried tool to automate this disassembly
like https://github.com/rocky/python-uncompyle6/ but didn't able to get it work,
so we follow line-by-line and convert it to original Python code.

```py
import dis
dis.dis("""

a = input('Enter the secret')
b = ''
c = 0

for x in a:
    if x == 'a':
        b += '@'
    if x == '@':
        b += 'a'
    elif x == 'o':
        b += '0'
    elif x == '0':
        b += 'o'
    elif x == 'e':
        b += '3'
    elif x == '3':
        b += 'e'
    elif x == 'l':
        pass
    else:
        b += x
    c += 1


d = 'S0th3combination1sonetw0thr3efourf1ve'

if c % 4 == 0 and b == d:
    print("You got the flag")
""")
```

### Cape Kennedy - #re - 100 - Easy

Please find valid input for this program that doesn't include special
characters. Don't forget to submit in flag format. (remember this is a themed
ctf, the answer is NOT random)

with a python code file named moon.py:

```py
builder = 0

for c in password:
  builder += ord(c)

if builder == 713 and len(password) == 8 and (ord(password[2]) == ord(password[5])):
  if (ord(password[3]) == ord(password[4])) and ((ord(password[6])) == ord(password[7])):
      print("correct")
  else:
      print("incorrect")
```

Bruteforce, there are many output, but search for `Cape Kennedy` and `moon`
would result in wiki, looks for many words and see Apollo11, it's the flag.

### Dreadful Battle - #re - 100 - #TODO
```
Raven Beak was able to steal the flag from the Galactic Federation HQ! Help
Samus defeat him and retrieve the flag, but make sure to stay on your toes and
never let your gaurd down...
```
attach a binary file.

### Spaceflight - #re - 174 - Medium - #TODO

https://spaceheroes-re-spaceflight.chals.io

Author: ICR
attach a binary file.

### Space Captain Garfield - #forensics - 100 - Easy
With a Garfield comic image, but the text using "cat font".

Search for captain Garfield, [got the original comic](https://www.mezzacotta.net/garfield/comics/3568.png), map the text to
the cat font then got the flag.

### The Legend of the Chozo - #forensics - 100 - Medium

```
Samus extracted this file from the site on the last expedition, but it appears
to have been corrupted! This may be the lead we've been looking for to bring
peace to the galaxy. Can you Identify what it once was and possibly restore it?
```

run `xxd` on the file, see it ends with `IEND`, the starts part looks a bit "broken"
with PGN not PNG. But a quick search shows this seems a [PNG file](https://en.wikipedia.org/wiki/Portable_Network_Graphics)
with broken header.
Use Python, open other good PNG file, get first 16 bytes (we just try first 8 bytes but did not work, then try 16 bytes with IHDR part)

```hex
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
```

then write it to this broken file to recover the header, open the image and it
shows the flag.

```py
f = open("CorruptedData.chr", 'rb')
d = f.read()
good = open("good.png", 'rb').read()
d2 = bytearray(d)
d2[:16] = good[:16]
f2 =open('result.png', 'wb')
f2.write(d2)
f2.close()
```

###  Star Pcap - #forensics - 100 - Easy
given a [star.pcap](star.pcap) file.
Download the file, open with WireShark, look through ping packets see the data
contains something.

[Use dpkt, the examples already have solutions to this and next problem](https://kbandla.github.io/dpkt/)

```py
import dpkt
import base64
r = dpkt.pcap.Reader(open("star.pcap", 'rb'))

out = []
for _, buf in r:
    eth = dpkt.ethernet.Ethernet(buf)
    out.append(chr(eth.data.data.code))
print(base64.b64decode("".join(out)))
```

### Netflix and CTF - #forensics - 100 - Easy

```
I don't like watching anything other than TV shows about Space Heroes.

with a .pcap file.
```
similar above, and the the URL from HTTP packet,
```py
r = Reader(open("/tmp/netflix-and-ctf.pcap", 'rb'))

uris = []
for _, buf in r:
    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data
    try:
        request = dpkt.http.Request(tcp.data)
    except Exception:
        continue

    uris.append(request.uri)
print("".join([i.split("_")[-1] for i in uris if "keypress" in i]))
```
