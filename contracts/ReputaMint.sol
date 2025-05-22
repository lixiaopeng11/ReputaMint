// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IGraphiteReputation {
    function getTrustScore(address user) external view returns (uint256);
}

contract ReputaMint {
    address public owner;
    IGraphiteReputation public reputationContract;
    uint256 public requiredScore = 70;

    mapping(address => bool) public hasMinted;

    event Minted(address indexed user);

    constructor(address _repContract) {
        owner = msg.sender;
        reputationContract = IGraphiteReputation(_repContract);
    }

    function mint() public {
        require(!hasMinted[msg.sender], "Already minted");
        uint256 score = reputationContract.getTrustScore(msg.sender);
        require(score >= requiredScore, "Trust score too low");

        hasMinted[msg.sender] = true;
        emit Minted(msg.sender);
        // Token logic placeholder
    }

    function setRequiredScore(uint256 score) public {
        require(msg.sender == owner, "Only owner");
        requiredScore = score;
    }
}