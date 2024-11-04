#!/bin/python3

import os
import sys
import math
from subprocess import check_output

def relay_file(buffer, from_file, to_file, num_bytes=None):
    buffer_view = memoryview(buffer)
    till_eof = num_bytes == None
    bytes_left = math.inf if till_eof else num_bytes
    while bytes_left > 0:
        to_read = len(buffer) if till_eof else min(len(buffer), bytes_left)
        bytes_read = from_file.readinto(buffer_view[0:to_read])
        if bytes_read == 0:
            break
        to_file.write(buffer_view[0:bytes_read])
        bytes_left -= bytes_read

script_basename = os.path.basename(sys.argv[0])
if len(sys.argv) != 4:
    print(f"Usage: {script_basename} <start offset inclusive> <end offset exclusive> <file>", file=sys.stderr)
    sys.exit(1)
try:
    start_offset = int(sys.argv[1])
    end_offset = int(sys.argv[2])
except ValueError:
    print("Invalid offsets", file=sys.stderr)
    sys.exit(1)
file_path = sys.argv[3]
if not os.path.isfile(file_path):
    print("Invalid file", file=sys.stderr)
    sys.exit(1)
out = sys.stdout.buffer
file_command = [
    "/bin/file",
    "--brief",
    "--mime-encoding",
    file_path
]
CSI_CHARACTER_ATTRIBUTES_TEMPLATE = b"\033[%bm"
BLACK_BG_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"40")
RESET_BG_BYTES = CSI_CHARACTER_ATTRIBUTES_TEMPLATE % (b"49")
guessed_mime_encoding = check_output(file_command, text=True).rstrip()
if guessed_mime_encoding not in ("us-ascii", "utf-8"):
    out.write(BLACK_BG_BYTES)
    out.write(b"Binary data")
    out.write(RESET_BG_BYTES)
    sys.exit(1)
with open(file_path, "rb") as file:
    buffer = bytearray(2 ** 12)
    relay_file(buffer, file, out, num_bytes=start_offset)
    out.write(BLACK_BG_BYTES)
    relay_file(buffer, file, out, num_bytes=end_offset - start_offset)
    out.write(RESET_BG_BYTES)
    relay_file(buffer, file, out)
