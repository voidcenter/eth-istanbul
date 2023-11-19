#!/bin/bash

export OOV3_ADDRESS=0xff00000000000000000000000000000000000997

export AXIOM_V2_QUERY_ADDRES=0xff00000000000000000000000000000000000997

forge create --rpc-url https://rpc.goerli.linea.build \
    --constructor-args ${OOV3_ADDRESS} ${AXIOM_V2_QUERY_ADDRES} false false\
    --verifier-url "https://api.lineascan.build/api?apikey=AHHK9JUICCBSCAXG5EXR9TT2N8HSQ95FT1" \
    --verify \
    --private-key ${DEPLOYER_PRIVATE_KEY} \
    src/RepOracle.sol:RepOracleContract
    