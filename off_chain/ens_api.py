from ens import ENS
from web3 import Web3
class ENSAPI:

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/_k459_5wqx-_anLhMSPJPfddLM8qU_LM'))
        self.ns = ENS.from_web3(self.w3)

    def get_ens_detail(self, address: str):
        _name = self.ns.name(address)
        if _name != None:
            _owner = self.ns.owner(_name)
            _resolver = self.ns.resolver(_name)
            _resolver_address = _resolver.address
            # find initial addr change:
            _addr_change_logs = self.get_latest_address_change(_resolver.address, _name)

        else:
            _name = ""
            _owner = None
            _resolver_address = None
            _addr_change_logs = None

        return {
            'name' : _name,
            'owner': _owner,
            'resolver': _resolver_address,
            'logs': _addr_change_logs
        }

    def get_address_by_ens(self, ens_name: str):
        eth_address = self.ns.address(ens_name)

        return eth_address

    def get_latest_address_change(self, resolver_address: str, name: str):
        # Define the ENS contract address and event signature
        contract_address = Web3.to_checksum_address(resolver_address)  # Replace with the ENS contract address
        # https://etherscan.io/tx/0xf6b39af1966074e9b1349b1d8c2fe8b18bff0339e03b44f0aa72e9e147e24e36#eventlog
        event_signature_hash = "0x52d7d861f09ab3d26239d492e8968629f95e9e318cf0b73bfddc441522a15fd2" # AddrChanged

        node = self.get_name_hash(name)
        topic1 = node

        # Set up the filter parameters
        filter_params = {
            "fromBlock": "earliest",
            "toBlock": "latest",
            "address": contract_address,
            "topics": [event_signature_hash, topic1]
        }

        logs = self.w3.eth.get_logs(filter_params)

        return logs

    def get_name_hash(self, name):
        return self.ns.namehash(name).hex()


if __name__ == '__main__':
    api = ENSAPI()

    result = api.get_ens_detail("0xeB1c22baACAFac7836f20f684C946228401FF01C")
    #
    # print(result)
    #
    #
    # result = api.get_address_by_ens("ens.eth")
    #
    # print(result)

    # result = api.get_latest_address_change("get_latest_address_change")

    # result = api.convert_name_to_bytes32("neoterica.eth")

    print(result)
