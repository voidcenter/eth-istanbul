#!/bin/bash
export FINDER_ADDRESS=0xE60dBa66B85E10E7Fd18a67a6859E241A243950e

export OOV3_ADDRESS=$(cast call --rpc-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0 ${FINDER_ADDRESS} "getImplementationAddress(bytes32)(address)" \
	$(cast --format-bytes32-string "OptimisticOracleV3"))

export AXIOM_V2_QUERY_ADDRES=0xf15cc7B983749686Cd1eCca656C3D3E46407DC1f

forge create --rpc-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0 \
    --constructor-args ${OOV3_ADDRESS} ${AXIOM_V2_QUERY_ADDRES}\
    --private-key ${DEPLOYER_PRIVATE_KEY} \
    --etherscan-api-key ${ETHERSCAN_API_KEY} \
    --verify \
    src/RepOracle.sol:RepOracleContract