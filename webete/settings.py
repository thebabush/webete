
# OPTIONS
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
