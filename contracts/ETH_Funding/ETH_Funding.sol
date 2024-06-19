// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ETH_Funding is ReentrancyGuard, Ownable {
    IERC20 public token;
    address public tokenOwner;

    // token contract distribute
    address public _token = 0x130ac05a2a5C8ba2e83021eFC0E442EA2B297f5d;
    address public _tokenOwner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    uint public decimals = 18;

    event BuyToken(address user, uint depositETH, uint boughtTokens, uint fee, uint balance);
    event WithdrawETH(address user, uint amount);
    
    constructor() Ownable(msg.sender) {
        token = IERC20(_token);
        tokenOwner = _tokenOwner;
    }

    function contractBalance() external view returns (uint256) {
        return address(this).balance;
    }    

    function buyToken(uint256 tokenAmount, uint256 fee) external payable {
        require(msg.value - fee > 0, "You must send some Ether to buy tokens");
        require(token.transferFrom(tokenOwner, msg.sender, tokenAmount), "Token transfer failed");
        emit BuyToken(msg.sender, msg.value, tokenAmount, fee, address(this).balance);
    }
    
    function withdrawETH() external {
        require(msg.sender == owner(), "Not the contract owner");
        payable(msg.sender).transfer(address(this).balance);
        emit WithdrawETH(msg.sender, address(this).balance);
    }
}
