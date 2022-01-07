// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {GNXPool} from "./GNXPool.sol";

// Upgradeables

interface IGNXPoolFactory {
    function createPool(address GNXTokenAddress) external returns (address);
    function getPool(address GNXTokenAddress) external view returns (address);
    
    event poolCreated(address indexed factory, address indexed token, address pool);
}

contract GNXPoolFactory is IGNXPoolFactory {
    
    mapping(address => address) public tokenToPool;
    
    address public implementationBeacon;
    address public native;
    
    constructor(address _GNXNative) {
        native = _GNXNative;
    }
    
    // !NOTE : Add access control ! Make adminOnly
    
    function createPool(address GNXTokenAddress) public override returns (address) {
        require(GNXTokenAddress != address(0), "GNX: invalid token");
        require(tokenToPool[GNXTokenAddress] == address(0), "GNX: pool exists");
        
        // Creates new pool from GNXTokenAddress
        GNXPool pool = new GNXPool(GNXTokenAddress, native);
        
        // Links token address to pool address
        tokenToPool[GNXTokenAddress] = address(pool);
        
        emit poolCreated(address(this), GNXTokenAddress, address(pool));
        
        return address(pool);
    }
    
    function getPool(address GNXTokenAddress) public override view returns (address) {
        return tokenToPool[GNXTokenAddress];
    }
    
}