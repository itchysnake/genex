// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {Initializable} from "@openzeppelin-upgradeable/contracts/proxy/utils/Initializable.sol";
import {ContextUpgradeable} from "@openzeppelin-upgradeable/contracts/utils/ContextUpgradeable.sol";
import {ERC165Upgradeable} from "@openzeppelin-upgradeable/contracts/utils/introspection/ERC165Upgradeable.sol";
import {IAccessControlEnumerableUpgradeable, AccessControlEnumerableUpgradeable} from "@openzeppelin-upgradeable/contracts/access/AccessControlEnumerableUpgradeable.sol";

import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

import "@openzeppelin/contracts/proxy/beacon/UpgradeableBeacon.sol";
import "@openzeppelin/contracts/proxy/beacon/BeaconProxy.sol";

import {GNXToken} from "../tokens/GNXToken.sol";

  /**
    * @title GNXTokenFactory
    * @author Bailey de Villiers (https://github.com/itchysnake)
    * @notice Creates proxy token contracts from the GNXToken wrapper
    */

interface IGNXTokenFactory {
    event GNXTokenCreated(address indexed factory, address indexed issuerAddress, address GNXToken);
}

contract GNXTokenFactory is
    Initializable, 
    ContextUpgradeable,
    ERC165Upgradeable,
    AccessControlEnumerableUpgradeable,
    IGNXTokenFactory {
    
    // Minter address assigned to the "minter" on GNX Tokens (can be different from Admin)
    // GNXTokenFactory does not have minter position, used to pass into GNX Token
    bytes32 public constant ROLE_MINTER = keccak256("MINTER");
    address public minter;
    
    // Links issuer address to their token address
    mapping(address => address) public issuerToGNXToken;
    // Links GNXToken address to issuer address
    mapping(address => address) public GNXTokenToIssuer;
    
    address public implementationBeacon;
    
    // ! NOTE : If use Constructor --> under gas limit (barely)
    // ! NOTE : If use initialize --> over gas limit (barely)
    

    constructor(){        
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        
        // Creates a single upgradeable beacon, transfers ownership to msg.sender, and sets it as the implementation beacon
        UpgradeableBeacon _beacon = new UpgradeableBeacon(address(new GNXToken()));      // Creates an upgradeable beacon from the token
        _beacon.transferOwnership(msg.sender);                  // transfers ownership of the upgradeable becon to the initializer
        implementationBeacon = address(_beacon);                // sets the implementationBeacon to the upgradeable beacon
    }
    /*
    function initialize() public virtual initializer {
        __Context_init_unchained();
        __ERC165_init_unchained();
        __AccessControlEnumerable_init_unchained();

        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);                 // Sets the default admin upon initialise

        UpgradeableBeacon _beacon = new UpgradeableBeacon(address(new GNXToken()));      // Creates an upgradeable beacon from the token
        _beacon.transferOwnership(msg.sender);                  // transfers ownership of the upgradeable becon to the initializer
        implementationBeacon = address(_beacon);                // sets the implementationBeacon to the upgradeable beacon
    }
    */
    
    // Allows us to change the minter who manages tokens, but admin can remain the same
    function setMinter(address _minter) public onlyRole(DEFAULT_ADMIN_ROLE) {
        minter = _minter;
        _setupRole(ROLE_MINTER, _minter);
    }
    
  /** Create proxy GNX Token
    * 
    * @notice Creates a GNXToken proxy contract. Selects initialiser specifically
    * of GNX Token contract and sets params.
    *
    * @dev Only admin can create token.
    *
    * @return Amount of GNXNative held in this contract.
    */
    function createGNXToken(
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply,
        address _issuerAddress
    ) public onlyRole(DEFAULT_ADMIN_ROLE) returns (address) {
        
        // Wallet can only have 1 GNXToken
        require(issuerToGNXToken[_issuerAddress] == address(0), "GNX: issuer already has token");        
    
        BeaconProxy proxy = new BeaconProxy(                    // proxy contract
            implementationBeacon,                               // sets pointer to implementation beacon
            abi.encodeWithSelector(                             // encodes params
                GNXToken(address(0x0)).initialize.selector,     // initialize function
                _name,                                          // token name
                _symbol,                                        // token symbol
                _initialSupply,                                 // token initial supply
                _issuerAddress,                                 // issuer address
                minter,                                         // predfined minter address
                getRoleMember(DEFAULT_ADMIN_ROLE, 0)            // admin is the creator of the factory
            )
        );
        
        address _GNXToken = address(proxy);                  // replaces proxy object with _GNXToken address var

        GNXTokenToIssuer[_GNXToken] = _issuerAddress;        // sets token address to issuer's address
        issuerToGNXToken[_issuerAddress] = _GNXToken;        // sets issuer address to their token adderss

        emit GNXTokenCreated(address(this), _issuerAddress, _GNXToken);

        return _GNXToken;
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC165Upgradeable, AccessControlEnumerableUpgradeable)
        returns (bool)
    {
        return AccessControlEnumerableUpgradeable.supportsInterface(interfaceId);
    }
}