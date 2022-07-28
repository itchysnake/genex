// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Context} from "@openzeppelin/contracts/utils/Context.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

interface IGNXToken is IERC20 {
  function mint(address _address, uint256 _amount) external returns (bool);
  function burn(address _address, uint256 _amount) external returns (bool);
  
  event TokenCreated(address indexed factory, address indexed token, address issuer);
}

contract GNXToken is
  Context,
  AccessControl,
  ERC20,
  IGNXToken {
    
    bytes32 public constant ROLE_ISSUER = keccak256("ISSUER");    // Issuer role

    address public issuer;                  // issuer address
    address public factory;                 // connected factory

    constructor(
      string memory _name,
      string memory _symbol,
      uint256 _initialSupply,
      address _issuer,
      address _admin
    ) ERC20(_name, _symbol) {
      issuer = _issuer;                           // sets issuer address
      factory = msg.sender;                         // sets factory address
      _setupRole(DEFAULT_ADMIN_ROLE, _admin);     // sets admin role
      _setupRole(ROLE_ISSUER, _issuer);           // sets issuer role
      _setRoleAdmin(ROLE_ISSUER, ROLE_ISSUER);    // sets issuer as their own admin
      _mint(_issuer, _initialSupply);             // mints initial supply
      emit TokenCreated(factory, _issuer, address(this));
    }

    function mint(address _recipient, uint256 _amount) public override(IGNXToken) onlyRole(DEFAULT_ADMIN_ROLE) returns (bool) {
      _mint(_recipient, _amount);
      return true;
    }

    function burn(address _from, uint256 _amount) public override(IGNXToken) onlyRole(DEFAULT_ADMIN_ROLE) returns (bool) {
      _burn(_from, _amount);
      return true;
    }
}