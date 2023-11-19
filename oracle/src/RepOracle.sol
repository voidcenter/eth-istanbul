// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./interface/IRepOracleUser.sol";
import "./interface/IRepOracle.sol";
import "./interface/IUMAOracleV3.sol";

contract RepOracleContract is IRepOracleContract, Ownable {
    // user call back
    mapping(bytes32 => address) public call_back_address; // request id to user address
    mapping(bytes32 => address) public requesting_address;
    // UMA 
    mapping(bytes32 => bytes32) public assertion_ids; //  assertion_ids to request_id
    // Evidence & score
    mapping(bytes32 => bytes) public evidence; // request id to evidence (IPFS hash), remove in production
    mapping(address => IRepOracleContract.RepScore) public repScore;
    
    // axiom proof
    mapping(bytes32 => uint256) public requestId_to_axiom_query_id;
    mapping(uint256 => bytes32) public axiom_query_id_to_requestId;


    uint256 public requestNonce;
    IUMAOracleV3 oov3;
    uint64 public assertionLiveness = 10;
    bytes32 public immutable defaultIdentifier;
    IERC20 public immutable defaultCurrency;
    address public axiomV2Query;

    // toggles for UMA & axiom
    bool public enable_uma;
    bool public enable_axiom;

    constructor(address umaOracle, address _axiomV2Query, bool _uma, bool _axiom) Ownable(msg.sender) {
        // Create an Optimistic Oracle V3 instance at the deployed address on Görli.
        toggleProviders(_uma, _axiom);

        if (enable_axiom) {
            axiomV2Query = _axiomV2Query;
        }

        if (enable_uma) {
            oov3 = IUMAOracleV3(umaOracle);
            defaultIdentifier = oov3.defaultIdentifier();
            defaultCurrency = IERC20(oov3.defaultCurrency());
        }
        requestNonce = 0;
    }

    function setAxiom(address _axiomV2Query) public onlyOwner {
        axiomV2Query = _axiomV2Query;
    }

    function toggleProviders(bool _uma, bool _axiom) public onlyOwner {
        enable_uma = _uma;
        enable_axiom = _axiom;
    }

    function setAssertionLiveness(uint64 _liveness) public onlyOwner {
        assertionLiveness = _liveness;
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
        requesting_address[requestId] = _address;
        call_back_address[requestId] = msg.sender;

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
        address userContractAddress = call_back_address[score.requestId];
        require(userContractAddress != address(0), "Request ID not found");

        if (enable_uma){
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
        } else {
            assertionId = bytes32(0);
        }


        IRepOracleUser(userContractAddress).reputationCallback(score);

        evidence[score.requestId] = _evidence;
        repScore[score.requestingAddress] = score;
        emit ReputationScoreSent(score.requestId, score.score, assertionId);

        if (!enable_uma) {
            IRepOracleUser(userContractAddress).commit(score.requestId);
            emit UMAAssertionResolved(assertionId, score.requestId, true);
        }
    }

    event UMAAssertionResolved(bytes32 indexed assertionId, bytes32 indexed requestId, bool _status);

    // OptimisticOracleV3 resolve callback.
    function assertionResolvedCallback(bytes32 assertionId, bool assertedTruthfully) public {
        require(msg.sender == address(oov3));
        bytes32 _requestId = assertion_ids[assertionId];
        address userContractAddress = call_back_address[_requestId];
        require(userContractAddress != address(0), "Request ID not found");

        // If the assertion was true, then the data assertion is resolved.
        // require Axiom proof to also pass
        bool axiomPassed = !enable_axiom || (requestId_to_axiom_query_id[_requestId] != 0);
        if (assertedTruthfully && axiomPassed) {
            IRepOracleUser(userContractAddress).commit(_requestId);

            emit UMAAssertionResolved(assertionId, _requestId, true);
            // Else delete the data assertion if it was false to save gas.
            // Enter reimbursement mechanism for users to get money.
        } else {
            IRepOracleUser(userContractAddress).rollback(_requestId);
            // the score is invalid, remove
            delete repScore[requesting_address[_requestId]];
            emit UMAAssertionResolved(assertionId, _requestId, false);
        }

        // Gas savings
        // delete assertion_ids[assertionId];
        // delete call_back_address[_requestId];
    }

    event AxiomVerificationSuccess(bytes32 indexed requestId, uint256 queryId);

    function axiomV2Callback(
        uint64 sourceChainId,
        address caller,
        bytes32 querySchema,
        uint256 queryId,
        bytes32[] calldata axiomResults,
        bytes calldata extraData // <-- we can requestId from this
    ) external { 
        // validate msg.sender against the AxiomV2Query address
        require(msg.sender == axiomV2Query || msg.sender == owner());
        require(caller == owner());     
        bytes32 requestId = bytes32(extraData);
        address userContractAddress = call_back_address[requestId];
        // validate the sourceChainId, caller, querySchema, and queryId
        
        IRepOracleContract.RepScore memory _unverifiedScore = repScore[requesting_address[requestId]];

        // verify axiom result
        emit AxiomVerificationSuccess(requestId, queryId);

        // perform your application logic
        requestId_to_axiom_query_id[requestId]= queryId;
        axiom_query_id_to_requestId[queryId] = requestId;

    }

    // Call this once liveness period is over
    function settelUMAAssertion(bytes32 assertionId) public {
        bool assertionResult = oov3.settleAndGetAssertionResult(assertionId);
    }
}
