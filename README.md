# Git_Leak_Checker

## Description
`.git` directory can leak complete source code of a website, I wrote this script to find vulnerable domains, Supply it a list of domains and it will write vulnerable domains in another file,

## Journey
- I wrote it in python and it didn't work the way it should
- I wrote it in bash and worked but was very slow
- I wrote it agian in Python and it seem stable for now with really good speed.


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

## Author
- Ravindra Sisodia
