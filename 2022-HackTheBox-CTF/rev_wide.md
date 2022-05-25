# WIDE

```
score: 300
solved: xx/xx
difficulty: easy
tags: re, radare2
```

## Problem

[binary](./wide)
[db.ex](./db.ex)

## Get the flag
Open the binary with radare2: `r2 -A wide`.
Type `iz` to see strings in binary, see

```
[0x000008e0]> iz
[Strings]
nth paddr      vaddr      len size section type    string
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――
0   0x00001088 0x00001088 43  44   .rodata ascii   Which dimension would you like to examine?
1   0x000010b4 0x000010b4 24  25   .rodata ascii   That option was invalid.
2   0x000010d0 0x000010d0 69  70   .rodata ascii   [X] That entry is encrypted - please enter your WIDE decryption key:
3   0x00001118 0x00001118 15  64   .rodata utf32le sup3rs3cr3tw1d3
```

Run the binary

```
$ ./wide db.ex
[*] Welcome user: kr4eq4L2$12xb, to the Widely Inflated Dimension Editor [*]
[*]    Serving your pocket dimension storage needs since 14,012.5 B      [*]
[*]                       Displaying Dimensions....                      [*]
[*]       Name       |              Code                |   Encrypted    [*]
[X] Primus           | people breathe variety practice  |                [*]
[X] Cheagaz          | scene control river importance   |                [*]
[X] Byenoovia        | fighting cast it parallel        |                [*]
[X] Cloteprea        | facing motor unusual heavy       |                [*]
[X] Maraqa           | stomach motion sale valuable     |                [*]
[X] Aidor            | feathers stream sides gate       |                [*]
[X] Flaggle Alpha    | admin secret power hidden        |       *        [*]
Which dimension would you like to examine? 1
The Ice Dimension
Which dimension would you like to examine? 2
The Berserk Dimension
Which dimension would you like to examine? 3
The Hungry Dimension
Which dimension would you like to examine? 4
The Water Dimension
Which dimension would you like to examine? 5
The Bone Dimension
Which dimension would you like to examine? 6
[X] That entry is encrypted - please enter your WIDE decryption key: sup3rs3cr3tw1d3
HTB{str1ngs_4r3nt_4lw4ys_4sc11}
```
we got the flag.
