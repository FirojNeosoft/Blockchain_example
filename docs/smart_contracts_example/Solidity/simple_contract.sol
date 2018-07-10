pragma solidity ^0.4.0;

contract SimpleContract {
    uint storedData;
    address issuer;

    event updatedStatus(string msg, address user, uint amt);


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
    
    function getBalance() public constant onlyOwner returns (uint) {
        return address(this).balance;
    }
    
    function deposit() public payable{
        emit updatedStatus("RECEIVE", msg.sender, msg.value);
    }
    
    function withdraw(uint amount) public onlyOwner{
        if(issuer.send(amount)){
           emit updatedStatus("SEND", issuer, amount);
        }
    }
    
}
