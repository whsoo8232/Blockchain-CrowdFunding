// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CrowdFunding is ReentrancyGuard, Ownable {
    IERC20 public token;
    address public tokenOwner;
    uint public RATE;

    // token contract distribute
    address public _token = 0xBafBe8Dc6b88868A7b58F6E5df89c3054dec93bB;
    address public _tokenOwner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    // token num per ETH rate
    uint public rate = 100000;

    event BuyToken(address user, uint amount, uint boughtTokens, uint balance);

    constructor() Ownable(msg.sender) {
        token = IERC20(_token);
        tokenOwner = address(_tokenOwner);
        RATE = rate;
    }

    function buyToken() external payable {
        require(msg.value > 0, "You must send some Ether to buy tokens");
        uint tokenAmount = msg.value * RATE;
        require(token.transferFrom(tokenOwner, msg.sender, tokenAmount), "Token transfer failed");
        emit BuyToken(msg.sender, msg.value, tokenAmount, address(this).balance);
    }

    function withdrawETH() external {
        require(msg.sender == owner(), "Not the contract owner");
        payable(msg.sender).transfer(address(this).balance);
    }
}
