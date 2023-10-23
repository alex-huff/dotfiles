#!/bin/python

import sys
import argparse
import json
from urllib.parse import urlparse, parse_qs, unquote

OTPAUTH = "otpauth"
TOTP = "totp"
HOTP = "hotp"
PROTOS = (TOTP, HOTP)
SECRET = "secret"
COUNTER = "counter"

parser = argparse.ArgumentParser(
    prog="extract-google-authenticator-params-from-uris",
    description="Extract google authenticator information from google's key URI format over stdin",
)
_ = parser.parse_args()
uris = list(map(str.rstrip, sys.stdin))
result_dicts = []
for uri in uris:
    parse_result = urlparse(uri)
    scheme = parse_result.scheme
    proto = parse_result.netloc
    if scheme != OTPAUTH:
        print(f"uri: {uri} had an invalid scheme", file=sys.stderr)
        exit(1)
    if proto not in PROTOS:
        print(f"uri: {uri} had an invalid protocol", file=sys.stderr)
        exit(1)
    result_dict = {}
    parameters = parse_qs(parse_result.query)
    if SECRET not in parameters:
        print(f"uri: {uri} had no {SECRET} parameter", file=sys.stderr)
        exit(1)
    if proto == HOTP and COUNTER not in parameters:
        print(f"uri: {uri} for key of type {HOTP} did not have {COUNTER} parameter", file=sys.stderr)
        exit(1)
    label = unquote(parse_result.path)[1:]
    result_dict["proto"] = proto
    result_dict["parameters"] = parameters
    result_dict["label"] = label
    result_dicts.append(result_dict)
print(json.dumps(result_dicts))
