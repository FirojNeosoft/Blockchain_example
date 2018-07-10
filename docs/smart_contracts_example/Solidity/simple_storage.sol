pragma solidity ^0.4.0;

contract SimpleStorage {
    uint storedData;
    address issuer;

    constructor() public {
        issuer = msg.sender;
    }

    modifier onlyOwner() {
        require(
            msg.sender == issuer,
            "Only owner can call this."
        );
        _;
    }

    function set(uint x) public {
        storedData = x;
    }

    function get() public view onlyOwner returns (uint) {
        return storedData;
    }
    
}
