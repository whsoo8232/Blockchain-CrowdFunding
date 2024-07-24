// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ARTC_Funding is ReentrancyGuard, Ownable {
    IERC20 public USDT;
    IERC20 public ARTC;
    address public ARTC_owner;

    // USDT contract distribute
    address public _USDT = 0x777af890456cFcF93431D37E756ec06bf190e3a7;

    // token contract distribute
    address public _ARTC = 0x130ac05a2a5C8ba2e83021eFC0E442EA2B297f5d;
    address public _ARTC_owner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    uint public decimals = 18;

    event Buy_ARTC_With_ETH(address user, uint depositETH, uint boughtARTC, uint fee, uint balance, uint id);
    event Buy_ARTC_With_USDT(address user, uint depositUSDT, uint boughtARTC, uint fee, uint balance, uint id);
    event Withdraw_ETH(address user, uint amount);
    event Withdraw_ARTC(address user, uint amount);
    event Withdraw_USDT(address user, uint amount);
    
    constructor() Ownable(msg.sender) {
        USDT = IERC20(_USDT);
        ARTC = IERC20(_ARTC);
        ARTC_owner = _ARTC_owner;
    }

    function contract_ARTC_balance() external view returns (uint256) {
        return ARTC.balanceOf(address(this));
    }

    function contract_ETH_balance() external view returns (uint256) {
        return address(this).balance;
    }

    function contract_USDT_balance() external view returns (uint256) {
        return USDT.balanceOf(address(this));
    }    

    function buy_ARTC_with_ETH(uint256 buyARTC_amount, uint256 ETH_fee, uint256 _id) external payable {
        require(msg.value - ETH_fee > 0, "You must send some Ether to buy tokens");
        require(ARTC.transfer(msg.sender, buyARTC_amount), "ARTC transfer failed");
        emit Buy_ARTC_With_ETH(msg.sender, msg.value, buyARTC_amount, ETH_fee, address(this).balance, _id);
    }

    function buy_ARTC_with_USDT(uint256 USDT_amount, uint256 buyARTC_amount, uint256 USDT_fee, uint256 _id) external payable {
        require(USDT_amount - USDT_fee > 0, "You must send some Ether to buy tokens");
        require(USDT.transferFrom(msg.sender, address(this), USDT_amount + USDT_fee), "USDT transfer failed");
        require(ARTC.transfer(msg.sender, buyARTC_amount), "ARTC transfer failed");
        emit Buy_ARTC_With_USDT(msg.sender, USDT_amount, buyARTC_amount, USDT_fee, USDT.balanceOf(address(this)), _id);
    }

    function withdraw_ETH() external onlyOwner {
        uint256 contractBalance = address(this).balance;
        payable(msg.sender).transfer(address(this).balance);
        emit Withdraw_ETH(msg.sender, contractBalance);
    }

    function withdraw_ARTC() external onlyOwner {
        uint256 contractBalance = ARTC.balanceOf(address(this));
        require(ARTC.transfer(msg.sender, ARTC.balanceOf(address(this))), "balance transfer failed");
        emit Withdraw_ARTC(msg.sender, contractBalance);
    }

    function withdraw_USDT() external onlyOwner {
        uint256 contractBalance = USDT.balanceOf(address(this));
        require(USDT.transfer(msg.sender, USDT.balanceOf(address(this))), "balance transfer failed");
        emit Withdraw_USDT(msg.sender, contractBalance);
    }
}
