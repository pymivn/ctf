# CAFE

```
score: 100
solved: xx/xx
difficulty: NA
tags: web
```

## Problem

http://3.39.55.38:1929

You can enjoy this cafe :)

upload text, youtube, ...

and file CAFE.zip

## Got the flag
Download & unzip the file

```sh
bot.py  db.sql              Dockerfile  mysql.cnf
bot.sh  docker-compose.yml  html/       run.sh
```

under `html/` there are many PHP, CSS, JS files. `docker-compose.yml` defines
a standard PHP-MySQL web app, which makes this looks like a not-too-simple challenge.
But, but, but there is a Python file named `bot.py`

```py
#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--disable-logging')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
#options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")

driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
driver.implicitly_wait(3)

driver.get('http://3.39.55.38:1929/login')
driver.find_element_by_id('id').send_keys('admin')
driver.find_element_by_id('pw').send_keys('$MiLEYEN4')
driver.find_element_by_id('submit').click()
time.sleep(2)

driver.get('http://3.39.55.38:1929/read?no=' + str(sys.argv[1]))
time.sleep(2)

driver.quit()
```

it is a code to open a web browser, visit a site then login with user & password.

```py
driver.get('http://3.39.55.38:1929/login')
driver.find_element_by_id('id').send_keys('admin')
driver.find_element_by_id('pw').send_keys('$MiLEYEN4')
driver.find_element_by_id('submit').click()
```

Open that site, then enter user & password, the flag is on the page.

## Conclusion
We solved this 13th, after 8 minutes, the first impression was it not that
easy, but look at the Scoreboard many teams got it, we looks at Python file
then solved.
