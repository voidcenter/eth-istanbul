#!/bin/bash
export CONSTARG=$(cast abi-encode "constructor(address,address,bool,bool)" 0xff00000000000000000000000000000000000997 0xff00000000000000000000000000000000000997 false false)

forge verify-contract --verifier-url "https://api.gnosisscan.io/api/?apikey=9A6AYZ1729TMY4C45NCIZ4R2MWAI5XQCRW" --constructor-args ${CONSTARG} --watch 0x51dec4eb917c138575c508ccb9a267c2ede83784 src/RepOracle.sol:RepOracleContract