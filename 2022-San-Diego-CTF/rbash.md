# rbash - all three levels

```
score: 150+150+350
solved: xx/
difficulty: easy/medium/hard
tags: jail, bash, rbash
```

## Problem
https://github.com/acmucsd/sdctf-2022/tree/main/jail/easy%20-%20rbash%20%E2%80%94%20warmup

### Rbash Warmup
Welcome to the restricted shell! Demonstrate RCE on this rbash setup by running the  /flag binary executable, and you will be awarded with the flag!
Connect via
socat FILE:`tty`,raw,echo=0 TCP:rbash-warmup.sdc.tf:1337

### Rbash Yet Another Calculator
Rbash, in its most restricted form, is nothing but a calculator. To get started, try this command: echo $(( 1337 + 1337 ))
Disclaimer
The flag does not have an easy guessable filename, but it is located in the initial working directory of the rbash instance.
Connect via
socat FILE:`tty`,raw,echo=0 TCP:yac.sdc.tf:1337

### Rbash Negotiation with the warden
You now have the right to negotiate your PATH with your prison warden. Same deal as the warmup: Get the flag by executing the /flag binary. Good luck!
Connect via
socat FILE:`tty`,raw,echo=0 TCP:warden.sdc.tf:1337
Jail environment
jail.zip
Note
Ignore the commented line 149 of jail.py. It does not hint at what files is present on the system or any valid solution to this challenge. It is simply a leftover of old code that I forgot to delete.

## Got the flag
### Warmup - easy
These problems all give user access to `rbash`, a restricted-bash environment,
read `man rbash` to see what is restricted, but basically:

- cannot change PATH, envs
- cannot cd
- no ls

The warmup problem, suppose to be the "easiest" but number of solves even < the 2nd medium one.
1st goal is to run /flag binary.

While cannot use `ls`, one can use `echo *` to list files. Type `env`, `export` to
show envs, PATH set, double hit TAB to see what commands available. We see `nc`.

Quick google returns https://fireshellsecurity.team/restricted-linux-shell-escaping-techniques/

Use nc to create reverse shell show there, just: `nc -lvp 5555 -e /flag`, easy?

Open another terminal and `nc address 5555` but it says connection failed, that
is where we stucked for awhile.

After time passed, we noticed `echo /proc/*` show this has only PID 1 running,
this means this run inside a docker container, thus, listen on port 5555 of this
container does not give access to other container.

We run the command again in background, i.e: `nc -lvp 5555 -e /flag &`,
then type `nc address 5555`, got the flag.

### Rbash Yet Another Calculator - medium
Rbash, in its most restricted form, is nothing but a calculator. To get started, try this command: echo $(( 1337 + 1337 ))
Disclaimer
The flag does not have an easy guessable filename, but it is located in the initial working directory of the rbash instance.
Connect via
socat FILE:`tty`,raw,echo=0 TCP:yac.sdc.tf:1337

`echo *` shows the flag filename.
`rbash` restricts only "redirecting output", not input, thus

`while read line; do echo $line; done < flagfilename` shows the flag.

### Rbash Negotiation with the warden
We was given a program to set our PATH env, but limit to max 3 (useless) options,
the program can write, chmod file in current directory (but not in PATH).

The "message" seems weird when we try to remove a PATH, like "we never seen any
prisoner want that but if you want, okay..." makes we wonder what happens if
PATH is empty? tried that in local and it shows that empty PATH would allow to call
files in current directory, or, the PATH set to current working directory.

Remove everything in PATH, write a script as "note" to run the /flag file,
chmod 777, then run it, got the flag.

After got the flag, we check the doc for learning purpose: `man bash`

```
       PATH   The  search  path  for commands.  It is a colon-separated
              list of directories in which the shell looks for commands
              (see  COMMAND EXECUTION below).  A zero-length (null) di‐
              rectory name in the value of PATH indicates  the  current
              directory.  A null directory name may appear as two adja‐
              cent colons, or as an initial or trailing colon.  The de‐
              fault  path is system-dependent, and is set by the admin‐
              istrator who installs bash.  A common value is ``/usr/lo‐
              cal/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin''.
```
