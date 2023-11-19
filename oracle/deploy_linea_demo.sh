export ORACLE_ADDRESS=0xfA89863E6B51694ccc0bDFe641E00F0355c2fb6c

forge create --rpc-url https://rpc.goerli.linea.build \
    --constructor-args ${ORACLE_ADDRESS} \
    --private-key $DEPLOYER_PRIVATE_KEY \
    --legacy \
    src/DemoOracleUser.sol:DemoRepOracleUser