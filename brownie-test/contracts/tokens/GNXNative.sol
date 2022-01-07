// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

  /** 
    * @title GNXNative - Native token associated to the GENEX decentralised exchange and DAO.
    *
    * @author Bailey de Villiers (https://github.com/itchysnake)
    */

contract GNXNative is IERC20, AccessControl, ERC20 {
    constructor() ERC20("GNXNative","GNX"){
        
        _setupRole(DEFAULT_ADMIN_ROLE,msg.sender);
        
        _mint(msg.sender,10**9);        // 1 billion
    }
    
    function mint(
        address _recipient,
        uint256 _amount
    ) public onlyRole(DEFAULT_ADMIN_ROLE) returns (bool) {
        _mint(_recipient, _amount);
        return true;
    }
}