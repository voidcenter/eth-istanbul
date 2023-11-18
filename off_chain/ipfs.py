# coding:utf-8
"""

@time: 2023/11/14
"""
import json
import os
from base64 import b64encode

import requests
from loguru import logger
from dotenv import load_dotenv


load_dotenv()


class IPFSClient:
    headers: dict

    def __init__(self):
        self.key = os.getenv("IPFS_KEY")
        self.secret = os.getenv("IPFS_SECRET")
        self.endpoint = "https://ipfs.infura.io:5001"
        self.init_header()
        # https://ipfs.io/ipfs/QmdnZPFMKSLNuLeYkPFtDp2veLNHwpr12xV3i66nTmKnme

    def init_header(self):
        self.headers = {}
        self.init_header_auth()

    def init_header_auth(self):
        auth = b64encode(f"{self.key}:{self.secret}".encode("utf-8"))
        self.headers["Authorization"] = f"Basic {auth.decode('utf-8')}"

    def save_data(self, request_id: str, data: dict):
        files = {
            'file': json.dumps(data)
        }

        response1 = requests.post(self.endpoint + '/api/v0/add', headers=self.headers, files=files)
        _hash = response1.json()["Hash"]
        logger.info(f"Create ipfs with request_id: {request_id}, hash: {_hash}")
        return _hash

    def read_data(self, ipfs_key):
        params = (
            ('arg', ipfs_key),
        )

        response = requests.post(self.endpoint + '/api/v0/block/get', headers=self.headers, params=params)

        print(response.text)


if __name__ == '__main__':
    ic = IPFSClient()
    ic.read_data("QmbYATT9cfirSRiHr6xFgVyXm9F8sPQZHPe8b3XpySKg3j")
    # print(ic.save_data("test_id", {
    #     "test": "ok"
    # }))
