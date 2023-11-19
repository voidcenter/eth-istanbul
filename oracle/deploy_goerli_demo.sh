export ORACLE_ADDRESS=0x381A8063c73F32E7D3D493E0d617c94De96b09cb


forge create --rpc-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0 \
    --constructor-args ${ORACLE_ADDRESS}\
    --private-key $DEPLOYER_PRIVATE_KEY \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --verify \
    src/DemoOracleUser.sol:DemoRepOracleUser