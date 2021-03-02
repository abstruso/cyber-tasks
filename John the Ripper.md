# John the Ripper
Academic task: crack hashes in `hasla_do_zlamania.txt`.

My first step is to identify what kind of hash I have deal with. According to `hash-identifier < hasla_do_zlamania.txt` propably all of them are MD5.
I begin attack with list of common passwords from `dirb` tool build into Kali Linux.
```
$ john --format=raw-md5 --wordlist=/usr/share/wordlists/dirb/common.txt hasla_do_zlamania.txt
Using default input encoding: UTF-8
Loaded 5 password hashes with no different salts (Raw-MD5 [MD5 256/256 AVX2 8x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
~apache         (?)
forgot-password (?)
Warning: Only 6 candidates left, minimum 24 needed for performance.
2g 0:00:00:00 DONE (2020-12-04 12:53) 200.0g/s 461400p/s 461400c/s 1614KC/s zone..zt
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed
```
Next I tried with `big.txt` from the same directory.
```
$ john --format=raw-md5 --wordlist=/usr/share/wordlists/dirb/big.txt hasla_do_zlamania.txt
Using default input encoding: UTF-8
Loaded 5 password hashes with no different salts (Raw-MD5 [MD5 256/256 AVX2 8x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
dev-bin         (?)
java_classes    (?)
other-resources (?)
```
Results:
```
─$ cat john.pot
$dynamic_0$4be61e7cfacf802887cbb91bccc9382e:~apache
$dynamic_0$00e2a8f568ff592a6f19d15f6fece067:forgot-password
$dynamic_0$081403781c01b64d74a32f468720c948:dev-bin
$dynamic_0$35e4010ee47fe425abf0e7e9608e10a6:java_classes
$dynamic_0$0ae1921df32b3f541150ee0e79c49a32:other-resources
```
