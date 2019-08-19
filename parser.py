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

    while line[index] == ' ' or line[index] == '\t':
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

    match = re.match('^"(.*)"', line[pos:])
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

    (parsed, pos, _) = parse_alpha(line, pos+1)
    pos = strip_empty(line, pos)

    if pos >= length or not parsed:
        return (None, pos, 'Invalid variable declaration')

    variable_name = parsed

    if line[pos] != BRACES_ENDS[start_char]:
        return (None, pos, 'Invalid/Missing closure for variable declaration')

    pos = strip_empty(line, pos+1)
    if not line or line[pos:pos+2] != ':=':
        return (None, pos, 'Variable declaration missing `:=`')

    pos += 2
    string_value, pos, _ = parse_string_val(line, pos)

    if not string_value:
        return None, pos, "Invalid right hand side for declaration"

    pos = strip_empty(line, pos)
    if line[pos:] != '':
        return None, pos, "Trailing characters after declaration"

    return (variable_name, string_value, start_char), pos, ''


LINKS_LIST = ['->', '<-', '|>', '<|']


def parse_chain(line, index=0):
    vars = []
    links = []

    parse_var = True
    pos = index
    curr_val = {}

    line = strip_comment(line)
    length = len(line)
    while index < length:
        if parse_var:
            str_val, pos, er = parse_string_val(line, index)
            if str_val is not None:
                curr_val['value'] = str_val
                curr_val['type'] = 'string'
                index = pos
                parse_var = False
            if parse_var:
                var_val, pos, _ = parse_alpha(line, index)
                if var_val is not None:
                    curr_val['value'] = var_val
                    curr_val['type'] = 'variable'
                    index = pos
                    parse_var = False
            if parse_var:
                return None, index, "Expected a string or variable"
            vars.append({**curr_val})
        else:
            pos = strip_empty(line, index)
            if pos >= len(line):
                break
            if line[pos:pos+2] not in LINKS_LIST:
                return None, pos, "Expected one of " + ', '.join(LINKS_LIST)

            links.append(line[pos:pos+2])
            index = pos + 2
            parse_var = True
    # It should not be expecting to parse a variable as chain ends on variable, not link
    if parse_var:
        return None, index, "Dangling link."
    return (vars, links), index, ''


def parse(input):
    """Takes in a string input and returns a graph like result"""
    var_definitions_map = {}

    lines = input.split('\n')
    for line_num, line in enumerate(lines):
        line = line.strip()
        if not line or line[0] == '#':
            continue
        declaration, dec_position, dec_err = parse_declaration(line, 0)
        if declaration is None:
            chain, chain_position, chain_err = parse_chain(line, 0)
            if chain is None:
                err = dec_err if dec_position > chain_position else chain_err
                err_col = max(dec_position, chain_position)
                print(f'SYNTAX_ERROR<Line {line_num+1}, Col {err_col+1}>: {err}')
            else:
                print('CHAIN', chain)
        else:
            print('DECLARATION', declaration)


if __name__ == '__main__':
    with open('diagram.dsl') as f:
        parse(f.read())
