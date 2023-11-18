# coding:utf-8
"""

@time: 2023/11/17
"""
import os
import time

from web3 import Web3
from dotenv import load_dotenv
from loguru import logger

from off_chain.client import GoerliClient
from off_chain.wallet import Wallet
from off_chain.abi import ABI

load_dotenv()


class UserReq:
    user_contract_address = Web3.to_checksum_address("0xc549d083fF7fef3025293bd44F3b31f63443Bf9a")
    oracle_address = Web3.to_checksum_address("0x2224E272bDea4568144fF4D5c78972012922DE2F")
    contract_abi = ABI

    all_events = {
        "0x730a0835abad09794876780683761cac554aa0af7bf3f8f443d82e7007df8829": "RequestReceived",
        "0x1131472297a800fee664d1d89cfa8f7676ff07189ecc53f80bbb5f4969099db8": "RequestSent",
        "0xdb1513f0abeb57a364db56aa3eb52015cca5268f00fd67bc73aaf22bccab02b7": "AssertionMade",
        "0x8d226cfd629623c6eb4995a6b5b9bb428dcdce089eaaef555ff378444ef7a03a": "ReputationScoreReceived",
        "0xf5fb6db7bf9a4bb01ab0c8cc79b8f8d65467f21c60a0f1cbc3fb608a0a3b9d0f": "ReputationScoreSent",
        "0x0d34780608e36acf97f9d23ab26fb39b6397f88e59e138c3fbc5d8aece40ee01": "ReputationScoreCommitted",
        "0xb7a47bdc713e6687bd5e47b987f185fdeddf7cee416886d56eb7b356239a4543": "UMAAssertionResolved",
        "0x09c84817895a69e4f9f22196529f0686d02b9424ba85cef1a5295e2d91fcf1e6": "AxiomVerificationSuccess"
    }
    all_contracts = [
        user_contract_address,  # user contract
        oracle_address,  # our oracle
    ]

    def __init__(self):
        self.client = GoerliClient()
        self.wallet = Wallet(os.getenv("WALLET_PK"), self.client)
        self.oracle_contract = self.client.w3.eth.contract(address=self.user_contract_address, abi=self.contract_abi)

    def start(self, addr):
        # 1. send request score
        # 2. wait for send request score
        # 3. wait for UMA
        start_block, request_id = self.request_score(addr)
        end_block = self.get_latest_block_number()

        logger.info("Wait for send request score")

        while True:
            if start_block >= end_block:
                time.sleep(12)
                end_block = self.get_latest_block_number()
                continue
            logs = self.client.get_logs(
                self.all_contracts, start_block, end_block,
                [list(self.all_events.keys())]
            )
            for log in logs:
                topic = log["topics"][0].hex()

                _request_id = ""

                if topic == "0x0d34780608e36acf97f9d23ab26fb39b6397f88e59e138c3fbc5d8aece40ee01" or \
                        topic == "0x8d226cfd629623c6eb4995a6b5b9bb428dcdce089eaaef555ff378444ef7a03a" or \
                        topic == "0xf5fb6db7bf9a4bb01ab0c8cc79b8f8d65467f21c60a0f1cbc3fb608a0a3b9d0f":
                    _request_id = log["topics"][1].hex()

                if topic == "0xb7a47bdc713e6687bd5e47b987f185fdeddf7cee416886d56eb7b356239a4543":
                    _request_id = log["topics"][2].hex()

                if topic == "0x09c84817895a69e4f9f22196529f0686d02b9424ba85cef1a5295e2d91fcf1e6":
                    _request_id = log["topics"][1].hex()
                    logger.info(f"Axiom query_id: {log['data'].hex()}")

                if _request_id != request_id:
                    continue

                event_name = self.all_events.get(topic)
                logger.info(f"Event: {event_name}")

                if topic == "0xb7a47bdc713e6687bd5e47b987f185fdeddf7cee416886d56eb7b356239a4543":
                    logger.info("Done")
                    return
            start_block = end_block + 1

    def request_score(self, addr: str):
        receipt = self.wallet.call_contact(
            self.oracle_contract.functions.requestReputationScore(
                Web3.to_checksum_address(addr),
                True,
                10 ** 8
            )
        )
        request_id = ""
        receipt = self.client.w3.eth.get_transaction_receipt(receipt["transactionHash"].hex())

        logger.info(f"User request score transaction sent: {receipt}")
        for log in receipt["logs"]:
            topic = log["topics"][0].hex()
            if topic in list(self.all_events.keys()):
                logger.info(f"Event: {self.all_events[topic]}")
            if topic == "0x730a0835abad09794876780683761cac554aa0af7bf3f8f443d82e7007df8829":
                request_id = log["topics"][1].hex()
                logger.info(f"Request_id: {request_id}")
        return receipt["blockNumber"], request_id

    def get_latest_block_number(self):
        return self.client.w3.eth.block_number


if __name__ == '__main__':
    ur = UserReq()
    address = "0xeB1c22baACAFac7836f20f684C946228401FF01C"
    ur.start(address)
