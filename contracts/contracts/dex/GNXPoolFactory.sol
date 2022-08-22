// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {GNXPool} from "./GNXPool.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

interface IGNXPoolFactory {
    function createPool(address GNXTokenAddress) external returns (address);
    function getPool(address GNXTokenAddress) external view returns (address);
    
    event poolCreated(address indexed factory, address indexed token, address pool);
}

contract GNXPoolFactory is IGNXPoolFactory, AccessControl {
    
  bytes32 public constant ROLE_MINTER = keccak256("MINTER");
  address public native;
  mapping(address => address) public tokenToPool;     // maps tokens to pools ("Test Token" --> 0x0a12)
  
  constructor(address _GNXNative) {
      _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);     // sets the admin role
      _grantRole(ROLE_MINTER, msg.sender);
      native = _GNXNative;                            // sets GNX native address
    }
    
  /** Creates GNXPool
    * 
    * @notice Creates a GNXPool from the GNXToken address and the GNXNative
    * 
    * @dev Only accessable to admin
    *
    * @return Address of pool
    */
  function createPool(address GNXTokenAddress) public override onlyRole(ROLE_MINTER) returns (address) {
      require(GNXTokenAddress != address(0), "GNX: invalid token");               // check for legitimate address
      require(tokenToPool[GNXTokenAddress] == address(0), "GNX: pool exists");    // check if pool already exists
      
      // Creates new pool from GNXTokenAddress
      GNXPool newPool = new GNXPool(GNXTokenAddress, native);
      
      // Links token address to pool address
      tokenToPool[GNXTokenAddress] = address(newPool);
      
      emit poolCreated(address(this), GNXTokenAddress, address(newPool));
      
      return address(newPool);
  }
    
  /** Lookup function
    *
    * @notice Checks to see if a pool address is registered to this factory
    *
    * @return Pool address
    */
    function getPool(address GNXTokenAddress) public override view returns (address) {
        return tokenToPool[GNXTokenAddress];
    }
}