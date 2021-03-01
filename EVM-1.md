*This tasks was realised in pair, I was responsible for finding vulnerabilities and exploiting them in order to obtain evidence of successful attack.*

# EVM-1

We start from scanning host with `nikto`, this revealed working wordpress serwer.
We have tried many exploits but none of them succeed in creating reverse connection.
Next, we use tool `wpscan` dedicated to WordPress audits.
After dictionary attack we know this:
```
[!] Valid Combinations Found:
 | Username: c0rrupt3d_brain, Password: 24992499
```
Using this credentials, we transfer malicious php file (created with `unix/webapp/wp_admin_shell_upload`), this leads us to gaining access to `www-data` user account.
In home directory of this user we found `.root_password_ssh.txt` containing "willy26".
Finally, as a root, we read `proof.txt` in /root
```
voila you have successfully pwned me :) !!!
:D
```
