// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

// Token protocols
import {IERC20Upgradeable} from "@openzeppelin-upgradeable/contracts/token/ERC20/IERC20Upgradeable.sol";
import {ERC20Upgradeable} from "@openzeppelin-upgradeable/contracts/token/ERC20/ERC20Upgradeable.sol";
import {IERC1363Upgradeable} from "@openzeppelin-upgradeable/contracts/interfaces/IERC1363Upgradeable.sol";
import {ERC1363Upgradeable} from "./ERC1363Upgradeable.sol";

// Peripheral protocols
import {Initializable} from "@openzeppelin-upgradeable/contracts/proxy/utils/Initializable.sol";
import {ContextUpgradeable} from "@openzeppelin-upgradeable/contracts/utils/ContextUpgradeable.sol";

// Access control
import {AccessControlUpgradeable} from "@openzeppelin-upgradeable/contracts/access/AccessControlUpgradeable.sol";

// Proxy Upgrades
import {UUPSUpgradeable} from "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";

// Interface detection
import {IERC165Upgradeable} from "@openzeppelin-upgradeable/contracts/interfaces/IERC165Upgradeable.sol";
import {ERC165Upgradeable} from "@openzeppelin-upgradeable/contracts/utils/introspection/ERC165Upgradeable.sol";

  /** 
    * @title GNXToken - the GENEX human equity security created by an issuer.
    *
    * @author Bailey de Villiers (https://github.com/itchysnake)
    *
    * @notice The base GNX Token used for human equity based securities. Version 
    * 1 does not yet support dividends. The security is based on the upgradeable
    * ERC1363, which is an improved ERC20 protocol.
    */

interface IGNXToken is IERC20Upgradeable {

    function issuer() external view returns (address);
    function mint(address _address, uint256 _amount) external returns (bool);
    function burn(address _address, uint256 _amount) external returns (bool);
    
    event TokenCreated(address indexed factory, address indexed token, address issuer);
}

// Inheritance must follow this path for solidity C3 linearization
contract GNXToken is
    Initializable,
    ContextUpgradeable,
    ERC165Upgradeable,
    AccessControlUpgradeable,
    ERC1363Upgradeable,
    UUPSUpgradeable,
    IGNXToken {
    
    /// Issuer's role
    bytes32 public constant ROLE_ISSUER = keccak256("ISSUER");

    /// Minter role
    bytes32 public constant ROLE_MINTER = keccak256("MINTER");

    // Issuer's address
    address public override (IGNXToken) issuer;

   /* Creates new GNX Token
    * 
    * @notice Creation of GNX Token. Called by GNX Token Factory to create
    * proxies.
    *
    * @dev Refer to ERC1967Proxy, UUPSUpgradeable, TransparentUpgradeableProxy.
    *
    * @param _name Token name
    * @param _symbol Token symbol
    * @param _initialSupply Number of initial tokens
    * @param _issuer Address of issuer
    * @param _minter Minter address (passed by factory)
    * @param _admin Admin address (passed by factory)
    *
    * @return bool Initialisation was successful
    */
    function initialize(
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply,
        address _issuer,
        address _minter,
        address _admin
    ) public initializer returns (bool) {

        // init funtions
        __Context_init_unchained();
        __ERC165_init_unchained();
        __ERC20_init_unchained(_name, _symbol);
        __AccessControl_init_unchained();

        issuer = _issuer;                           // sets public issuer address

        _setupRole(DEFAULT_ADMIN_ROLE, _admin);     // sets the admin role
        _setupRole(ROLE_ISSUER, _issuer);           // sets the issuer role
        _setupRole(ROLE_MINTER, _minter);           // sets the minter role

        _setRoleAdmin(ROLE_ISSUER, ROLE_ISSUER);    // sets the admin of ROLE_ISSUER to 
                                                    // ROLE_ISSUER, making them their
                                                    // own admin.

        _mint(_issuer, _initialSupply);             // mints initial supply
        
        emit TokenCreated(msg.sender, _issuer, address(this));
        
        return true;
    }

   /* UUPS compliant by adding access control (onlyRole)
    * 
    * @notice Refer to ERC1967Proxy, UUPSUpgradeable, TransparentUpgradeableProxy.
    * 
    * @notice Inherit UUPSUpgradeable and add access control to create UUPS compliant
    *         implementation. TransparentUpgradeableProxy and UUPS implementation
    *         cannot be used together.
    *
    * @param newImplementation New implementation contract address
    */
    function _authorizeUpgrade(address newImplementation)
        internal
        override(UUPSUpgradeable)
        onlyRole(DEFAULT_ADMIN_ROLE) {
    }

   /* Mints new GNXTokens to recipient
    *
    * @notice Only accessible to ROLE_MINTER
    *
    * @param _recipient Recipient of the new tokens
    * @param _amount Quantity minted
    * 
    * @return bool If mint was succesful
    */ 
    function mint(address _recipient, uint256 _amount) public override(IGNXToken) onlyRole(ROLE_MINTER) returns (bool) {
        _mint(_recipient, _amount);
        return true;
    }

   /* Burns existing GNXTokens from address
    *
    * @notice Only accessible to ROLE_MINTER
    *
    * @param _from Address to burn tokens from
    * @param _amount Quantity burned
    *
    * @return bool If burn was succesful
    */
    function burn(address _from, uint256 _amount) public override(IGNXToken) onlyRole(ROLE_MINTER) returns (bool) {
        _burn(_from, _amount);
        return true;
    }
    
    // @inheritdoc ERC165Upgradeable
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC165Upgradeable, AccessControlUpgradeable, ERC1363Upgradeable)
        returns (bool)
    {
        return
            interfaceId == type(IERC20Upgradeable).interfaceId ||
            interfaceId == type(IERC1363Upgradeable).interfaceId ||
            super.supportsInterface(interfaceId);
    }
}