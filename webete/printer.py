from . import settings


def print_header(title):
    print('=' * settings.SECTION_WIDTH, str(title), '=' * settings.SECTION_WIDTH)


def print_request(url, method=None, line_end=' '):
    if method:
        method = method.title()
        # Double consonant at the end
        if len(method) > 1 and method[-1] not in {'a', 'e', 'i', 'o', 'u'}:
            method += method[-1]
    else:
        method = 'Try'

    print('*' * settings.LIST_INDENT, '{}ing {}...'.format(method, url), end=line_end)


def print_request_result(status, content=None, max_content_lines=None):
    print(status)
    if content:
        content = content.split('\n')
        if max_content_lines and len(content) > max_content_lines:
            print('\n'.join(content[:max_content_lines]))
            print('... ({} other lines not displayed) ...'.format(len(content) - max_content_lines))
        else:
            print('\n'.join(content))
