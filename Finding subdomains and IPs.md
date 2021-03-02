Academic task: find all subdomains on `juniper.net` and IP addresses for them.

Downloading `index.html` with `wget juniper.net`.
Searching for subdomains:
```
cat index.html | grep -E "http|https" | cut -d "/" -f 3 | tr -d "'," | cut -d '"' -f 1 | grep -v '+' | uniq -u >> list.txt
```
1. Collecting lines containing `http` or `https`
2. Cutting lines in 3 segments with respect to "/"
3. Removing "',"
4. Removing '"' with cut operation
5. Excluding lines with '+'
6. Excluding redundant lines
7. Save to file
Next, I look for IP addresses:
```
for url in $(cat list.txt); do host $url; done | grep "has address" | cut -d " " -f 4 | sort -u >> addresses.txt
```
1. Resolving address for domains
2. Excluding strings representing aliases
3. Cutting only end of line, after 4 " " characters
4. Excluding redundant lines
5. Save to file

Result:
```
head addresses.txt                                                                                                          104.244.42.1
104.244.42.129
104.244.42.193
104.244.42.65
104.81.212.82
13.107.43.14
136.147.56.133
136.147.56.5
136.147.58.133
142.0.173.134
...
```
