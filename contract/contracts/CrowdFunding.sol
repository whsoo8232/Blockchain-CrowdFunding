// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CrowdFunding is ReentrancyGuard, Ownable {
    IERC20 public token;
    address public tokenOwner;
    uint public RATE;
    uint public FEE;

    // token contract distribute
    address public _token = 0xBafBe8Dc6b88868A7b58F6E5df89c3054dec93bB;
    address public _tokenOwner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    uint public decimals = 10**18;

    // service distribute
    uint public _rate = 100000;
    uint public _fee = 1 * decimals;

    event BuyToken(address user, uint inputETH, uint tokenForETH, uint fee, uint boughtTokens, uint balance);
    event WithdrawETH(address user, uint amount);
    
    constructor() Ownable(msg.sender) {
        token = IERC20(_token);
        tokenOwner = address(_tokenOwner);
        RATE = _rate;
        FEE = _fee;
    }

    function contractBalance() external view returns (uint256) {
        return address(this).balance;
    }    

    function buyToken(uint256 tokenAmount) external payable {
        require(msg.value - FEE > 0, "You must send some Ether to buy tokens");
        uint ETHAmount = msg.value - FEE;
        tokenAmount = tokenAmount * decimals;
        require(token.transferFrom(tokenOwner, msg.sender, tokenAmount), "Token transfer failed");
        emit BuyToken(msg.sender, msg.value, ETHAmount, FEE, tokenAmount, address(this).balance);
    }
    
    function withdrawETH() external {
        require(msg.sender == owner(), "Not the contract owner");
        payable(msg.sender).transfer(address(this).balance);
        emit WithdrawETH(msg.sender, address(this).balance);
    }
}
