# Vulnix
From `nmap` scan we know that host Vulnix work on some Linux 2.6.32 - 3.10.
```
PORT STATE SERVICE
22/tcp open ssh
25/tcp open smtp
79/tcp open finger
110/tcp open pop3
111/tcp open rpcbind
143/tcp open imap
512/tcp open exec
513/tcp open login
514/tcp open shell
993/tcp open imaps
995/tcp open pop3s
2049/tcp open nfs
MAC Address: 00:0C:29:0F:3A:A5 (VMware)
Device type: general purpose
Running: Linux 2.6.X|3.X
OS CPE: cpe:/o:linux:linux_kernel:2.6 cpe:/o:linux:linux_kernel:3
OS details: Linux 2.6.32 - 3.10
```
Next, I would like to discover users of Vulnix. It can be done by telnet, in my case: `telnet 192.168.109.131 25`. From that users are root, user and vulnix.
I write names of this users to users.txt in order to perform dictionary attack on their passwords. I will use rockyou wordlist build in Kali Linux and hydra:
```
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt 192.168.109.131 ssh
```
Success! Credentials `user:letmein` found.
Unfortunately user doesn't belong to sudoers.
New conception is to create vulnix account in my local attacker system, to imitate user in Vulnix machine. Using vulnerabilities in Vulnix configuration I mount vulnix /home partition into attacker machine.
I use it to generate new ssh key: `ssh-keygen -t rsa`. I change name of public key on `authorized_keys` in .ssh catalog. Then there is possible to login with ssh key, without knowing password.
My next step will be change in `/etc/exports` in order to mount `/root`, generate next pair of ssh keys, change name, and login with ssh key, in one word-repeat process for root.
