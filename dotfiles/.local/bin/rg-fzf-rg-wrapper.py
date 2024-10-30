#!/bin/python3

import os
import sys
from subprocess import Popen, DEVNULL, PIPE
import base64
import json

# fzf item input format
# <base32 encoded absolute path>
# ":"<byte offset inclusive beginning of region>
# ":"<byte offset of first match>
# ":"<byte offset exclusive end of region>
# ":"<line number of beginning of region>
# ":"(<unicode string basename> | "Invalid <encoding> filename")
# ":"(<unicode string match without null bytes> | "Invalid <encoding> data")
# "\0"

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

def write_item(rg_message):
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
        file_basename_bytes = b"%b%b" % (MAGENTA_BYTES, file_basename_bytes)
    except UnicodeError:
        file_basename_bytes = INVALID_FILENAME_BYTES
    out.write(RESET_BYTES)
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

CSI_CHARACTER_ATTRIBUTES_TEMPLATE = b"\033[%bm"
GREEN_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"32")
MAGENTA_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"35")
RED_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"31")
RESET_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"0")
DELIMITER_BYTE = b":"
NULL_BYTE = b"\0"
EMPTY_BYTE = b""
ENCODING = "utf-8"
ENCODING_BYTES = b"utf-8"
INVALID_FILENAME_BYTES = b"%bInvalid %b filename" % (RED_BYTES, ENCODING_BYTES)
INVALID_DATA_BYTES = b"%bInvalid %b data" % (RED_BYTES, ENCODING_BYTES)
rg_command = [
    "/bin/rg",
    "--line-number",
    "--smart-case",
    "--json",
]
rg_command.extend(sys.argv[i] for i in range(1, len(sys.argv)))
rg_process = Popen(rg_command, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, text=True, encoding=ENCODING)
out = sys.stdout.buffer
for rg_json in rg_process.stdout:
    rg_message = json.loads(rg_json)
    if rg_message["type"] != "match":
        continue
    write_item(rg_message)
rg_process.wait()
