#!/bin/python3

import sys
from itertools import batched, compress, chain
from multiprocessing.dummy import Pool
import requests

ENDPOINT = "https://gql.twitch.tv/gql"
STREAM_ID_QUERY = """\
query {
    user(login: "%s") {
        stream {
            id
        }
    }
}\
"""
TWITCH_CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"
BATCH_SIZE = 35
MAX_CONCURRENT_REQUESTS = 4


def filter_online_channels_over_stdin():
    channel_names = list(map(str.rstrip, sys.stdin))
    multi_queries = [
        [
            {"query": STREAM_ID_QUERY % channel, "variables": {}}
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
    channels = map(
        lambda query_response: query_response["data"]["user"],
        chain.from_iterable(responses),
    )
    online_selector = map(
        lambda channel: True if channel != None and channel["stream"] else False,
        channels,
    )
    return list(compress(channel_names, online_selector))


try:
    online_channels = filter_online_channels_over_stdin()
    if online_channels:
        print("\n".join(online_channels))
except:
    print("Failed to filter channels", file=sys.stderr)
