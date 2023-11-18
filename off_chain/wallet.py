# coding:utf-8
"""

@time: 2023/11/13
"""

from eth_account.account import Account
from eth_account.signers.local import LocalAccount

from off_chain.client import EVMClient


class Wallet:
    def __init__(self, pk: str, client: EVMClient):
        self.sender: LocalAccount = Account.from_key(pk)
        self.client = client

    def call_contact(self, function):
        tx = function.build_transaction(
            {
                "chainId": self.client.chain_id,
                "from": self.sender.address,
                "nonce": self.get_nonce()
            })
        signed_tx = self.sender.sign_transaction(tx)
        txn_hash = self.client.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        txn_receipt = self.client.w3.eth.wait_for_transaction_receipt(txn_hash)
        return txn_receipt

    def get_nonce(self):
        return self.client.w3.eth.get_transaction_count(self.sender.address)

