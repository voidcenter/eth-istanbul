#!/bin/bash

export OOV3_ADDRESS=0xff00000000000000000000000000000000000997

export AXIOM_V2_QUERY_ADDRES=0xff00000000000000000000000000000000000997

forge create --rpc-url https://rpc.testnet.mantle.xyz/ \
    --constructor-args ${OOV3_ADDRESS} ${AXIOM_V2_QUERY_ADDRES} false false\
    --private-key ${DEPLOYER_PRIVATE_KEY} \
    --legacy \
    src/RepOracle.sol:RepOracleContract
    