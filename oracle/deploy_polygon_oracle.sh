#!/bin/bash

export OOV3_ADDRESS=0xff00000000000000000000000000000000000997

export AXIOM_V2_QUERY_ADDRES=0xff00000000000000000000000000000000000997

forge create --rpc-url https://rpc.public.zkevm-test.net \
    --constructor-args ${OOV3_ADDRESS} ${AXIOM_V2_QUERY_ADDRES} false false\
    --verifier-url "https://api-testnet-zkevm.polygonscan.com/api?apikey=E2ZQPAZRNW5A47G4899I6BS2W7T8MYCZ7E" \
    --verify \
    --private-key ${DEPLOYER_PRIVATE_KEY} \
    src/RepOracle.sol:RepOracleContract
    