#!/bin/python3

import os
import sys
from subprocess import Popen, DEVNULL, PIPE
import base64
import json

# match item input format
# match
# ":"<base32 encoded absolute path>
# ":"<byte offset inclusive beginning of region>
# ":"<byte offset of first match>
# ":"<byte offset exclusive end of region>
# ":"<line number of beginning of region>
# ":"<unicode string basename> | Invalid <encoding> filename
# ":"<unicode string match without null bytes> | Invalid <encoding> data
# "\0"

# query-error/rg-error item input format
# query-error | rg-error
# ":"<base32 encoded error message>
# ":"b""
# ":"b""
# ":"b""
# ":"1
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

    def push_long_arg(self, name, *values):
        return self.push_args(*(f"--{name}={value}" for value in values)) if values else self.push_arg(f"--{name}")

    def pop_arg(self):
        self.arguments.pop()
        return self

    def push_paths(self, *paths):
        self.paths.extend(os.path.expanduser(path) for path in paths)
        return self

    def push_path(self, path):
        return self.push_paths(path)

    def pop_path(self):
        self.paths.pop()
        return self

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
    region = rg_data["lines"]
    line_number = rg_data["line_number"]
    file_path = rg_data["path"]
    submatches = rg_data["submatches"]
    region_start_offset = absolute_offset
    region_start_offset_string_encoded = str(region_start_offset).encode(ENCODING)
    first_match_offset = region_start_offset + submatches[0]["start"] if submatches else 0
    first_match_offset += 1
    first_match_offset_string_encoded = str(first_match_offset).encode(ENCODING)
    region_bytes = get_data_bytes(region)
    region_end_offset = region_start_offset + len(region_bytes)
    region_end_offset_string_encoded = str(region_end_offset).encode(ENCODING)
    if not is_data_utf8(region):
        formatted_region_bytes = INVALID_DATA_BYTES
    else:
        formatted_region_bytes = get_formatted_region(region_bytes, submatches)
    line_number_string_encoded = str(line_number).encode(ENCODING)
    file_path_bytes = get_data_bytes(file_path)
    file_path_bytes = os.path.abspath(file_path_bytes)
    file_path_bytes = os.path.normpath(file_path_bytes)
    file_path_base32_bytes = base64.b32encode(file_path_bytes)
    file_basename_bytes = os.path.basename(file_path_bytes)
    try:
        _ = file_basename_bytes.decode(ENCODING)
        file_basename_bytes = b"%b%b" % (BLUE_BYTES, file_basename_bytes)
    except UnicodeError:
        file_basename_bytes = INVALID_FILENAME_BYTES
    out.write(RESET_BYTES)
    out.write(MATCH_TYPE_BYTES)
    out.write(DELIMITER_BYTE)
    out.write(file_path_base32_bytes)
    out.write(DELIMITER_BYTE)
    out.write(region_start_offset_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(first_match_offset_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(region_end_offset_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(line_number_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(file_basename_bytes)
    out.write(RESET_BYTES)
    out.write(DELIMITER_BYTE)
    out.write(formatted_region_bytes)
    out.write(RESET_BYTES)
    out.write(NULL_BYTE)
    out.flush()

def write_error_item(error_type, error_message):
    error_message_bytes = error_message.encode(ENCODING)
    error_message_base32_bytes = base64.b32encode(error_message_bytes)
    error_type_bytes = QUERY_ERROR_TYPE_BYTES if error_type == QUERY_ERROR_TYPE else RG_ERROR_TYPE_BYTES
    error_specifier_bytes = QUERY_ERROR_SPECIFIER_BYTES if error_type == QUERY_ERROR_TYPE else RG_ERROR_SPECIFIER_BYTES
    out.write(RESET_BYTES)
    out.write(error_type_bytes)
    out.write(DELIMITER_BYTE)
    out.write(error_message_base32_bytes)
    for _ in range(4):
        out.write(DELIMITER_BYTE)
    out.write(ONE_BYTE)
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
MATCH_TYPE = "match"
QUERY_ERROR_TYPE = "query-error"
RG_ERROR_TYPE = "rg-error"
MATCH_TYPE_BYTES = MATCH_TYPE.encode(ENCODING)
QUERY_ERROR_TYPE_BYTES = QUERY_ERROR_TYPE.encode(ENCODING)
RG_ERROR_TYPE_BYTES = RG_ERROR_TYPE.encode(ENCODING)
INVALID_FILENAME_BYTES = b"%bInvalid %b filename" % (RED_BYTES, ENCODING_BYTES)
INVALID_DATA_BYTES = b"%bInvalid %b data" % (RED_BYTES, ENCODING_BYTES)
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
        write_error_item(QUERY_ERROR_TYPE, str(exception))
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
    write_error_item(RG_ERROR_TYPE, error_message)
rg_process.wait()
