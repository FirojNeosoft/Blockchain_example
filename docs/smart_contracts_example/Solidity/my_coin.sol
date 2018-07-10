pragma solidity ^0.4.0;

contract MyCoin {
address public owner;
uint public totalCoins;

event LogCoinsMinted(address deliveredTo, uint amount);
event LogCoinsSent(address sentTo, uint amount);

mapping (address => uint) balances;

constructor(uint initialCoins) public {
owner = msg.sender;
totalCoins = initialCoins;
balances[owner] = initialCoins;
}

function mint(address coinowner, uint amount) public {
if (msg.sender != owner) return;
balances[coinowner] += amount;
totalCoins += amount;
emit LogCoinsMinted(coinowner, amount);
}

function send(address receiver, uint amount) public {
if (balances[msg.sender] < amount) return;
balances[msg.sender] -= amount;
balances[receiver] += amount;
emit LogCoinsSent(receiver, amount);
}

function queryBalance(address addr) public constant returns (uint balance) {
return balances[addr];
}

}



