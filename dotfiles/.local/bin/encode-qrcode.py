#!/bin/python

import argparse
import cv2
import sys
import tempfile

parser = argparse.ArgumentParser(
    prog="encode-qrcode",
    description="Encode data from stdin to qrcode and write path to image on stdout",
)
parser.add_argument(
    "path_to_image",
    nargs="?",
    help=f"The path to save the encoded image. If ommited, the image will be saved to a temporary file",
)
arguments = parser.parse_args()
qrcode_encoder = cv2.QRCodeEncoder.create()
qrcode = qrcode_encoder.encode(sys.stdin.read())
path_to_image = arguments.path_to_image
if not path_to_image:
    path_to_image = tempfile.mktemp(suffix=".png")
cv2.imwrite(path_to_image, qrcode)
print(path_to_image)
