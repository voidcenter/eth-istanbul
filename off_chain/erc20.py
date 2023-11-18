# coding:utf-8
"""

@time: 2023/5/31
"""

import requests
from loguru import logger


class ERC20Contract:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def balance_of(self, token, address):
        balance: str = self.call(
            [
                {
                    "to": token,
                    "data": f"0x70a08231{address[2:].zfill(64)}"  # balanceOf(address)
                },
                "latest"
            ]
        )
        return int(balance, 16) if balance != "0x" else 0

    def call(self, params: []):
        res = requests.post(
            self.endpoint,
            json={
                "method": "eth_call",
                "params": params,
                "id": 1,
                "jsonrpc": "2.0"
            }
        )
        try:
            res_json = res.json()
            result = res_json.get("result")
            if result:
                return result
            else:
                err = res_json.get("error")
                logger.error(f"Request: {params} failed, err: {err}")
                return {}
        except Exception as e:
            return "0x0"
