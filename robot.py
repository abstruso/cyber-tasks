#!/usr/bin/env python3
# Solution to simple captcha task where,
# captcha picutre name contains acces string.

import requests

url = "http://tasks.ctfd.kncyber.pl:7022/"
r = requests.get(url)
my_cookie = r.cookies
position = str(my_cookie).find("PHPSESSID=")
print("cookie:", str(my_cookie)[position:position+42])


def find_code(r):
    position = str(r.text).find("code=")
    position += 5
    return str(r.text)[position:position + 32]


for i in range(100):
    r = requests.post(url, data={'captcha': find_code(r)}, cookies=my_cookie)
    print(i, "%")
print(r.text)
