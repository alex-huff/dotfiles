#!/bin/python3

import os
import sys
from subprocess import Popen, DEVNULL, PIPE
import base64
import json

# match item input format
# match
# ":"<base32 encoded absolute path>
# ":"<byte offset of first match>
# ":"<line number of start of region>
# ":"<line number of end of region>
# ":"<unicode string basename> | non-<encoding> filename
# ":"<unicode string match without null bytes> | non-<encoding> data
# "\0"

# query-error/rg-error item input format
# error
# ":"<base32 encoded error message>
# ":"b""
# ":"1
# ":"b""
# ":"Query error | rg error
# "\0"

class RGOptions:
    def __init__(self):
        self.paths = []
        self.arguments = []

    def __getattribute__(self, attribute):
        try:
            return super().__getattribute__(attribute)
        except:
            processed_name = attribute.replace('_', '-')
            return lambda *values: self.push_long_arg(processed_name, *values)

    def push_args(self, *args):
        self.arguments.extend(str(arg) for arg in args)
        return self

    def push_arg(self, arg):
        return self.push_args(arg)

    def push_long_arg(self, arg, *values):
        return self.push_args(*(f"--{arg}={value}" for value in values)) if values else self.push_arg(f"--{arg}")

    def pop_arg(self, num=1):
        del self.arguments[-num:]
        return self

    def push_paths(self, *paths):
        self.paths.extend(os.path.expanduser(path) for path in paths)
        return self

    def push_path(self, path):
        return self.push_paths(path)

    def pop_path(self, num=1):
        del self.paths[-num:]
        return self

    def help(self):
        raise Exception(help_message)

def is_data_utf8(data_object):
    return "text" in data_object

def get_non_utf8_data_bytes(data_object):
    return base64.b64decode(data_object["bytes"])

def get_utf8_data_bytes(data_object):
    return data_object["text"].encode(ENCODING)

def get_data_bytes(data_object):
    if is_data_utf8(data_object):
        return get_utf8_data_bytes(data_object)
    else:
        return get_non_utf8_data_bytes(data_object)

def get_formatted_region(region_bytes, submatches):
    region_bytes_view = memoryview(region_bytes)
    processed_region_bytes = bytearray()
    current_position = 0
    for match in submatches:
        start = match["start"]
        end = match["end"]
        if start == end:
            continue
        if start > current_position:
            processed_region_bytes.extend(RESET_BYTES)
            processed_region_bytes.extend(region_bytes_view[current_position:start])
            processed_region_bytes.extend(RESET_BYTES)
            processed_region_bytes.extend(GREEN_BYTES)
        elif current_position == 0:
            processed_region_bytes.extend(GREEN_BYTES)
        processed_region_bytes.extend(region_bytes_view[start:end])
        current_position = end
    processed_region_bytes.extend(RESET_BYTES)
    if current_position < len(region_bytes):
        processed_region_bytes.extend(region_bytes_view[current_position:])
    return processed_region_bytes.replace(NULL_BYTE, EMPTY_BYTE)

