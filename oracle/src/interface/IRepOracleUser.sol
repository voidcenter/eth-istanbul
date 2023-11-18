// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IRepOracle.sol";

interface IRepOracleUser {
    function reputationCallback(IRepOracleContract.RepScore memory score) external;

    function commit(bytes32 _requestId) external;

    function rollback(bytes32 _requestId) external;
}

abstract contract RepOracleUser is IRepOracleUser {
    address reputationOracle;
    IRepOracleContract oracle;

    modifier onlyRepOracle() {
        require(msg.sender == reputationOracle);
        _;
    }

    constructor(address _reputationOracle) {
        reputationOracle = _reputationOracle;
        oracle = IRepOracleContract(_reputationOracle);
    }
    // this function will get callbacked immediately a reputation score is computed, however, at this point
    // the score is yet to be verified.

    function reputationCallback(IRepOracleContract.RepScore memory score) external virtual;

    // when this function is called, the requested score is verified
    function commit(bytes32 _requestId) external virtual;

    // when this function is called, the score verification failed, rollback anything if needed
    // this is function will never be called if requested has already been committed.
    function rollback(bytes32 _requestId) external virtual;
}
