DEMO_USER=0x4CdEcc2C9f569F52f9B3d9B00cbDE4A323A0B911
DEMO_ORACLE=0x93838Ac1D8f469Ef466D50cA8Aa294ACe94dD612

dry0:
	@cast call ${DEMO_USER} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://rpc.gnosis.gateway.fm \
		"requestReputationScore(address,bool,uint256)()" 0xeB1c22baACAFac7836f20f684C946228401FF01C true 0

run0:
	@cast send ${DEMO_USER} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://rpc.gnosis.gateway.fm \
		"requestReputationScore(address,bool,uint256)()" 0xeB1c22baACAFac7836f20f684C946228401FF01C true 0

# Send reputation 
dry1:
	@cast call ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://rpc.gnosis.gateway.fm \
		"sendReputationScore((address,int256,uint256,bool,bool,(bool,uint256,uint256,uint256,bytes),(uint256,uint256,uint256,uint256,uint256,uint256),bytes32,bytes),bytes)(bytes32)" \
		"(0xeB1c22baACAFac7836f20f684C946228401FF01C,0,1,true,false,(true,1,2,3,0x12345678),(1,2,3,4,5,6),0x935449c94fc3dbb88f9145665969e49ab22ece701fc3f9d5731f45bb7a0254de,0x12345678)" 0x123456

run1:
	@cast send ${DEMO_ORACLE} --private-key ${DEPLOYER_PRIVATE_KEY} \
		--rpc-url https://rpc.gnosis.gateway.fm \
		"sendReputationScore((address,int256,uint256,bool,bool,(bool,uint256,uint256,uint256,bytes),(uint256,uint256,uint256,uint256,uint256,uint256),bytes32,bytes),bytes)(bytes32)" \
		"(0xeB1c22baACAFac7836f20f684C946228401FF01C,0,1,true,false,(true,1,2,3,0x12345678),(1,2,3,4,5,6),0x935449c94fc3dbb88f9145665969e49ab22ece701fc3f9d5731f45bb7a0254de,0x12345678)" 0x123456