def write_match_item(rg_message):
    rg_data = rg_message["data"]
    absolute_offset = rg_data["absolute_offset"]
    file_path = rg_data["path"]
    submatches = rg_data["submatches"]
    region = rg_data["lines"]
    region_bytes = get_data_bytes(region)
    formatted_region_bytes = get_formatted_region(region_bytes, submatches) if is_data_utf8(region) else PLACEHOLDER_DATA_BYTES
    num_lines = region_bytes.count(NEWLINE_BYTE)
    if not region_bytes.endswith(NEWLINE_BYTE):
        num_lines += 1
    line_number_start = rg_data["line_number"]
    line_number_start_string_encoded = str(line_number_start).encode(ENCODING)
    line_number_end = line_number_start + (num_lines - 1)
    line_number_end_string_encoded = str(line_number_end).encode(ENCODING)
    first_match_offset = absolute_offset + submatches[0]["start"] if submatches else 0
    first_match_offset += 1
    first_match_offset_string_encoded = str(first_match_offset).encode(ENCODING)
    file_path_bytes = get_data_bytes(file_path)
    file_path_bytes = os.path.abspath(file_path_bytes)
    file_path_bytes = os.path.normpath(file_path_bytes)
    file_path_base32_bytes = base64.b32encode(file_path_bytes)
    file_basename_bytes = os.path.basename(file_path_bytes)
    try:
        _ = file_basename_bytes.decode(ENCODING)
        file_basename_bytes = b"%b%b" % (BLUE_BYTES, file_basename_bytes)
    except UnicodeError:
        file_basename_bytes = PLACEHOLDER_FILENAME_BYTES
    out.write(RESET_BYTES)
    out.write(MATCH_TYPE_BYTES)
    out.write(DELIMITER_BYTE)
    out.write(file_path_base32_bytes)
    out.write(DELIMITER_BYTE)
    out.write(first_match_offset_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(line_number_start_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(line_number_end_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(file_basename_bytes)
    out.write(RESET_BYTES)
    out.write(DELIMITER_BYTE)
    out.write(formatted_region_bytes)
    out.write(RESET_BYTES)
    out.write(NULL_BYTE)
    out.flush()

def write_error_item(error_specifier_bytes, error_message):
    error_message_bytes = error_message.encode(ENCODING)
    error_message_base32_bytes = base64.b32encode(error_message_bytes)
    out.write(RESET_BYTES)
    out.write(ERROR_TYPE_BYTES)
    out.write(DELIMITER_BYTE)
    out.write(error_message_base32_bytes)
    for _ in range(2):
        out.write(DELIMITER_BYTE)
    out.write(ONE_BYTE)
    for _ in range(2):
        out.write(DELIMITER_BYTE)
    out.write(error_specifier_bytes)
    out.write(RESET_BYTES)
    out.write(NULL_BYTE)
    out.flush()

script_basename = os.path.basename(sys.argv[0])
if len(sys.argv) != 2:
    print(f"Usage: {script_basename} <query>", file=sys.stderr)
    sys.exit(1)
out = sys.stdout.buffer
query = sys.argv[1]
help_message = \
"""\
ripgrep command manipulation:
    rg.push_arg(arg), rg.push_args(*args), rg.push_long_arg(arg, *values)
    rg.push_path(path), rg.push_paths(*paths)
    rg.pop_arg(num=1), rg.pop_path(num=1)

    rg.some_arg()               # same as --some-arg
    rg.some_arg(value1, value2) # same as --some-arg=value1 --some-arg=value2

Some useful ripgrep options:
    --regexp=PATTERN --file=PATTERNFILE
    --invert-match
    --smart-case --ignore-case
    --fixed-strings
    --word-regexp --line-regexp
    --multiline --multiline-dotall
    --no-unicode
    --null-data --crlf
    --text
    --unrestricted
    --ignore-file=PATH --ignore-file-case-insensitive
    --no-ignore --no-ignore-dot --no-ignore-exclude --no-ignore-global
        --no-ignore-parent --no-ignore-vcs
    --hidden
    --follow
    --one-file-system
    --glob=GLOB --iglob=GLOB
    --type=TYPE --type-not=TYPE --type-add=TYPESPEC --type-clear=TYPE
    --search-zip
    --pre=COMMAND --pre-glob
    --stop-on-nonmatch
    --max-count=NUM
    --max-depth=NUM
    --max-filesize=NUM+SUFFIX?
    --threads=NUM
    --encoding=ENCODING
    --engine=ENGINE
    --no-config\
"""
ENCODING = "utf-8"
ENCODING_BYTES = ENCODING.encode(ENCODING)
CSI_CHARACTER_ATTRIBUTES_TEMPLATE = b"\033[%bm"
GREEN_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"32")
BLUE_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"34")
RED_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"31")
RESET_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"0")
DELIMITER_BYTE = b":"
QUERY_DELIMITER = ";;"
NULL_BYTE = b"\0"
EMPTY_BYTE = b""
ONE_BYTE = b"1"
NEWLINE_BYTE = b"\n"
MATCH_TYPE = "match"
ERROR_TYPE = "error"
MATCH_TYPE_BYTES = MATCH_TYPE.encode(ENCODING)
ERROR_TYPE_BYTES = ERROR_TYPE.encode(ENCODING)
PLACEHOLDER_FILENAME_BYTES = b"%bnon-%b filename" % (RED_BYTES, ENCODING_BYTES)
PLACEHOLDER_DATA_BYTES = b"%bnon-%b data" % (RED_BYTES, ENCODING_BYTES)
QUERY_ERROR_SPECIFIER_BYTES = b"%bQuery error" % RED_BYTES
RG_ERROR_SPECIFIER_BYTES = b"%brg error" % RED_BYTES
rg_command = [
    "rg",
    "--line-number",
    "--json",
]
rg_options = RGOptions()
setup_expression_end = query.rfind(QUERY_DELIMITER)
if setup_expression_end != -1:
    regex_start = setup_expression_end + 2
    setup_expression = query[0:setup_expression_end]
    try:
        # a carefully crafted setup_expression can still destroy the system but
        # removing all unnecessary globals and some dangerous builtins makes
        # accidently modifying the system very unlikely
        eval(
            setup_expression,
            {
                "rg": rg_options,
                "env": os.environ,
                "__import__": None,
                "open": None,
                "print": None,
                "compile": None,
                "exec": None,
                "eval": None,
            }
        )
    except Exception as exception:
        write_error_item(QUERY_ERROR_SPECIFIER_BYTES, str(exception))
        sys.exit(0)
else:
    regex_start = 0
regex = query[regex_start:]
rg_options.regexp(regex)
rg_command.extend(rg_options.arguments)
rg_command.append("--")
rg_command.extend(rg_options.paths)
rg_process = Popen(rg_command, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, encoding=ENCODING)
for rg_json in rg_process.stdout:
    rg_message = json.loads(rg_json)
    if rg_message["type"] != "match":
        continue
    write_match_item(rg_message)
error_message = rg_process.stderr.read()
if error_message:
    write_error_item(RG_ERROR_SPECIFIER_BYTES, error_message)
rg_process.wait()
