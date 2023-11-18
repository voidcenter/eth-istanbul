#!/usr/bin/env python3
import os
import subprocess

# we should pass these in as arguments:   #   oracle address
#   laetst block 
#   address
#   address's first block


class Axiom:
    def __init__(self, oracle_address):
        self.path = os.path.join(os.path.dirname(__file__), "src/index.ts")
        self.oracle_address = str(oracle_address).lower()

    def call_axiom(self, from_block_number, to_block_number, request_address, request_id):
        cmd = f"npx ts-node {self.path} {to_block_number} {self.oracle_address} {str(request_address.lower())} {from_block_number} {request_id}"
        print(cmd)
        out = subprocess.check_output(cmd, shell=True)
        print(out)
        return out


if __name__ == '__main__':
    a = Axiom("0xfb7581e2bcff4c5c3a428123f36c73edc8fc4e4b")
    print(a.call_axiom(
        8242852,
        10060567,
        "0xeb1c22baacafac7836f20f684c946228401ff01c",
        "0xc4ef17ac016e59c02668d35ff0960db840cd97333c44ae0be691aeb2bc688862"
    ))
