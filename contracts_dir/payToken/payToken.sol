// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract payToken is ERC20, ReentrancyGuard, Ownable {
    uint public totalValue;
    uint public _totalValue = 1000000000000;

    constructor() ERC20("payToken","PTK") Ownable(msg.sender) {
        totalValue = _totalValue;
        _mint(msg.sender, totalValue * 10**decimals());
    }
}
