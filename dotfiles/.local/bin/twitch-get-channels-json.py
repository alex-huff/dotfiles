#!/bin/python3

from itertools import batched, compress, chain
import json
from multiprocessing.dummy import Pool
import requests
import sys

# https://kawcco.com/twitch-graphql-api

ENDPOINT = "https://gql.twitch.tv/gql"
STREAM_ID_QUERY = """\
query($login: String!) {
    user(login: $login) {
        login,
        profileImageURL(width: 600),
        stream {
            title,
            viewersCount,
            previewImageURL(width: 640, height: 360)
        }
    }
}\
"""
TWITCH_CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"
BATCH_SIZE = 35
MAX_CONCURRENT_REQUESTS = 4


def grab_channels_over_stdin():
    channel_names = list(map(str.rstrip, sys.stdin))
    multi_queries = [
        [
            {"query": STREAM_ID_QUERY, "variables": {"login": channel}}
            for channel in channel_batch
        ]
        for channel_batch in batched(channel_names, n=BATCH_SIZE)
    ]

    thread_pool = Pool(MAX_CONCURRENT_REQUESTS)
    try:
        responses = thread_pool.map(
            lambda multi_query: requests.post(
                ENDPOINT, json=multi_query, headers={"client-id": TWITCH_CLIENT_ID}
            ).json(),
            multi_queries,
        )
    finally:
        thread_pool.close()
        thread_pool.join()

    return [response["data"]["user"] for response in chain.from_iterable(responses)]


try:
    print(json.dumps(grab_channels_over_stdin()))
except:
    print("Failed to filter channels", file=sys.stderr)
