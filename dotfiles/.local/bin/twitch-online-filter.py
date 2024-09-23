#!/bin/python

import sys
from itertools import batched, chain
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

usernames = list(map(str.rstrip, sys.stdin))
multi_queries = [
    [
        {"query": STREAM_ID_QUERY % username, "variables": {}}
        for username in username_batch
    ]
    for username_batch in batched(usernames, n=BATCH_SIZE)
]
responses = [
    requests.post(
        ENDPOINT,
        json=multi_query,
        headers={"client-id": TWITCH_CLIENT_ID},
    ).json()
    for multi_query in multi_queries
]
query_responses = chain.from_iterable(responses)
users = (query_response["data"]["user"] for query_response in query_responses)
stream_datas = (user["stream"] if user != None else False for user in users)
online = "\n".join(
    username for username, stream_data in zip(usernames, stream_datas) if stream_data
)
if online:
    print(online)
