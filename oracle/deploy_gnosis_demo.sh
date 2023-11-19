export ORACLE_ADDRESS=0x51dec4Eb917c138575C508ccB9a267c2eDE83784

forge create --rpc-url https://rpc.gnosis.gateway.fm \
    --constructor-args ${ORACLE_ADDRESS} \
    --private-key $DEPLOYER_PRIVATE_KEY \
    --verifier-url "https://api.gnosisscan.io/api/?apikey=9A6AYZ1729TMY4C45NCIZ4R2MWAI5XQCRW" \
    --verify \
    src/DemoOracleUser.sol:DemoRepOracleUser