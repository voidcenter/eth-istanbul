# coding:utf-8
"""

@time: 2023/11/11
"""
import json
import math
import os
import time
from threading import Thread

from web3 import Web3
from eth_abi import abi
from loguru import logger
from dotenv import load_dotenv

from off_chain.client import (
    GoerliClient,
    ETHClient,
    PolygonClient,
    GnosisClient,
    LineaClient,
    PolygonZKEVMClient,
    ScrollClient,
    MantleClient
)
from off_chain.wallet import Wallet
from off_chain.abi import ABI
from off_chain.ipfs import IPFSClient
from off_chain.lens_protocol_api import LensProtocolAPI
from off_chain.ens_api import ENSAPI
from off_chain.open_ai import generate_text
from off_chain.axiom_quick_start.run import Axiom


load_dotenv()


class Listener:
    all_chain_class = {
        1: ETHClient,
        5: GoerliClient,
        137: PolygonClient,
        100: GnosisClient,
        59140: LineaClient,
        1442: PolygonZKEVMClient,
        534351: ScrollClient,
        5001: MantleClient,
    }

    chain_address_mapping = {
        5: {
            "user": Web3.to_checksum_address("0xc549d083fF7fef3025293bd44F3b31f63443Bf9a"),
            "oracle": Web3.to_checksum_address("0x2224E272bDea4568144fF4D5c78972012922DE2F"),
            "uma": Web3.to_checksum_address("0x9923d42ef695b5dd9911d05ac944d4caca3c4eab"),
            "axiom": Web3.to_checksum_address("0xf15cc7B983749686Cd1eCca656C3D3E46407DC1f")
        },
        100: {
            "user": Web3.to_checksum_address("0x4CdEcc2C9f569F52f9B3d9B00cbDE4A323A0B911"),
            "oracle": Web3.to_checksum_address("0x93838Ac1D8f469Ef466D50cA8Aa294ACe94dD612"),
        },
        1442: {
            "user": Web3.to_checksum_address("0x51dec4Eb917c138575C508ccB9a267c2eDE83784"),
            "oracle": Web3.to_checksum_address("0xfA89863E6B51694ccc0bDFe641E00F0355c2fb6c"),
        },
        534351: {
            "user": Web3.to_checksum_address("0x51dec4Eb917c138575C508ccB9a267c2eDE83784"),
            "oracle": Web3.to_checksum_address("0xfA89863E6B51694ccc0bDFe641E00F0355c2fb6c"),
        },
        59140: {
            "user": Web3.to_checksum_address("0x51dec4Eb917c138575C508ccB9a267c2eDE83784"),
            "oracle": Web3.to_checksum_address("0xfA89863E6B51694ccc0bDFe641E00F0355c2fb6c"),
        },
        5001: {
            "user": Web3.to_checksum_address("0x51dec4Eb917c138575C508ccB9a267c2eDE83784"),
            "oracle": Web3.to_checksum_address("0xfA89863E6B51694ccc0bDFe641E00F0355c2fb6c"),
        }
    }

    topic_RR = "0x730a0835abad09794876780683761cac554aa0af7bf3f8f443d82e7007df8829"
    topic_Assertion = "0xdb1513f0abeb57a364db56aa3eb52015cca5268f00fd67bc73aaf22bccab02b7"
    axiom_VFS = "0x09c84817895a69e4f9f22196529f0686d02b9424ba85cef1a5295e2d91fcf1e6"

    all_events = {
        topic_RR: "RequestReceived",
        "0x1131472297a800fee664d1d89cfa8f7676ff07189ecc53f80bbb5f4969099db8": "RequestSent",
        topic_Assertion: "AssertionMade",
        "0x8d226cfd629623c6eb4995a6b5b9bb428dcdce089eaaef555ff378444ef7a03a": "ReputationScoreReceived",
        "0xf5fb6db7bf9a4bb01ab0c8cc79b8f8d65467f21c60a0f1cbc3fb608a0a3b9d0f": "ReputationScoreSent",
        "0x0d34780608e36acf97f9d23ab26fb39b6397f88e59e138c3fbc5d8aece40ee01": "ReputationScoreCommitted",
        "0xb7a47bdc713e6687bd5e47b987f185fdeddf7cee416886d56eb7b356239a4543": "UMAAssertionResolved",
        axiom_VFS: "AxiomVerificationSuccess",
    }
    contract_address: str
    user_address: str
    uma_address: str
    axiom_address: str
    all_contracts: list

    contract_abi = ABI
    oracle_contract = None
    wallet: Wallet
    assertion_exp = 12
    interact_with_mixer = {}
    interact_with_attacker = {}

    source_data = {
        "likely_human": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": True,
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": True,
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": False,
        },
        "compliant": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": True,
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": False,
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": True,
        },
        "score": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": 80,
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": -100,
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": 20,
        },
        "twitter": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": 185900,
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": 0,
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": 0,
        },
        "twitter_account": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": "richerd",
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": "",
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": "jaredmev_eth",
        },
        "likely_bot": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": False,
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": False,
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": True,
        },
        "number_of_non_compliant_interactions": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": 0,
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": 2,
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": 0,
        },
        "non_compliant_txn_list": {
            "0xeB1c22baACAFac7836f20f684C946228401FF01C": [],
            "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA": [
                {
                    "chain_id": 1,
                    "url": 'https://etherscan.io/tx/0xfeedbf51b4e2338e38171f6e19501327294ab1907ab44cfd2d7e7336c975ace7',
                    "attack_analysis": 'https://rekt.news/raft-rekt/'
                },
                {
                    "chain_id": 1,
                    "url": 'https://etherscan.io/tx/0x406949ff6d93a8dfa21b3ccbda7f444b93f019b262dcbd733a9ae714c602adef',
                    "interaction_with_mixer_name": 'Tornado.cash',
                    "interaction_with_mixer_url": 'https://etherscan.io/address/0xd90e2f925da726b50c4ed8d0fb90ad053324f31b',
                }
            ],
            "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13": [],
        }
    }

    def __init__(self, current_chain=5, from_block=None, to_block=None):
        if current_chain not in self.chain_address_mapping:
            raise ValueError(f"Chain: {current_chain} was not supported")

        self.all_chain_client = {chain_id: cl() for chain_id, cl in self.all_chain_class.items()}

        self.client = self.all_chain_client.get(current_chain)
        logger.info(f"Start with chain: {self.client.chain_id}")

        addresses_mapping = self.chain_address_mapping[current_chain]
        self.contract_address = addresses_mapping["oracle"]
        self.user_address = addresses_mapping["user"]
        self.uma_address = addresses_mapping.get("uma")
        self.axiom_address = addresses_mapping.get("axiom")
        self.all_contracts = list(addresses_mapping.values())

        self.from_block = self.get_latest_block_number() if from_block is None else from_block
        self.to_block = self.get_latest_block_number() if to_block is None else to_block
        self.lens_client = LensProtocolAPI()
        self.ens_client = ENSAPI()

        self.wallet = Wallet(os.getenv("WALLET_PK"), self.client)
        self.init_contract()
        self.ipfs_client = IPFSClient()

        self.axiom = Axiom(self.contract_address)

        self.uma_assertion = {}
        self.uma_assertion_request = {}
        self.axiom_done = {}
        uma_callback_thread = Thread(target=self.uma_callback)
        uma_callback_thread.start()

    def init_contract(self):
        self.oracle_contract = self.client.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)

    def get_checkpoint(self):
        with open("./checkpoint", "w+") as f:
            block_number = f.read()
            if block_number == "":
                return self.get_latest_block_number()
            return block_number

    def log_event(self, topic):
        event_name = self.all_events.get(topic)
        logger.info(f"Event: {event_name}")

    def listen(self):
        while True:
            if self.from_block >= self.to_block:
                time.sleep(12)
                self.to_block = self.get_latest_block_number()
                continue
            logs = self.client.get_logs(
                self.all_contracts, self.from_block, self.to_block,
                [list(self.all_events.keys())]
            )
            for log in logs:
                topic = log["topics"][0].hex()
                data = log["data"]

                self.log_event(topic)

                if topic == self.topic_RR:
                    request_id = log["topics"][1].hex()
                    block_number = log["blockNumber"]
                    request_addr = Web3.to_checksum_address("0x" + log["topics"][2].hex()[-40:])
                    # request_receive
                    address, nonce = self.request_received(data)
                    addresses = [address]
                    addresses = [Web3.to_checksum_address(addr) for addr in addresses]
                    self.request_receive(block_number, request_id, addresses, request_addr)

                # if topic == self.topic_Assertion:
                #     # callback to user contract
                #     assertion_id = log["topics"][1].hex()
                #     self.uma_assertion[assertion_id] = int(time.time()) + 2 * 60 + 12
                #     logger.info(f"Found assertion: {assertion_id}, txn_hash: {log['transactionHash'].hex()}")

                if topic == self.axiom_VFS:
                    request_id = log["topics"][1].hex()
                    self.axiom_done[request_id] = True

            self.from_block = self.to_block + 1

    def request_receive(self, block_number, request_id, addresses, request_addr):
        logger.info(f"Create score with request_id: {request_id}, address: {addresses[0]}")
        # calculate score
        scores = self.calculate_score(request_id, addresses)

        # ipfs
        ipfs_hash = self.ipfs_upload(request_id, scores)

        # callback to oracle contract
        try:
            receipt = self.contract_callback(block_number, request_id, scores, ipfs_hash)
            receipt = self.client.w3.eth.get_transaction_receipt(receipt["transactionHash"].hex())
            logger.info(f"Send score success, receipt: {receipt}")

            if self.uma_address is not None and self.user_address != "":
                for log in receipt["logs"]:
                    topic = log["topics"][0].hex()
                    if topic == self.topic_Assertion:
                        assertion_id = log["topics"][1].hex()
                        self.uma_assertion_request[assertion_id] = request_id
                        self.uma_assertion[assertion_id] = int(time.time()) + self.assertion_exp
                        logger.info(f"Found assertion: {assertion_id}, txn_hash: {log['transactionHash'].hex()}")

            if self.axiom_address is not None and self.axiom_address != "":
                # after that we call axiom
                self.axiom.call_axiom(8242852, 10060567, addresses[0], request_id)
                logger.info(f"Send Axiom success")
        except Exception as e:
            logger.error(f"Send score failed, block_number: {e}")

    def uma_callback(self):
        while True:
            time.sleep(12)
            current_time = time.time()
            checked = []
            for assertion_id, timestamp in self.uma_assertion.items():
                request_id = self.uma_assertion_request[assertion_id]
                if timestamp < current_time and request_id in self.axiom_done:
                    checked.append(assertion_id)
                    try:
                        receipt = self.wallet.call_contact(
                            self.oracle_contract.functions.settelUMAAssertion(
                                bytes.fromhex(assertion_id.removeprefix("0x")),
                            )
                        )
                        logger.info(f"Send settle UMA success, receipt: {receipt}")
                    except Exception as e:
                        logger.error(f"Failed to settle UMA, assertion_id: {assertion_id}, e: {e}")
                else:
                    logger.info(f"Assertion: {assertion_id} will be run after {int(timestamp - current_time)}s")
            logger.info(f"Total UMA callback checked: {len(checked)}, unchecked: {len(self.uma_assertion)}")
            for assertion_id in checked:
                del self.uma_assertion[assertion_id]
                request_id = self.uma_assertion_request[assertion_id]
                del self.axiom_done[request_id]
                del self.uma_assertion_request[assertion_id]

    def contract_callback(self, block_number, request_id, _evidence, ipfs_hash: str):
        # todo, how about batch
        score = _evidence["score"]
        chain_stats = _evidence["chain_stats"]

        evidence = {
            "chain_id": _evidence["chain_id"],
            "request_id": request_id,
            "address": _evidence["address"],
            "ens": _evidence["ens"],
            "usd_balance": chain_stats[self.client.chain_id]["usd_balance"],
            "all_chain_usd_balance": sum([v["usd_balance"] for v in chain_stats.values()]),
            "nonce": chain_stats[self.client.chain_id]["nonce"],
            "all_chain_max_nonce": max([v["nonce"] for v in chain_stats.values()]),
            "age": chain_stats[self.client.chain_id]["age"],
            "all_chain_max_age": max([v["age"] for v in chain_stats.values()]),
            "world_coin_confirmed": _evidence["world_coin_confirmed"],
            "lens_followers": _evidence["lens_followers"],
            "twitter_followers": _evidence["twitter_followers"],
            "is_human": _evidence["is_human"],
            "is_compliant": _evidence["is_compliant"],
            "score": _evidence["score"],
            "non_compliant_txns": _evidence["non_compliant_txns"],
            "ipfs_hash": ipfs_hash
        }

        receipt = self.wallet.call_contact(
            self.oracle_contract.functions.sendReputationScore(
                (
                    Web3.to_checksum_address(evidence["address"]),
                    score,
                    int(block_number),
                    bool(evidence["is_compliant"]),
                    bool(evidence["is_human"]),
                    (
                        evidence["world_coin_confirmed"],
                        evidence["lens_followers"],
                        evidence["twitter_followers"],
                        0,
                        evidence["ens"].encode("utf-8"),
                    ),
                    (
                        evidence["all_chain_max_nonce"],
                        evidence["nonce"],
                        evidence["all_chain_max_age"],
                        evidence["age"],
                        evidence["all_chain_usd_balance"],
                        evidence["usd_balance"]
                    ),
                    bytes.fromhex(request_id.removeprefix("0x")),
                    ipfs_hash.encode("utf-8")
                ),
                ipfs_hash.encode("utf-8")
            ),
        )
        return receipt

    def calculate_score(self, request_id, addresses: []):
        scores = {}
        current_time = int(time.time())
        for addr in addresses:
            ens = self.ens_name(addr)

            likely_human = self.source_data["likely_human"].get(addr, False)
            compliant = self.source_data["compliant"].get(addr, False)
            score = self.source_data["score"].get(addr, 0)
            twitter_follower = self.source_data["twitter"].get(addr, 0)
            likely_bot = self.source_data["likely_bot"].get(addr, 0)
            noncompliantTxns = self.source_data["number_of_non_compliant_interactions"].get(addr, 0)
            non_compliant_txn_list = self.source_data["non_compliant_txn_list"].get(addr, [])
            twitter_account = self.source_data["twitter_account"].get(addr, "")

            lens_follower, is_world_coin = self.lens_followers(addr)

            balances = self.all_chain_balance(addr)
            ages, nonces = self.all_chain_age(addr)

            chain_stats = {}
            for chain_id in self.all_chain_client.keys():
                chain_stats[chain_id] = {
                    "usd_balance": int(balances.get(chain_id)),
                    "nonce": nonces.get(chain_id),
                    "age": ages.get(chain_id),
                }

            current_usd_balance = chain_stats[self.client.chain_id]["usd_balance"]
            current_age = chain_stats[self.client.chain_id]["age"]
            current_nonce = chain_stats[self.client.chain_id]["nonce"]

            scores = {
                "chain_id": self.client.chain_id,
                "request_id": request_id,
                "address": addr.lower(),
                "ens": ens,
                "world_coin_confirmed": is_world_coin,
                "lens_followers": lens_follower,
                "twitter_followers": twitter_follower,
                "is_human": likely_human,
                "is_compliant": compliant,
                "score": score,
                "chain_stats": chain_stats,
                "summary": generate_text(
                    score,
                    compliant,
                    likely_human,
                    current_usd_balance,
                    current_age,
                    current_nonce,
                    is_world_coin,
                    lens_follower,
                    twitter_follower,
                ),
                "non_compliant_txns": noncompliantTxns,
                "non_compliant_txn_list": non_compliant_txn_list,
                "twitter_account": twitter_account,
            }

        return scores

    def all_chain_balance(self, address):
        balances = {}
        for chain_id, cli in self.all_chain_client.items():
            balances[chain_id] = cli.usd_balance(address)
        return balances

    def all_chain_age(self, address):
        age = {}
        nonce = {}
        for chain_id, cli in self.all_chain_client.items():
            age[chain_id] = cli.address_age(address)
            nonce[chain_id] = cli.address_nonce(address)
        return age, nonce

    def ens_name(self, address):
        return self.ens_client.get_ens_detail(address)["name"]

    def lens_followers(self, address) -> (int, bool):
        res = self.lens_client.get_profiles([address])
        items = res["data"]["profiles"]["items"]
        if len(items) == 0:
            return 0, False
        return \
            res["data"]["profiles"]["items"][0]["stats"]["followers"], \
                res["data"]["profiles"]["items"][0]["onchainIdentity"]["worldcoin"]["isHuman"]

    def ipfs_upload(self, request_id, scores):
        return self.ipfs_client.save_data(request_id, scores)

    def get_latest_block_number(self):
        return self.client.w3.eth.block_number

    def batch_request_received(self, data: bytes):
        return self.decode_batch_request_received(data)

    @staticmethod
    def decode_batch_request_received(data: bytes):
        addresses, nonce = abi.decode(
            ["address[]", "uint256"], data
        )
        return addresses, nonce

    def request_received(self, data: bytes):
        return self.decode_request_received(data)

    @staticmethod
    def decode_request_received(data: bytes):
        address, nonce = abi.decode(
            ["address", "uint256"], data
        )
        return address, nonce

    def score_ipfs(self, addr):
        scores = self.calculate_score("", [addr])
        #
        # ipfs
        ipfs_hash = self.ipfs_upload("", scores)
        print(ipfs_hash)


if __name__ == '__main__':
    lis = Listener()
    lis.listen()

# 0xeB1c22baACAFac7836f20f684C946228401FF01C: https://cloudflare-ipfs.com/ipfs/QmcsVNJuNQYAh26ytARtHar84ALNxmNRD2bnSfp9AUSb7A
# 0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA: https://cloudflare-ipfs.com/ipfs/QmXJHigLsHiDVXv7U8G16nbtLBqP2nu1RViDEufUn7euCx
# 0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13: https://cloudflare-ipfs.com/ipfs/QmVNC8SEjpunQDpLaLeRhcBMpFMWBdcWrARoRPC6tgs5VM
