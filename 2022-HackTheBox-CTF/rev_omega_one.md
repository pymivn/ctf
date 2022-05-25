# Omega One

```
score: 300
solved: xx/xx
difficulty: easy
tags: re, radare2
```

## Problem

[code](./omega-one)
[output.txt](./output.txt)

## Get the flag
Open the binary with radare2: `r2 -A omega-one`; type `afl` to list functions,
see main. Type `pdf @main` to decompile the main function, see output like
following

```
┌ 2766: int main (int argc, char **argv, char **envp);
│           0x00000b4c      55             push rbp
│           0x00000b4d      4889e5         mov rbp, rsp
│           0x00000b50      bf04000000     mov edi, 4                  ; size_t arg1
│           0x00000b55      e8190b0000     call fcn.00001673
│           0x00000b5a      488905b72420.  mov qword [0x00203018], rax ; [0x203018:8]=0
│           0x00000b61      488d3d82ffff.  lea rdi, qword [0x00000aea]
│           0x00000b68      e8b3150000     call fcn.00002120
│           0x00000b6d      488b05a42420.  mov rax, qword [0x00203018] ; [0x203018:8]=0
│           0x00000b74      488d15c51500.  lea rdx, qword str.Lendrens ; 0x2140 ; "Lendrens" ; char *arg3
│           0x00000b7b      488d35c71500.  lea rsi, qword [0x00002149] ; "k" ; char *arg2
│           0x00000b82      4889c7         mov rdi, rax                ; int64_t arg1
│           0x00000b85      e8e60c0000     call fcn.00001870
│           0x00000b8a      488b05872420.  mov rax, qword [0x00203018] ; [0x203018:8]=0
│           0x00000b91      488d15b31500.  lea rdx, qword str.Thauv_i  ; 0x214b ; "Thauv'i" ; char *arg3
│           0x00000b98      488d35b41500.  lea rsi, qword [0x00002153] ; "d" ; char *arg2
│           0x00000b9f      4889c7         mov rdi, rax                ; int64_t arg1
│           0x00000ba2      e8c90c0000     call fcn.00001870
...
```

we can notice the keyword "Lendrens" follows by char "k", so just guessing that
map word to char. To test this hypothesis, we check first 3 words from output.txt
and got HTB, so this is correct guess. Convert all words in output.txt to the char,
after 33 chars, we got the flag... hahaha just kidding. That is too much to
do manually, so we use a command line to help solve it.

Firstly, write this decompiled code to a file using r2 command:  `pdf @main > omega.asm`
Then run a shell script to automate the mapping

```sh
while read line
    do grep -A2 \"$line omega.asm
done < output.txt  | grep -F 'char *arg2' | awk '{print $9}' | xargs | tr -d ' '
```

we got the flag: `HTB{l1n34r_t1m3_but_pr3tty_sl0w!`
