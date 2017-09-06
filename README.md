# WEBETE

[![Build Status](https://travis-ci.org/kenoph/webete.svg?branch=master)](https://travis-ci.org/kenoph/webete)

WEB Extensive Testing Environment.

![mentana](https://user-images.githubusercontent.com/1985669/30066524-73e87bd6-9258-11e7-9a83-62963edac0c3.jpg)

## Install

```bash
git clone git@github.com:kenoph/webete.git
cd webete
pip install .
pip install -U --no-deps -r requirements.txt
```

## Examples

### Python `.pyc` download and decompilation

Say you want to get a compiled python file from a webserver but you don't
want to try all the different paths manually (different interpreter versions, `__pycache__/`, ecc...).
Say, then, that you would also like to decompile such file once you find its url.
`webete` has got you covered:

Download and decompile a `secret.pyc` file straight from a webserver:

```bash
webete http://target/ --python secret # output ./secret.py
```

Download and decompile `secret.pyc` from library `hidden`:

```bash
webete http://target/ -p hidden/secret # output ./hidden/secret.py
```
