# coding:utf-8
"""

@time: 2023/11/11
"""

from web3 import Web3
from web3.middleware import geth_poa_middleware


def get_w3(endpoint):
    return Web3(
        Web3.HTTPProvider(endpoint, request_kwargs={'timeout': 60 * 10}),
        middlewares=[geth_poa_middleware]
    )
