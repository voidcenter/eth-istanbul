export ORACLE_ADDRESS=0x39a62Cd6B9d956D48c42B73D89a6319E3f3440cF

forge create --rpc-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0 \
    --constructor-args ${ORACLE_ADDRESS} \
    --private-key $DEPLOYER_PRIVATE_KEY \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --verify \
    src/DemoOracleUser.sol:DemoRepOracleUser
