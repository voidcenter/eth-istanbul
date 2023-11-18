# coding:utf-8
"""

@time: 2023/11/14
"""
import json
from base64 import b64encode

import requests
from loguru import logger


class IPFSClient:
    headers: dict

    def __init__(self):
        self.key = "2HxMTX76fFTZUk8pUNL14Y2JaWy"
        self.secret = "66fb6b9c58e5ec67a925bcd6a0bb4649"
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

    def read_data(self):
        pass


if __name__ == '__main__':
    ic = IPFSClient()
    print(ic.save_data("test_id", {
        "test": "ok"
    }))
