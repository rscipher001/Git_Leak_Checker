# Git_Leak_Checker

## Description
`.git` directory can leak complete source code of a website, I wrote this script to find vulnerable domains.

## How to use
You need a list of domains you want to test in textfile without protocol name.
Ex:

```
api.google.com
google.com
developer.google.com
...
education.google.com
```

Clone it and run
```bash
./git_leak_checker.py -i file.txt -o out.txt -t 2
```

- `-i`: Input file containing domain list
- `-o`: Output file containing vulnerable domain list
- `-t`: Curl timeout [Keep low]

## Journey
- I wrote it in python and it didn't work the way it should
- I wrote it in bash and worked but was very slow
- I wrote it again in Python and it seem stable for now with really good speed.


## Dependency Installation 

### Ubuntu
- Don't use `pip` to install `pycurl` instead use apt

```bash
sudo apt install python3-pycurl
```


### Termux

```bash
pkg i python python-dev openssl openssl-dev curl clang libcrypt libcrypt-dev libcurl libcurl-dev
export PYCURL_SSL_LIBRARY=openssl
pip install pycurl
```

### Curl TimeOut
On a vulnerable server it will take less than a second to verify vulnerability so it is a good idea to keep it low but you want to be sure then leave default which is 10.

### Changlog
- Merged UA in python file now script is portable
- File that contains `domain` and all `.txt` file are ignored by git

## Author
- Ravindra Sisodia
