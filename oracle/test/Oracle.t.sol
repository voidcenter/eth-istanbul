// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

// import {DSTest} from "ds-test/test.sol";
import {Test, console2} from "forge-std/Test.sol";
import {RepOracleContract, IRepOracleContract} from "../src/RepOracle.sol";
import {DemoRepOracleUser} from "../src/DemoOracleUser.sol";

contract OracleTest is Test {
    RepOracleContract public oracle;
    DemoRepOracleUser public user;
    address constant UMAOracle = 0x9923D42eF695B5dd9911D05Ac944d4cAca3c4EAB;
    address constant axiomv2query = 0xB871BabfcbEC25b049C4e65BD5f5d8B3FE3Cc6F5;

    function setUp() public {
        // testing on Goerli
        oracle = new RepOracleContract(UMAOracle, axiomv2query);
        user = new DemoRepOracleUser(address(oracle));
    }

    function test_SingleRequest() public {
        // Setup
        uint256 beginningNonce = oracle.requestNonce();
        address queryingAddress = address(1);

        bytes32 expectedRequestID =
            keccak256(abi.encodePacked(address(this), queryingAddress, block.timestamp, beginningNonce));

        // Checking if events are emitted
        vm.expectEmit(true, true, true, true);
        emit IRepOracleContract.RequestReceived(expectedRequestID, address(this), queryingAddress, beginningNonce);

        // Sending Request through user contrat
        bytes32 requestId = oracle.requestReputationScore(queryingAddress, true, 0);

        assertEq(oracle.requestNonce(), beginningNonce + 1);

        assertEq(oracle.call_back_address(expectedRequestID), address(this));

        // sending reputation score
        vm.expectEmit(true, false, false, true);
        emit IRepOracleContract.ReputationScoreSent(requestId, 99, 0);

        IRepOracleContract.RepScore memory exampleScore = IRepOracleContract.RepScore(
            queryingAddress, 99, block.number, true, false,
            IRepOracleContract.SocialDetail(false, 10, 100, 2, "justin.eth"),
            IRepOracleContract.OnchainDetails(1,2,3,4,5,6), 
            requestId,
            "QmQMvd3pSWxaoEVit5oui9xcJa4C5UqZLAcubuhawcN3F6"
        );
        bytes32 assertionId =
            oracle.sendReputationScore(exampleScore, "verify IPFS hash QmQMvd3pSWxaoEVit5oui9xcJa4C5UqZLAcubuhawcN3F6");

        
        // call back to axiom
        uint256 queryId = 1234;
        bytes32[] memory axiomResults = new bytes32[](3);
        axiomResults[0] = bytes32(uint256(1));
        axiomResults[1] = bytes32(0);
        axiomResults[2] = bytes32(uint256(4));
        
        vm.prank(axiomv2query);
        vm.expectEmit(true, true, true, true);
        emit RepOracleContract.AxiomVerificationSuccess(requestId, queryId);
        // these are data from https://explorer.phalcon.xyz/tx/goerli/0x400c41eb4e877d07ed821e05466f9b61f6db2d247fbd7e3cd3ef212bc5479594
        oracle.axiomV2Callback(5, address(this), bytes32(0), queryId, axiomResults, abi.encodePacked(requestId));

        // pretend to be UMA and send assert back
        vm.prank(UMAOracle);
        vm.expectEmit();
        emit RepOracleContract.UMAAssertionResolved(assertionId, requestId, true);
        oracle.assertionResolvedCallback(assertionId, true);
    }

    // function test_UserInteraction() public {
    //     // Setup
    //     uint256 beginningNonce = oracle.requestNonce();
    //     address queryingAddress = address(2);

    //     bytes32 expectedRequestID =
    //         keccak256(abi.encodePacked(address(user), queryingAddress, block.timestamp, beginningNonce));

    //     // Checking if events are emitted
    //     vm.expectEmit();

    //     emit IRepOracleContract.RequestReceived(expectedRequestID, address(user), queryingAddress, beginningNonce);

    //     vm.expectEmit();
    //     emit DemoRepOracleUser.RequestSent(expectedRequestID);

    //     // Sending Request through user contrat
    //     user.requestReputationScore(queryingAddress);

    //     assertEq(oracle.requestNonce(), beginningNonce + 1);

    //     assertEq(oracle.requests(expectedRequestID), address(user), "user address");

    //     // Test Callback
    //     uint256 _reputationScore = 100;
    //     vm.expectEmit();
    //     emit DemoRepOracleUser.ReputationScoreReceived(expectedRequestID, _reputationScore);

    //     vm.expectEmit();
    //     emit IRepOracleContract.ReputationScoreSent(expectedRequestID, _reputationScore);

    //     oracle.sendReputationScore(expectedRequestID, _reputationScore, "hash to IPFS");

    //     assertEq(
    //         oracle.requests(expectedRequestID), address(user), "request is still ongoing, needs commit or rollback"
    //     );

    //     assertEq(user.pendingRequests(expectedRequestID), false);
    // }

    // function test_AccessControl() public {
    //     address queryingAddress = address(1);
    //     bytes32 requestId = oracle.requestReputationScore(queryingAddress, true, 0);

    //     IRepOracleContract.RepScore memory emptyScore = IRepOracleContract.RepScore(
    //         0, 0, false, false, IRepOracleContract.RepDetail(0, 0, 0, false, 0, 0, 0), requestId
    //     );

    //     // Non oracle owner should not have access
    //     vm.startPrank(address(5050));
    //     vm.expectRevert();
    //     oracle.sendReputationScore(emptyScore, "hash to IPFS");
    //     vm.stopPrank();

    //     // Oracle owner should have acccess
    //     oracle.sendReputationScore(emptyScore, "hash to IPFS");
    // }

    // Dummy callback for testing, pretending this address is a oracle user
    function reputationCallback(IRepOracleContract.RepScore calldata _score) external {}
    function commit(bytes32 _requestId) external {}
}
