export ORACLE_ADDRESS=0xFb7581e2bCFF4C5C3A428123f36c73eDC8fc4e4B


forge create --rpc-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0 \
    --constructor-args ${ORACLE_ADDRESS}\
    --private-key $DEPLOYER_PRIVATE_KEY \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --verify \
    src/DemoOracleUser.sol:DemoRepOracleUser
