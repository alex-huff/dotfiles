#!/bin/python

import sys
import requests

ENDPOINT = "https://gql.twitch.tv/gql"
STREAM_ID_QUERY = """\
query {{
    user(login: "{username}") {{
        stream {{
            id
        }}
    }}
}}\
"""
TWITCH_CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"

usernames = list(map(str.rstrip, sys.stdin))
multi_query = [
    {"query": STREAM_ID_QUERY.format(username=username), "variables": {}}
    for username in usernames
]
response = requests.post(
    ENDPOINT,
    json=multi_query,
    headers={"client-id": TWITCH_CLIENT_ID},
).json()
users = (query_response["data"]["user"] for query_response in response)
stream = "stream"
stream_datas = (user[stream] if user != None else False for user in users)
online = "\n".join(
    username for username, stream_data in zip(usernames, stream_datas) if stream_data
)
if online:
    print(online)
