// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interface/IRepOracleUser.sol";

contract DemoRepOracleUser is Ownable, RepOracleUser {
    mapping(bytes32 => bool) public pendingRequests;
    mapping(bytes32 => bool) public proofingRequests;

    event RequestSent(bytes32 indexed requestId);
    event ReputationScoreReceived(bytes32 indexed requestId, IRepOracleContract.RepScore score);
    event ReputationScoreCommitted(bytes32 indexed requestId);
    event ReputationScoreRolledback(bytes32 indexed requestId);

    constructor(address _oracleAddress) RepOracleUser(_oracleAddress) Ownable(msg.sender) {}

    function requestReputationScore(address _address, bool _forceRefresh, uint256 _expirationBlock)
        external
        onlyOwner
    {
        bytes32 requestId = oracle.requestReputationScore(_address, _forceRefresh, _expirationBlock);
        pendingRequests[requestId] = true;
        emit RequestSent(requestId);
    }

    // this function will get callbacked immediately a reputation score is computed, however, at this point
    // the score is yet to be verified.
    function reputationCallback(IRepOracleContract.RepScore memory score) external override onlyRepOracle {
        require(msg.sender == address(oracle), "Only oracle can call this function");
        require(pendingRequests[score.requestId], "Request ID not found");

        emit ReputationScoreReceived(score.requestId, score);
        delete pendingRequests[score.requestId];
        proofingRequests[score.requestId] = true;
    }

    // when this function is called, the requested score is verified
    function commit(bytes32 _requestId) external override onlyRepOracle {
        emit ReputationScoreCommitted(_requestId);
        delete proofingRequests[_requestId];
    }

    // when this function is called, the score verification failed, rollback anything if needed
    // this is function will never be called if requested has already been committed.
    function rollback(bytes32 _requestId) external override onlyRepOracle {
        emit ReputationScoreRolledback(_requestId);
        delete proofingRequests[_requestId];
    }
}
