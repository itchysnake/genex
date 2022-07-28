// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {Context} from "@openzeppelin/contracts/utils/Context.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
import {GNXToken} from "../tokens/GNXToken.sol";

interface IGNXTokenFactory {
    event GNXTokenCreated(address indexed factory, address indexed issuerAddress, address GNXToken);
}

contract GNXTokenFactory is
    Context,
    AccessControl,
    IGNXTokenFactory {
    
    bytes32 public constant ROLE_MINTER = keccak256("MINTER");
    
    mapping(address => address) public issuerToGNXToken;            // Links issuer address to their token address
    mapping(address => address) public GNXTokenToIssuer;            // Links GNXToken address to issuer address

    constructor(){        
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ROLE_MINTER, msg.sender);                // set GENEX as minter, saves a transaction
    }
    
    function createGNXToken(
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply,
        address _issuerAddress
    ) public onlyRole(ROLE_MINTER) returns (address) {
        
        // Wallet can only have 1 GNXToken
        require(issuerToGNXToken[_issuerAddress] == address(0), "GNX: issuer already has token");        
    
        GNXToken newToken = new GNXToken(
            _name,
            _symbol,
            _initialSupply,
            _issuerAddress,                                 // sets issuer address
            msg.sender                                      // sets admin --> can be licensed msg.sender or GNX
                                                            // factory automatically set as msg.sender
        );

        GNXTokenToIssuer[address(newToken)] = _issuerAddress;        // sets token address to issuer's address
        issuerToGNXToken[_issuerAddress] = address(newToken);        // sets issuer address to their token adderss

        emit GNXTokenCreated(address(this), _issuerAddress, address(newToken));

        return address(newToken);
    }

    /*
    To add a minter, find the ROLE_MINTER key "0x0.." and use grantRole
    */
}