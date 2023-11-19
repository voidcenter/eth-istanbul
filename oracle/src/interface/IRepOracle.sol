// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IRepOracleContract {

    struct OnchainDetails {

        uint256 allChainMaxNounce;
        uint256 nonce;
        uint256 allChainMaxAge;
        uint256 age;
        uint256 allChainUsdBalance;
        uint256 usdBalance;
    }

    struct SocialDetail {
        bool worldcoinConfirmed;
        uint256 lensFollowers;
        uint256 twitterFollowers;
        uint256 noncompliantTxns;
        bytes ens;
    }

    struct RepScore {
        address requestingAddress;
        int256 score;
        uint256 blocknumber;
        bool isCompliant; // multi-chain
        bool isHuman;
        SocialDetail socialDetail;
        OnchainDetails onchainDetail;
        bytes32 requestId;
        bytes ipfs_hash;
    }

    event BatchRequestReceived(
        bytes32 indexed requestId, address indexed requester, address[] addresses, uint256 nonce
    );
    event RequestReceived(bytes32 indexed requestId, address indexed requester, address addresses, uint256 nonce);

    event CachedRequestReceived(bytes32 indexed requestId, address indexed requester, address addresses, uint256 nonce);

    event ReputationScoreSent(bytes32 indexed requestId, int256 reputationScore, bytes32 indexed assertionId);

    // function requestBatchReputationScore(address[] calldata _addresses) external returns (bytes32);

    function requestReputationScore(address _address, bool forceRefresh, uint256 expirationBlock)
        external
        returns (bytes32);

    function sendReputationScore(IRepOracleContract.RepScore calldata score, bytes memory _evidence)
        external
        returns (bytes32 assertionId);

    function settelUMAAssertion(bytes32 assertionId) external;
}
