# Hexahue Hate!

```
score: 445
solved: xx/76
difficulty: medium
tags: misc, hexahue, crypto, image processing, python, opencv
```

## Problem
I hate hexahue so much!

Note: Please wrap your answer in vsctf{}. Flag format (RegEx): `vsctf\{[A-Z_]+\}`

[hexhuebad.png](./hexhuebad.png)

## Got the flag
For unknown reason, the default image viewer on Ubuntu 20.04 does not display
the image properly, it shows only noise.

Read the file into Python with opencv2:

```py
import cv2
im = cv2.imread("hexhuebad.png")
print(im.shape)
# (50, 111340, 3)
print(im[:, :200, :])
# array([[[255, 255, 255],
#         [255, 255, 255],
#         [255, 255, 255],
#         ...
```

Seeing many value are 255 == white color, this does not match to what we see.
So we wrote this to file and view it:

```py
cv2.imwrite("out.png", im[:, :1024, :])
```

Open the `out.png` file shows image with rectangle color blocks.
Try open the hexhuebad.png with GIMP, zoom in we can view the image.
A quick search returns that hexahue is a cipher that can encode/decode online
on https://www.dcode.fr/hexahue-cipher

Manually decode some first characters, it says "LOREM IPSUM...",
and the image is very wide (111340 pixel width), the message is long and
need to decode programatically.

Another quick search for "hexahue python" returns a snippet which already
mapping all block to alphabet, thanks [charles-l](https://gist.github.com/charles-l/648446476df66db88f6f864e47793666)

Looks closer to the image, each block width 20 pixels, 30 pixel heights,
the padding top/bottom/left/right are all 10 pixels, the "space" after each
char is 10 pixel width. So we crop the padding, then reach in each 30 pixels (a char and a space),
map the color from 6 blocks to alphabet characters to building the message:

```py
crop = im[10:-10, 10:-10]
cs = []
for x in range(0, crop.shape[1], 30):
    # get 6 pix and build code word
    window = crop[:, x:x+30,:]
    char = ''.join(colors[tuple(i.tolist())] for i in (
                                      window[0,  0, :], window[0, 10, :],
                                      window[10, 0, :], window[10, 10, :],
                                      window[20, 0, :], window[20, 10, :]))
    cs.append(codewords[char])
print(''.join(cs).upper())
# LOREM IPSUM DOLOR SIT AMET  CONSECTETUR ADIPISCING ELIT  ...
```

The message is long, but looks closer, in the middle of the message, says
`THE MESSAGE YOU SEEK IS IHATEHEXAHUESOMUCHPLEASEHELP`

That, we got the flag: `vsctf{IHATEHEXAHUESOMUCHPLEASEHELP}`
