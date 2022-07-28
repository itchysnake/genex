// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

  /**
    * @title GNXNative
    * @author Bailey de Villiers (https://github.com/itchysnake)
    * @notice GENEX (decentralised exchange) native token contract
    * @dev Used in all GNXPool exchanges.
    */

contract GNXNative is IERC20, ERC20 {

    address public admin;

    constructor() ERC20("GNXNative","GNX"){
        admin = msg.sender;
        _mint(msg.sender,10**9);        // 1 billion
    }
    
    function mint(
        address _recipient,
        uint256 _amount
    ) public {
        require(msg.sender == admin);
        _mint(_recipient, _amount);
    }
}