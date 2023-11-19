DEMO_USER=0x156ec9aac062e48aedaec5b4e4be33a7f354286b
DEMO_ORACLE=0xfb7581e2bcff4c5c3a428123f36c73edc8fc4e4b

dry0:
	@cast call ${DEMO_USER} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"requestReputationScore(address,bool,uint256)()" 0xeB1c22baACAFac7836f20f684C946228401FF01C true 0

run0:
	@cast send ${DEMO_USER} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"requestReputationScore(address,bool,uint256)()" 0xeB1c22baACAFac7836f20f684C946228401FF01C true 0

# Send reputation
dry1:
	@cast call ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"sendReputationScore((address,uint256,uint256,bool,bool,(bool,uint256,uint256,uint256,bytes),(uint256,uint256,uint256,uint256,uint256,uint256),bytes32,bytes),bytes)(bytes32)" \
		"(0xeB1c22baACAFac7836f20f684C946228401FF01C,0,1,true,false,(true,1,2,3,0x12345678),(1,2,3,4,5,6),0xd2618b1146e106e16185f60d85c4af8e5380d6f22f79569db357fe281bb04bb8,0x12345678)" 0x123456

run1:
	@cast send ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"sendReputationScore((address,uint256,uint256,bool,bool,(bool,uint256,uint256,uint256,bytes),(uint256,uint256,uint256,uint256,uint256,uint256),bytes32,bytes),bytes)(bytes32)" \
		"(0xeB1c22baACAFac7836f20f684C946228401FF01C,0,1,true,false,(true,1,2,3,0x12345678),(1,2,3,4,5,6),0xd2618b1146e106e16185f60d85c4af8e5380d6f22f79569db357fe281bb04bb8,0x12345678)" 0x123456
## Axiom

## call UMA
dry2:
	@cast call ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"settelUMAAssertion(bytes32)()" 0xe3aefd5329040ef46ae888bbceccba8cfba5c07c0cf6bfa0d39738b9f38aa284 # change THIS assetionID

run2:
	@cast send ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"settelUMAAssertion(bytes32)()" 0xe3aefd5329040ef46ae888bbceccba8cfba5c07c0cf6bfa0d39738b9f38aa284 # change THIS assetionID