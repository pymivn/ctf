# OK!

```
author: Volf
score: 400
solved: 33/94
difficulty: medium
tags: forensics
```

## Description

Our computer performance was altered by a malicious individual. We have managed to make a copy of the altered computer and we need immediately to obtain some answers regarding this file. Due to the stressful situation, one of our colleagues managed to write just a single word in his notebook:

Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook. Ook? Ook. Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook! Ook! Ook? Ook! Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook? Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook! Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook.

Your input is needed on the following aspects and you should remember that wecracktheworlds is an important key in this process.

Files are available at the following links:

https://storage.googleapis.com/cyberedu-production/dctf22-ok-chall/unintended.zip.000

https://storage.googleapis.com/cyberedu-production/dctf22-ok-chall/unintended.zip.001

https://storage.googleapis.com/cyberedu-production/dctf22-ok-chall/unintended.zip.002

## Got the flag

Description provide us Ook Programming Language and hint to get the flag "you should remember that <strong>wecracktheworlds</strong> is an important key in this process".

Using https://www.dcode.fr/ook-language to execute code, we get "autopsy" string.

Autopsy is a forensic program, we can use it to open an image file which is snapshot of OS.

The downloaded image file can't be opened directly by Autopsy. We use <strong>FTK Image</strong> to export image to raw (.dd)

In data artifacts, dive deep into Recent Document, we found Malicious Powershell in Downloads folder of sunflower user.

![Recent Document](https://live.staticflickr.com/65535/51938454387_8d40d58051_b.jpg)

*<em>We know that the attacker used a password to unrar the malicious scripts downloaded from his server. Can you provide its value? (Points: 50)</em>

Found flag in README file. Password unrar = infect

*<em> We know that the attacker attempted to download an infected image from one of his servers before launching the attack. Can you provide the file name? (Points: 50) </em>

Found flag in Sample 1 Folder. Image filename is "p_1372hc5jv1.jpg"

![Malicious Image](https://live.staticflickr.com/65535/51938454387_8d40d58051_b.jpg)

*<em>A message is received when the first task is completed. Please share it with us: (Points: 229)</em>

We found C:\Users\sunflower\Documents\secret1.txt file. It contains "E5EB9479E816D06CD53062B1EF017B185D9E47B087059484EEF344810E4B06A7" string. Remember "wecracktheworlds" is an important key. Because string's length is 256 bit and key's length is 16 bit. We try decrypting message using [AES256.](https://www.devglan.com/online-tools/aes-encryption-decryption). Flag is "yourfirstmissioniscompleted"

*<em>We suspect that the Sample 5 script contains another malicious download link. Can you determine the address? (Points: 79)</em>

Extract Sample 5 we get powershell code. Payload was decrypted by XOR algorithm with "b5ce91" key. Decrypt payload we have URL "http://fbigov.website/oru/Noni.exe"

## Conclusion

This challenge introduces forensics techniques that are usually used for Incident Response.
