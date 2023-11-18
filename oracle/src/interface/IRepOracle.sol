// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IRepOracleContract {
    struct RepDetail {
        uint256 usdBalance;
        uint256 age;
        uint256 transactionCount;
        bool worldcoinProved;
        uint256 lensConnections;
        uint256 twitterFollowers;
        uint256 noncompliantTxns;
    }

    struct RepScore {
        uint256 score;
        uint256 blocknumber;
        bool isCompliant; // multi-chain
        bool isHuman;
        RepDetail detail;
        bytes32 requestId;
    }

    event BatchRequestReceived(
        bytes32 indexed requestId, address indexed requester, address[] addresses, uint256 nonce
    );
    event RequestReceived(bytes32 indexed requestId, address indexed requester, address addresses, uint256 nonce);

    event CachedRequestReceived(bytes32 indexed requestId, address indexed requester, address addresses, uint256 nonce);

    event ReputationScoreSent(bytes32 indexed requestId, uint256 reputationScore, bytes32 indexed assertionId);

    function requestBatchReputationScore(address[] calldata _addresses) external returns (bytes32);

    function requestReputationScore(address _address, bool forceRefresh, uint256 expirationBlock)
        external
        returns (bytes32);

    function sendReputationScore(IRepOracleContract.RepScore calldata score, bytes memory _evidence)
        external
        returns (bytes32 assertionId);

    function settelUMAAssertion(bytes32 assertionId) external;
}
