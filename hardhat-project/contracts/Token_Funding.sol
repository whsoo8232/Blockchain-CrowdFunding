// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Token_Funding is ReentrancyGuard, Ownable {
    IERC20 public payToken;
    IERC20 public token;
    address public tokenOwner;

    // payToken contract distribute
    address public _payToken = 0x777af890456cFcF93431D37E756ec06bf190e3a7;

    // token contract distribute
    address public _token = 0x130ac05a2a5C8ba2e83021eFC0E442EA2B297f5d;
    address public _tokenOwner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    uint public decimals = 10**18;

    event BuyToken(address user, uint payTokens, uint boughtTokens, uint fee, uint balance);
    event WithdrawETH(address user, uint amount);
    
    constructor() Ownable(msg.sender) {
        payToken = IERC20(_payToken);
        token = IERC20(_token);
        tokenOwner = _tokenOwner;
    }

    function contractBalance() external view returns (uint256) {
        return payToken.balanceOf(address(this));
    }    

    function buyToken(uint256 payTokenAmount, uint256 tokenAmount, uint256 fee) external payable {
        require(payTokenAmount - fee > 0, "You must send some Ether to buy tokens");
        require(payToken.transferFrom(msg.sender, address(this), payTokenAmount + fee), "PayToken transfer failed");
        require(token.transferFrom(tokenOwner, msg.sender, tokenAmount), "Token transfer failed");
        emit BuyToken(msg.sender, payTokenAmount, tokenAmount, fee, payToken.balanceOf(address(this)));
    }

    function withdrawToken() external onlyOwner {
        require(payToken.transfer(msg.sender, payToken.balanceOf(address(this))), "balance transfer failed");
        emit WithdrawETH(msg.sender, address(this).balance);
    }
}
