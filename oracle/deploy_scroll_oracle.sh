#!/bin/bash

export OOV3_ADDRESS=0xff00000000000000000000000000000000000997

export AXIOM_V2_QUERY_ADDRES=0xff00000000000000000000000000000000000997

forge create --rpc-url https://sepolia-rpc.scroll.io \
    --constructor-args ${OOV3_ADDRESS} ${AXIOM_V2_QUERY_ADDRES} false false\
    --verifier-url "https://sepolia.scrollscan.com/api?apikey=21B84GV7KNX1AC46DG75377TXP63K1ZU6G" \
    --verify \
    --legacy \
    --private-key ${DEPLOYER_PRIVATE_KEY} \
    src/RepOracle.sol:RepOracleContract
    