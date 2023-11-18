
----------- TEST LOCALLY ON GOERLI FORK SETUP
anvil --fork-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0

export MNEMONIC="test test test test test test test test test test test junk"

export FINDER_ADDRESS=0xE60dBa66B85E10E7Fd18a67a6859E241A243950e

export OOV3_ADDRESS=$(cast call $FINDER_ADDRESS "getImplementationAddress(bytes32)(address)" \
	$(cast --format-bytes32-string "OptimisticOracleV3"))

--------------- DEPLOY CONTRACT

export REP_ORACLE=$(forge create --json src/RepOracle.sol:RepOracleContract \
	--mnemonic "$MNEMONIC" \
	--constructor-args $OOV3_ADDRESS \
	| jq -r .deployedTo)

------------- VERIFYING CONTRACT
forge verify-contract \
	--chain-id $(cast chain-id) \
	--constructor-args $(cast abi-encode "constructor(address)" \
	$OOV3_ADDRESS) $REP_ORACLE RepOracle


----- TESTING DEPLOYED CONTRACT 
export ASSERTER_ID=1

export DATA=$(cast --format-bytes32-string $(echo '69+420' | bc))
echo "DATA=$(echo $DATA)"


export ASSERTION_TX=$(cast send --json \
	--mnemonic "$MNEMONIC" --mnemonic-index $ASSERTER_ID \
	$DATA_ASSERTER \
	"sendReputationScore(bytes32,uint256, bytes)" $DATA_ID $DATA $DATA_ASSERTER \
	| jq -r .transactionHash)


export ASSERTION_TX=$(cast send --json \
	--mnemonic "$MNEMONIC" --mnemonic-index $ASSERTER_ID \
	$DATA_ASSERTER \
	"sendReputationScore(bytes32,uint256, bytes)" $DATA_ID $DATA $DATA_ASSERTER \
	| jq -r .transactionHash)

-------------- DEPLOY TO GOERLI
forge create --rpc-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0 \
    --constructor-args $OOV3_ADDRESS \
    --private-key $DEPLOYER_PRIVATE_KEY \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --verify \
    src/RepOracle.sol:RepOracleContract

-------------- DEPLOY DEMO USER
forge create --rpc-url https://eth-goerli.g.alchemy.com/v2/Dy3YnnKVgx3i6DM6WGPlY8kz5W8QpKb0 \
    --constructor-args 0xA7983eE84414D84027AB36b4c3113caaA4Ad505c \
    --private-key $DEPLOYER_PRIVATE_KEY \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --verify \
    src/DemoOracleUser.sol:DemoRepOracleUser
