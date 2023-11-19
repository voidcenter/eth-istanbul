DEMO_USER=0x501efC741A68C6faa0FbD020e4DB9DB946C4018F
DEMO_ORACLE=0x381A8063c73F32E7D3D493E0d617c94De96b09cb

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
		"sendReputationScore((address,int256,uint256,bool,bool,(bool,uint256,uint256,uint256,bytes),(uint256,uint256,uint256,uint256,uint256,uint256),bytes32,bytes),bytes)(bytes32)" \
		"(0xeB1c22baACAFac7836f20f684C946228401FF01C,0,1,true,false,(true,1,2,3,0x12345678),(1,2,3,4,5,6),0x9686b88521763f9bbb030df09428b3d8de4752ca0dcf1c9b51c99cd2378bccfa,0x12345678)" 0x123456

run1:
	@cast send ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"sendReputationScore((address,int256,uint256,bool,bool,(bool,uint256,uint256,uint256,bytes),(uint256,uint256,uint256,uint256,uint256,uint256),bytes32,bytes),bytes)(bytes32)" \
		"(0xeB1c22baACAFac7836f20f684C946228401FF01C,0,1,true,false,(true,1,2,3,0x12345678),(1,2,3,4,5,6),0x9686b88521763f9bbb030df09428b3d8de4752ca0dcf1c9b51c99cd2378bccfa,0x12345678)" 0x123456
## Axiom

## call UMA
dry2:
	@cast call ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"settelUMAAssertion(bytes32)()" 0x2cb2580614f4b506e1000828ace0f150f3bf9f6d8f9016ed85e1f2e3833062d4 # change THIS assetionID

run2:
	@cast send ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://eth-goerli.g.alchemy.com/v2/IbSfio5zI-0O2qB-nRCz0AvTN9xwndm2 \
		"settelUMAAssertion(bytes32)()" 0x2cb2580614f4b506e1000828ace0f150f3bf9f6d8f9016ed85e1f2e3833062d4 # change THIS assetionID
