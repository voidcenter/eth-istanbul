#!/bin/bash

export OOV3_ADDRESS=0xff00000000000000000000000000000000000997

export AXIOM_V2_QUERY_ADDRES=0xff00000000000000000000000000000000000997

forge create --rpc-url https://rpc.gnosis.gateway.fm \
    --constructor-args ${OOV3_ADDRESS} ${AXIOM_V2_QUERY_ADDRES} false false\
    --verifier-url "https://api.gnosisscan.io/api/?apikey=9A6AYZ1729TMY4C45NCIZ4R2MWAI5XQCRW" \
    --verify \
    --private-key ${DEPLOYER_PRIVATE_KEY} \
    src/RepOracle.sol:RepOracleContract
    