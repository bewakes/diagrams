import string
import re
"""
The DSL is parsed line by line. There are no multi line statements. So, the
parsing will be easy
"""

rules = {
    'DEFINITION': [('DECLARATION', ':=', '*')],
    'DECLARATION': [
        ('[', 'ALPHA', ']'),
        ('(', 'ALPHA', ')'),
        ('/', 'ALPHA', '/'),
    ],
    'CHAIN': [
        ('VAR',),
        ('VAR', 'LINK', 'CHAIN'),
    ],
    'LINK': [
        ('-', '>'),
        ('|', '>'),
        ('<', '-'),
        ('<', '|'),
    ],
    'COMMENT': [('#', '*')],
}

BRACES_ENDS = {
    '[': ']',
    '(': ')',
    '/': '/',
}


def parse_char(char, line, index):
    pos = strip_empty(line, index)
    if pos >= len(line) or line[pos] != char:
        return None, pos, ''


def strip_empty(line, index=0):
    length = len(line)

    if index >= length:
        return index

    while line[index] == ' ' or '\t':
        index += 1
        if index >= len(line):
            break
    return index


def strip_comment(line):
    quote_count = 0
    for i, x in enumerate(line[::-1]):
        if x == '"':
            quote_count += 1
        elif x == '#':
            return line[:len(line) - i - 1]
    return line


def parse_alpha(line, index=0):
    index = strip_empty(line, index)
    length = len(line)
    if index >= length:
        return '', index, ''  # parsed, index, msg

    position = index
    while line[position] in string.ascii_letters:
        position += 1
        if position >= length:
            return line[index:], position+1, ''
    return line[index:position], position, ''


def parse_string_val(line, index=0):
    line = strip_comment(line)
    pos = strip_empty(line, index)

    match = re.match(line[pos:], '^"(.*)"')
    if not match:
        return None, pos, "Invalid string"
    val = match.group(1)
    return val, pos + len(val) + 2, ''


def parse_declaration(line, index=0):
    line = strip_comment(line)
    length = len(line)
    pos = strip_empty(line, index)
    if pos >= length:
        return None, pos, 'Empty declaration'

    start_char = line[pos]
    if start_char not in BRACES_ENDS:
        return (None, pos, 'Invalid declaration token')

    (parsed, pos, _) = parse_alpha(line, pos)
    pos = strip_empty(line, pos)

    if pos >= length or not parsed:
        return (None, pos, 'Invalid variable declaration')

    variable_name = parsed

    if line[pos] != BRACES_ENDS[start_char]:
        return (None, pos, 'Invalid/Missing closure for variable declaration')

    pos = strip_empty(line, pos)
    if not line or not line[pos:pos+2] != ':=':
        return (None, pos, 'Variable declaration missing `:=`')

    pos += 2
    string_value, pos, _ = parse_string_val(line, pos)

    if not string_value:
        return None, pos, "Invalid right hand side for declaration"

    pos = strip_empty(line, pos)
    if line[pos:] != '':
        return None, pos, "Trailing characters after declaration"

    return (variable_name, string_value, start_char), pos, ''


def parse_chain(line, index=0):
    vars_links = {}
    values_links = {}

    parse_var = True
    pos = index
    while True:
        if parse_var:
            str_val, pos, _ = parse_string_val(line, index)
            if str_val is not None:
                # TODO: start here
                pass


def parse(input):
    """Takes in a string input and returns a graph like result"""
    var_definitions_map = {}

    lines = input.split('\n')
    for line_num, line in enumerate(lines):
        pass
