// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {GNXPool} from "./GNXPool.sol";

import {AccessControlUpgradeable} from "@openzeppelin-upgradeable/contracts/access/AccessControlUpgradeable.sol";

   /*
    * @title GNXPoolFactory
    *
    * @author Bailey de Villiers (https://github.com/itchysnake)
    *
    * @notice Creates trading pools for GNX Token securities
    *
    * @notice Unlike GNX Tokens, pool functionalities are not upgradeable. New
    * pool versions and factories will be released in the future.
    *
    * @dev Only GNXTokens and GNXNative can be used as trading pairs.
    */

interface IGNXPoolFactory {
    function createPool(address GNXTokenAddress) external returns (address);
    function getPool(address GNXTokenAddress) external view returns (address);
    
    event poolCreated(address indexed factory, address indexed token, address pool);
}

contract GNXPoolFactory is IGNXPoolFactory, AccessControlUpgradeable {
    
    mapping(address => address) public tokenToPool;     // maps tokens to pools ("Test Token" --> 0x0a12)
    
    address public native;
    
    constructor(address _GNXNative) {
        
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);     // sets the admin role
        native = _GNXNative;                            // sets GNX native address
        
    }
    
    // Creates GNXPool
    // 
    // @notice Creates a GNXPool from the GNXToken address and the GNXNative
    // 
    // @dev Only accessable to admin
    //
    // @return Address of pool
    function createPool(address GNXTokenAddress) public override onlyRole(DEFAULT_ADMIN_ROLE) returns (address) {
        require(GNXTokenAddress != address(0), "GNX: invalid token");               // check for legitimate address
        require(tokenToPool[GNXTokenAddress] == address(0), "GNX: pool exists");    // check if pool already exists
        
        // Creates new pool from GNXTokenAddress
        GNXPool pool = new GNXPool(GNXTokenAddress, native);
        
        // Links token address to pool address
        tokenToPool[GNXTokenAddress] = address(pool);
        
        emit poolCreated(address(this), GNXTokenAddress, address(pool));
        
        return address(pool);
    }
    
    // Lookup function
    // 
    // @notice Checks to see if a pool address is registered to this factory
    function getPool(address GNXTokenAddress) public override view returns (address) {
        return tokenToPool[GNXTokenAddress];
    }
    
}