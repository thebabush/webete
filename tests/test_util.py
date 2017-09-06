from webete.util import strip_file_ext_from_list


def test_strip_ext():
    assert strip_file_ext_from_list('asd.py', ['py', 'pyc']) == 'asd'
    assert strip_file_ext_from_list('asd.pyc', ['py', 'pyc']) == 'asd'
    assert strip_file_ext_from_list('asd.py', []) == 'asd.py'
