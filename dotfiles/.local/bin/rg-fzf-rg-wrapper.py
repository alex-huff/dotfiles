#!/bin/python3

import os
import sys
from subprocess import Popen, DEVNULL, PIPE
import math
import base64
import json

# match item input format
# match
# ":"<base32 encoded absolute path>
# ":"<byte offset of first match>
# ":"<line number of start of region>
# ":"<line number of first match>
# ":"<line number of end of region>
# ":"<unicode string basename> | non-<encoding> filename
# ":"<unicode string match without null bytes> | non-<encoding> data
# "\0"

# query-error/rg-error item input format
# error
# ":"<base32 encoded error message>
# ":"b""
# ":"b""
# ":"1
# ":"b""
# ":"Query error | rg error
# "\0"


class RGOptions:
    def __init__(self):
        self.paths = []
        self.arguments = []

    def __getattr__(self, attribute):
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

    def add_paths(self, *paths):
        self.paths.extend(os.path.expanduser(path) for path in paths if path)
        return self

    def add_path(self, path):
        return self.add_paths(path)

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


def get_utf8_encoded_codepoint_length(first_byte):
    if first_byte >> 7 == 0b0:
        return 1
    elif first_byte >> 5 == 0b110:
        return 2
    elif first_byte >> 4 == 0b1110:
        return 3
    elif first_byte >> 3 == 0b11110:
        return 4
    else:
        raise UnicodeError("Invalid first byte for UTF-8 code point")


