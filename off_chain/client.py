# coding:utf-8
"""

@time: 2023/11/9
"""
import os

import requests
from web3.types import FilterParams
from dotenv import load_dotenv

from off_chain.util import get_w3
from off_chain.erc20 import ERC20Contract


load_dotenv()


class Client:
    chain_id: int

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.w3 = get_w3(endpoint)
        self.chain_id = self.w3.eth.chain_id


class EVMClient(Client):

    def __init__(self, scan_endpoint, scan_key, endpoint):
        self.scan_key = scan_key
        self.scan_endpoint = scan_endpoint
        super().__init__(endpoint)
        self.erc20 = ERC20Contract(endpoint)

    def address_native_balance(self, address: str) -> int:
        return self.w3.eth.get_balance(address)

    def address_nonce(self, address: str):
        return self.w3.eth.get_transaction_count(address)

    def address_age(self, address: str) -> int:
        url = f"{self.scan_endpoint}?" \
              f"module=account&action=txlist&" \
              f"address={address}&startblock=0&endblock=9999999999&page=1&offset=1&sort=asc&apikey={self.scan_key}"
        result = requests.get(url).json()
        if len(result["result"]) == 0:
            return 0
        return int(result["result"][0]["timeStamp"])

    def token_balance(self, addr, token):
        return self.erc20.balance_of(token, addr)

    def get_logs(self, address, from_block, to_block, topics):
        return self.w3.eth.get_logs(
            FilterParams(
                address=address,
                fromBlock=from_block,
                toBlock=to_block,
                topics=topics
            )
        )

    def usd_balance(self, address):
        native_balance = self.address_native_balance(address)
        total_balance = native_balance * self.prices["native"] / 10**18
        for name, token in self.tokens.items():
            token_balance = self.token_balance(address, token)
            decimals = self.decimals.get(name)
            total_balance += (self.prices.get(name) * token_balance/10**decimals)
        return total_balance


class ETHClient(EVMClient):
    scan_endpoint = "https://api.etherscan.io/api"
    scan_key = os.getenv('ETH_SCAN_KEY')
    endpoint = "https://eth.getblock.io/mainnet/8cda9c8c-af5d-4278-bbeb-9b08b7991279/"

    prices = {
        "native": 2000,
        "weth": 2000,
        "usdt": 1,
        "usdc": 1
    }

    decimals = {
        "weth": 18,
        "usdt": 6,
        "usdc": 6,
    }

    tokens = {
        "weth": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    }

    def __init__(self):
        super().__init__(self.scan_endpoint, self.scan_key, self.endpoint)


class GoerliClient(EVMClient):
    scan_endpoint = "https://api-goerli.etherscan.io/api"
    scan_key = os.getenv('GOERLI_SCAN_KEY')
    endpoint = "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"

    prices = {
        "native": 2000,
        "weth": 2000,
    }

    decimals = {
        "weth": 18
    }

    tokens = {
        "weth": "0xb4fbf271143f4fbf7b91a5ded31805e42b2208d6"
    }

    def __init__(self):
        super().__init__(self.scan_endpoint, self.scan_key, self.endpoint)


class GnosisClient(EVMClient):
    scan_endpoint = "https://api.gnosisscan.io/api"
    scan_key = os.getenv('GNOSIS_SCAN_KEY')
    endpoint = "https://rpc.gnosis.gateway.fm"

    prices = {
        "native": 1,
        "usdt": 1,
        "usdc": 1,
    }

    decimals = {
        "usdt": 6,
        "usdc": 6,
    }

    tokens = {
        "usdt": "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",
        "usdc": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
    }

    def __init__(self):
        super().__init__(self.scan_endpoint, self.scan_key, self.endpoint)


class PolygonClient(EVMClient):
    scan_endpoint = "https://api.polygonscan.com/api"
    scan_key = os.getenv('POLYGON_SCAN_KEY')
    endpoint = "https://polygon-bor.publicnode.com"

    prices = {
        "native": 0.93,
        "wmatic": 0.93,
        "usdt": 1,
        "usdc": 1
    }

    decimals = {
        "wmatic": 18,
        "usdc": 6,
        "usdt": 6,
    }

    tokens = {
        "wmatic": "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
        "usdc": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
        "usdt": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f"
    }

    def __init__(self):
        super().__init__(self.scan_endpoint, self.scan_key, self.endpoint)


if __name__ == '__main__':
    gc = PolygonClient()
    print(gc.address_native_balance("0xFbCF4d80d3c267876F6795C02aAB10DE751Da8A4"))
    print(gc.address_nonce("0xFbCF4d80d3c267876F6795C02aAB10DE751Da8A4"))
    print(gc.address_age("0xFbCF4d80d3c267876F6795C02aAB10DE751Da8A4"))
    # print(gc.usd_balance("0xF25b29d208efb66d1007e11d2457Df213F7B1e64"))
