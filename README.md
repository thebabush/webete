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

## Pull requests

Pull requests are welcome. A few rules:

- Respect the coding style and formatting of the existing code.
- Do not change the formatting of existing code.
- Design changes should be discussed beforehand in order to not waste anyone's effort.
- PRs must merge cleanly against the branch they target and must build on Travis.
- PRs must be single scoped (no "add this, fix that and implement X" in the same PR) and complete.
- Commit messages should be informative.
- If you are working on an open issue, [reference it in the title](https://help.github.com/articles/closing-issues-using-keywords/). If you are fixing a bug that hasn't been reported yet, open an issue and reference it in the commit message.
- Generally speaking, the codebase follows PEP8 with an exception: lines longer than 80 chars are OK-ish. Shorter is better than longer. You should definitely stay below 120. Longer lines should be the exception and should be used only for long string constants or when there's no sane way to avoid a `\`.
- TODOs belong to GH issues most of the times, so that they can be discussed.

Most of these are somewhat flexible. Use common sense. 
