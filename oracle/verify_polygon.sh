#!/bin/bash
export CONSTARG1=$(cast abi-encode "constructor(address,address,bool,bool)" 0xff00000000000000000000000000000000000997 0xff00000000000000000000000000000000000997 false false)
export CONSTARG2=$(cast abi-encode "constructor(address)" 0xfA89863E6B51694ccc0bDFe641E00F0355c2fb6c)

# forge verify-contract --constructor-args ${CONSTARG1} --show-standard-json-input 0xfa89863e6b51694ccc0bdfe641e00f0355c2fb6c src/RepOracle.sol:RepOracleContract

forge verify-contract --constructor-args ${CONSTARG2} --show-standard-json-input 0x51dec4Eb917c138575C508ccB9a267c2eDE83784 src/DemoOracleUser.sol:DemoRepOracleUser