def process_region(region, first_match_byte, submatches):
    """Processes the "lines" region of a match message.

    Returns a tuple containing:
    1. The UTF-8 encoded bytearray with ANSI escape sequences that highlight
    submatches.
    2. The total number of lines in the region.
    3. The offset of the line relative to the region start that contains the first
    match.

    In the case that the given region is not valid UTF-8, a placeholder indicating
    that the data was not valid UTF-8 is returned as the bytearray.

    The returned bytearray will not represent more than MAX_DISPLAYED_LINES lines
    or MAX_DISPLAYED_CODEPOINTS codepoints. In the case that the region contains
    more than the maximum for either lines or codepoints, the region is truncated
    and shifted so that the first visible submatch is somewhere in the middle of
    the returned bytearray. When data at the beginning of the region is truncated,
    the returned bytearray will be prefixed with the continuation marker defined by
    CONTINUATION_MARKER_BYTES. When data at the end of the region is truncated, the
    returned bytearray will end with the same continuation marker.

    In the case that the given region is valid UTF-8 and a null byte is
    encountered, it will be replaced with the ASCII representation: \\x00 when
    added to the returned bytearray.

    In the case that the given region is valid UTF-8 and a highlighted region
    begins or ends in the middle of a multi-byte UTF-8 codepoint, the individual
    bytes of that codepoint are added to the returned bytearray in an ASCII
    representation similar to \\xFF. This is to prevent escape sequences splitting
    up UTF-8 codepoints in a way that the resulting bytearray is not valid UTF-8
    anymore.
    """
    def generate_escapes():
        """Generates the position and bytes of each escape sequence that should be
        injected into the bytes of the formatted region. Submatches that are empty do
        not generate highlight or reset escape sequences. Consecutive submatches are
        squashed together so that only one highlight escape and one reset escape are
        generated.
        """
        def update_current_and_next():
            nonlocal current_submatch, next_submatch
            if i < len(submatches):
                current_submatch = submatches[i]
                next_submatch = submatches[i + 1] if i + \
                    1 < len(submatches) else None
            else:
                current_submatch = next_submatch = None

        def increment_current_and_next():
            nonlocal i
            i += 1
            update_current_and_next()

        i = 0
        current_submatch = next_submatch = None
        update_current_and_next()
        while current_submatch:
            while current_submatch and current_submatch["start"] == current_submatch["end"]:
                increment_current_and_next()
            if not current_submatch:
                break
            yield current_submatch["start"], WHITE_FOREGROUND_BLACK_BACKGROUND_BYTES
            while next_submatch and current_submatch["end"] == next_submatch["start"]:
                increment_current_and_next()
            yield current_submatch["end"], RESET_FOREGROUND_BACKGROUND_BYTES
            increment_current_and_next()
        yield math.inf, None

    def should_start_displaying():
        within_max_lines_from_first_highlight = (
            first_highlight_lines_encountered - lines_encountered) <= MAX_DISPLAYED_LINES // 2
        within_max_codepoints_from_first_highlight = (
            first_highlight_codepoints_encountered - codepoints_encountered) <= MAX_DISPLAYED_CODEPOINTS // 2
        return within_max_lines_from_first_highlight and within_max_codepoints_from_first_highlight

    just_found_newline = False
    lines_encountered = 0
    first_match_line_number = 0
    should_display_region = is_data_utf8(region)
    if should_display_region:
        region_bytes = get_utf8_data_bytes(region)
        processed_region_bytes = bytearray()
        codepoints_encountered = -1
        codepoints_displayed = 0
        lines_displayed = 0
        currently_representing_bytes_as_ascii = False
        currently_displaying = False
        finished_displaying = False
        escapes_generator = generate_escapes()
        next_escape_position, next_escape = next(escapes_generator)
        if next_escape:
            first_highlight_lines_encountered = 0
            first_highlight_codepoints_encountered = 0
            current_codepoint_end = -1
            i = 0
            while i < next_escape_position:
                byte = region_bytes[i]
                if byte in NEWLINE_BYTE:
                    first_highlight_lines_encountered += 1
                first_highlight_codepoints_encountered += 1
                i += get_utf8_encoded_codepoint_length(byte)
            currently_displaying = False
        else:
            currently_displaying = True
        current_codepoint_end = -1
    else:
        region_bytes = get_non_utf8_data_bytes(region)
        processed_region_bytes = PLACEHOLDER_DATA_BYTES
    for i, byte in enumerate(region_bytes):
        if just_found_newline:
            lines_encountered += 1
        just_found_newline = byte in NEWLINE_BYTE
        if just_found_newline:
            if i < first_match_byte:
                first_match_line_number += 1
            if should_display_region and currently_displaying:
                lines_displayed += 1
        if not should_display_region or finished_displaying:
            continue
        at_start_of_codepoint = i > current_codepoint_end
        if at_start_of_codepoint:
            codepoints_encountered += 1
            current_codepoint_end = i + \
                get_utf8_encoded_codepoint_length(byte) - 1
            if not currently_displaying:
                currently_displaying = should_start_displaying()
                if currently_displaying and codepoints_encountered > 0:
                    processed_region_bytes.extend(BLUE_FOREGROUND_BYTES)
                    processed_region_bytes.extend(CONTINUATION_MARKER_BYTES)
                    processed_region_bytes.extend(RESET_FOREGROUND_BYTES)
                    previous_byte_was_newline = region_bytes[i -
                                                             1] in NEWLINE_BYTE
                    if previous_byte_was_newline:
                        processed_region_bytes.extend(NEWLINE_BYTE)
            else:
                codepoints_displayed += 1
            if currently_displaying:
                if lines_displayed == MAX_DISPLAYED_LINES or codepoints_displayed == MAX_DISPLAYED_CODEPOINTS:
                    should_print_continuation = not just_found_newline or i < len(
                        region_bytes) - 1
                    if should_print_continuation:
                        processed_region_bytes.extend(RESET_BYTES)
                        if just_found_newline:
                            processed_region_bytes.extend(NEWLINE_BYTE)
                        processed_region_bytes.extend(BLUE_FOREGROUND_BYTES)
                        processed_region_bytes.extend(
                            CONTINUATION_MARKER_BYTES)
                    finished_displaying = True
                    currently_displaying = False
                    continue
        if not currently_displaying:
            continue
        if i == next_escape_position:
            processed_region_bytes.extend(next_escape)
            next_escape_position, next_escape = next(escapes_generator)
        if at_start_of_codepoint:
            in_codepoint_split_by_escape = next_escape_position <= current_codepoint_end
        should_represent_byte_as_ascii = in_codepoint_split_by_escape or byte in NULL_BYTE
        if should_represent_byte_as_ascii:
            if not currently_representing_bytes_as_ascii:
                currently_representing_bytes_as_ascii = True
                processed_region_bytes.extend(UNDERLINE_BYTES)
            processed_region_bytes.extend(b"\\x%02X" % byte)
        else:
            if currently_representing_bytes_as_ascii:
                currently_representing_bytes_as_ascii = False
                processed_region_bytes.extend(NOT_UNDERLINE_BYTES)
            processed_region_bytes.append(byte)
    return processed_region_bytes, lines_encountered + 1, first_match_line_number


