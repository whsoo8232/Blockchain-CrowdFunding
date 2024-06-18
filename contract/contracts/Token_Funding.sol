// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Token_Funding is ReentrancyGuard, Ownable {
    IERC20 public payToken;
    address public payTokenOwner;
    IERC20 public token;
    address public tokenOwner;
    uint public FEE;

    // payToken contract distribute
    address public _payToken = 0x3346280584c7A3afeaAD6Ebd4297560c22D654A5;
    address public _payTokenOwner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    // token contract distribute
    address public _token = 0xBafBe8Dc6b88868A7b58F6E5df89c3054dec93bB;
    address public _tokenOwner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    uint public decimals = 10**18;

    // service distribute
    uint public _fee = 10000000000000000;

    event BuyToken(address user, uint payTokens, uint fee, uint tokens);
    event WithdrawETH(address user, uint amount);
    
    constructor() Ownable(msg.sender) {
        payToken = IERC20(_payToken);
        payTokenOwner = _payTokenOwner;
        token = IERC20(_token);
        tokenOwner = _tokenOwner;
        FEE = _fee; 
    }

    function contractBalance() external view returns (uint256) {
        return payToken.balanceOf(address(this));
    }    

    function buyToken(uint256 payTokenAmount, uint256 tokenAmount) external payable {
        require(payTokenAmount > 0, "You must send some Ether to buy tokens");
        payTokenAmount = payTokenAmount * decimals;
        tokenAmount = tokenAmount * decimals;
        require(payToken.transferFrom(msg.sender, address(this), payTokenAmount), "PayToken transfer failed");
        require(token.transferFrom(tokenOwner, msg.sender, tokenAmount), "Token transfer failed");
        emit BuyToken(msg.sender, payTokenAmount, FEE, tokenAmount);
    }
    
    function approveBalance() external {
        require(payToken.approve(msg.sender, payToken.balanceOf(address(this))), "balance approve failed");
    }

    function withdrawETH() external {
        require(msg.sender == owner(), "Not the contract owner");
        require(payToken.transferFrom(address(this), msg.sender, payToken.balanceOf(address(this))), "balance transfer failed");
        emit WithdrawETH(msg.sender, address(this).balance);
    }
}
