// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./interface/IRepOracleUser.sol";
import "./interface/IRepOracle.sol";
import "./interface/IUMAOracleV3.sol";

contract RepOracleContract is IRepOracleContract, Ownable {
    mapping(bytes32 => address) public requests; // request id to user address
    mapping(bytes32 => bytes32) public assertion_ids; //  assertion_ids to request_id
    mapping(bytes32 => bytes) public evidence; // request id to evidence (IPFS hash), remove in production

    mapping(address => IRepOracleContract.RepScore) public repScore;

    uint256 public requestNonce;
    IUMAOracleV3 oov3;
    uint64 public constant assertionLiveness = 120;
    bytes32 public immutable defaultIdentifier;
    IERC20 public immutable defaultCurrency;

    constructor(address umaOracle) Ownable(msg.sender) {
        // Create an Optimistic Oracle V3 instance at the deployed address on Görli.
        oov3 = IUMAOracleV3(umaOracle);
        defaultIdentifier = oov3.defaultIdentifier();
        defaultCurrency = IERC20(oov3.defaultCurrency());
        requestNonce = 0;
    }

    function requestBatchReputationScore(address[] calldata _addresses) external returns (bytes32) {
        bytes32 requestId = keccak256(abi.encodePacked(msg.sender, _addresses, block.timestamp, requestNonce));
        requests[requestId] = msg.sender;
        emit BatchRequestReceived(requestId, msg.sender, _addresses, requestNonce);
        requestNonce += 1;
        return requestId;
    }

    function requestReputationScore(address _address, bool forceRefresh, uint256 expirationBlock)
        external
        returns (bytes32)
    {
        // Three possible way to get fresh score
        // Forced Refresh
        // First time calculating the score
        // The score expired
        bytes32 requestId = keccak256(abi.encodePacked(msg.sender, _address, block.timestamp, requestNonce));
        requests[requestId] = msg.sender;

        if (forceRefresh || repScore[_address].blocknumber == 0 || repScore[_address].blocknumber <= expirationBlock) {
            emit RequestReceived(requestId, msg.sender, _address, requestNonce);
            requestNonce += 1;
        } else {
            // directly callback
            emit CachedRequestReceived(requestId, msg.sender, _address, requestNonce);
            requestNonce += 1;
            IRepOracleUser(msg.sender).reputationCallback(repScore[_address]);
        }
        return requestId;
    }

    function sendReputationScore(IRepOracleContract.RepScore calldata score, bytes memory _evidence)
        external
        onlyOwner
        returns (bytes32 assertionId)
    {
        address userContractAddress = requests[score.requestId];
        require(userContractAddress != address(0), "Request ID not found");

        uint256 bond = oov3.getMinimumBond(address(defaultCurrency));
        defaultCurrency.transferFrom(msg.sender, address(this), bond);
        defaultCurrency.approve(address(oov3), bond);

        assertionId = oov3.assertTruth(
            _evidence,
            owner(), // asserter, recieve the bond back at resolution if correct
            address(this),
            address(0), // no sovereign security
            assertionLiveness,
            defaultCurrency,
            bond,
            defaultIdentifier,
            bytes32(0) // No domain.
        );
        assertion_ids[assertionId] = score.requestId;

        IRepOracleUser(userContractAddress).reputationCallback(score);

        evidence[score.requestId] = _evidence;
        repScore[userContractAddress] = score;
        emit ReputationScoreSent(score.requestId, score.score, assertionId);
    }

    event UMAAssertionResolved(bytes32 indexed assertionId, bytes32 indexed requestId, bool _status);

    // OptimisticOracleV3 resolve callback.
    function assertionResolvedCallback(bytes32 assertionId, bool assertedTruthfully) public {
        require(msg.sender == address(oov3));
        bytes32 _requestId = assertion_ids[assertionId];
        address userContractAddress = requests[_requestId];
        require(userContractAddress != address(0), "Request ID not found");

        // If the assertion was true, then the data assertion is resolved.
        if (assertedTruthfully) {
            IRepOracleUser(userContractAddress).commit(_requestId);
            emit UMAAssertionResolved(assertionId, _requestId, true);
            // Else delete the data assertion if it was false to save gas.
            // Enter reimbursement mechanism for users to get money.
        } else {
            IRepOracleUser(userContractAddress).rollback(_requestId);
            emit UMAAssertionResolved(assertionId, _requestId, false);
        }

        // Gas savings
        // delete assertion_ids[assertionId];
        // delete requests[_requestId];
    }

    // Call this once liveness period is over
    function settelUMAAssertion(bytes32 assertionId) public {
        bool assertionResult = oov3.settleAndGetAssertionResult(assertionId);
    }
}
