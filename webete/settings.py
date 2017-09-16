
# HTTP options
HTTP_USER_AGENTS = [
    # Chrome
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19',
    # Firefox
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12',
    # iPhone
    'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
]
HTTP_DEFAULT_USER_AGENT = HTTP_USER_AGENTS[0]

# Python options
PYTHON_EXTS = ['pyc', 'pyd', 'pyo']
# As of python 3.3, `sys.implementation.cache_tag` or `imp.get_tag()`.
# It used to be hard-coded as "cpython-{MAJOR}{MINOR}"
# See https://www.python.org/dev/peps/pep-0488/
#     https://www.python.org/dev/peps/pep-3147/
PYTHON_CACHE_TAGS = [
    'cpython-26',
    'cpython-27',
    'cpython-35',
    'cpython-36',
    'cpython-37',
]


# Cosmetics
LIST_INDENT = 3
SECTION_WIDTH = 30
