#!/bin/python

import argparse
import cv2

parser = argparse.ArgumentParser(
    prog="decode-qrcode",
    description="Decode qrcode within a supplied image sending data to stdout",
)
parser.add_argument(
    "path_to_image",
    help=f"path to the image to decode",
)
arguments = parser.parse_args()
image = cv2.imread(arguments.path_to_image)
qrcode_detector = cv2.QRCodeDetector()
data, bounding_box, transformed_qrcode = qrcode_detector.detectAndDecode(image)
print(data, end="")