def write_match_item(rg_message):
    rg_data = rg_message["data"]
    absolute_offset_byte = rg_data["absolute_offset"]
    file_path = rg_data["path"]
    submatches = rg_data["submatches"]
    first_match_byte = submatches[0]["start"] if submatches else 0
    region = rg_data["lines"]
    region_bytes, num_lines, first_match_line_number = process_region(
        region,
        first_match_byte,
        submatches
    )
    absolute_start_line_number = rg_data["line_number"]
    absolute_start_line_number_string_encoded = str(
        absolute_start_line_number).encode(ENCODING)
    absolute_first_match_line_number = absolute_start_line_number + first_match_line_number
    absolute_first_match_line_number_string_encoded = str(
        absolute_first_match_line_number).encode(ENCODING)
    absolute_end_line_number = absolute_start_line_number + (num_lines - 1)
    absolute_end_line_number_string_encoded = str(
        absolute_end_line_number).encode(ENCODING)
    absolute_first_match_byte = absolute_offset_byte + first_match_byte + 1
    absolute_first_match_byte_string_encoded = str(
        absolute_first_match_byte).encode(ENCODING)
    file_path_bytes = get_data_bytes(file_path)
    file_path_bytes = os.path.abspath(file_path_bytes)
    file_path_bytes = os.path.normpath(file_path_bytes)
    file_path_base32_bytes = base64.b32encode(file_path_bytes)
    file_basename_bytes = os.path.basename(file_path_bytes)
    try:
        _ = file_basename_bytes.decode(ENCODING)
        file_basename_bytes = b"%b%b" % (
            BOLD_UNDERLINE_BYTES, file_basename_bytes)
    except UnicodeError:
        file_basename_bytes = PLACEHOLDER_FILENAME_BYTES
    out.write(RESET_BYTES)
    out.write(MATCH_TYPE_BYTES)
    out.write(DELIMITER_BYTE)
    out.write(file_path_base32_bytes)
    out.write(DELIMITER_BYTE)
    out.write(absolute_first_match_byte_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(absolute_start_line_number_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(absolute_first_match_line_number_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(absolute_end_line_number_string_encoded)
    out.write(DELIMITER_BYTE)
    out.write(file_basename_bytes)
    out.write(RESET_BYTES)
    out.write(DELIMITER_BYTE)
    out.write(region_bytes)
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
    for _ in range(3):
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
help_message = """\
ripgrep command manipulation:
    rg.push_arg(arg), rg.push_args(*args), rg.push_long_arg(arg, *values)
    rg.pop_arg(num=1)
    rg.add_path(path), rg.add_paths(*paths)

    rg.some_arg()               # same as --some-arg
    rg.some_arg(value1, value2) # same as --some-arg=value1 --some-arg=value2

    temporarily disable an argument like so:
        rg.some_arg()           # --some-arg enabled
        rg.some_arg().pop_arg() # --some-arg disabled

    temporarily disable a path like so:
        rg.add_path("~/foo")   # ~/foo enabled
        rg.add_path("~/foo"*0) # ~/foo disabled

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
MAX_DISPLAYED_CODEPOINTS = 2 ** 11 - 1
MAX_DISPLAYED_LINES = 2 ** 4 - 1
ENCODING = "utf-8"
CSI_CHARACTER_ATTRIBUTES_TEMPLATE = b"\033[%bm"
WHITE_FOREGROUND_BLACK_BACKGROUND_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"38;2;249;245;215;48;5;7"
BLUE_FOREGROUND_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"34"
RED_FOREGROUND_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"31"
UNDERLINE_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"4"
BOLD_UNDERLINE_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"1;4"
RESET_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"0"
RESET_FOREGROUND_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"39"
RESET_FOREGROUND_BACKGROUND_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"39;49"
NOT_UNDERLINE_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % b"24"
CONTINUATION_MARKER_BYTES = "…".encode(ENCODING)
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
PLACEHOLDER_FILENAME_BYTES = b"%bNon-UTF-8 filename" % RED_FOREGROUND_BYTES
PLACEHOLDER_DATA_BYTES = b"%bNon-UTF-8 data" % RED_FOREGROUND_BYTES
QUERY_ERROR_SPECIFIER_BYTES = b"%bQuery error" % RED_FOREGROUND_BYTES
RG_ERROR_SPECIFIER_BYTES = b"%brg error" % RED_FOREGROUND_BYTES
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
rg_process = Popen(rg_command, stdin=DEVNULL, stdout=PIPE,
                   stderr=PIPE, encoding=ENCODING)
for rg_json in rg_process.stdout:
    rg_message = json.loads(rg_json)
    if rg_message["type"] != "match":
        continue
    write_match_item(rg_message)
error_message = rg_process.stderr.read()
if error_message:
    write_error_item(RG_ERROR_SPECIFIER_BYTES, error_message)
rg_process.wait()
