// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/AddressUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/introspection/ERC165Upgradeable.sol";

import "@openzeppelin/contracts-upgradeable/utils/ContextUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/interfaces/IERC1363Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/interfaces/IERC1363ReceiverUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/interfaces/IERC1363SpenderUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

  /**
    * @title ERC1363Upgradeable
    * @author Vittorio Minacori (https://github.com/vittominacori)
    * @author GENEX
    * @dev Upgradeable verion of Vittorio Minacori's ERC1363 implementation
    */

abstract contract ERC1363Upgradeable is
    Initializable,
    ContextUpgradeable,
    ERC165Upgradeable,
    ERC20Upgradeable,
    IERC1363Upgradeable {
    
    using AddressUpgradeable for address;

    function __ERC1363_init(string memory _name, string memory _symbol) internal initializer {
        __Context_init_unchained();
        __ERC165_init_unchained();
        __ERC20_init_unchained(_name, _symbol);
    }

    function __ERC1363_init_unchained(string memory _name, string memory _symbol) internal initializer {}

  /**
    * @dev See {IERC165-supportsInterface}.
    */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC165Upgradeable, IERC165Upgradeable)
        returns (bool)
    {
        return interfaceId == type(IERC1363Upgradeable).interfaceId || super.supportsInterface(interfaceId);
    }

  /**
    * @dev Transfer tokens to a specified address and then execute a callback on recipient.
    * @param recipient The address to transfer to.
    * @param amount The amount to be transferred.
    * @return A boolean that indicates if the operation was successful.
    */
    function transferAndCall(address recipient, uint256 amount) public virtual override returns (bool) {
        return transferAndCall(recipient, amount, "");
    }

  /**
    * @dev Transfer tokens to a specified address and then execute a callback on recipient.
    * @param recipient The address to transfer to
    * @param amount The amount to be transferred
    * @param data Additional data with no specified format
    * @return A boolean that indicates if the operation was successful.
    */
    function transferAndCall(
        address recipient,
        uint256 amount,
        bytes memory data
    ) public virtual override returns (bool) {
        transfer(recipient, amount);
        require(_checkAndCallTransfer(_msgSender(), recipient, amount, data), "ERC1363: _checkAndCallTransfer reverts");
        return true;
    }

  /**
    * @dev Transfer tokens from one address to another and then execute a callback on recipient.
    * @param sender The address which you want to send tokens from
    * @param recipient The address which you want to transfer to
    * @param amount The amount of tokens to be transferred
    * @return A boolean that indicates if the operation was successful.
    */
    function transferFromAndCall(
        address sender,
        address recipient,
        uint256 amount
    ) public virtual override returns (bool) {
        return transferFromAndCall(sender, recipient, amount, "");
    }

  /**
    * @dev Transfer tokens from one address to another and then execute a callback on recipient.
    * @param sender The address which you want to send tokens from
    * @param recipient The address which you want to transfer to
    * @param amount The amount of tokens to be transferred
    * @param data Additional data with no specified format
    * @return A boolean that indicates if the operation was successful.
    */
    function transferFromAndCall(
        address sender,
        address recipient,
        uint256 amount,
        bytes memory data
    ) public virtual override returns (bool) {
        transferFrom(sender, recipient, amount);
        require(_checkAndCallTransfer(sender, recipient, amount, data), "ERC1363: _checkAndCallTransfer reverts");
        return true;
    }

  /**
    * @dev Approve spender to transfer tokens and then execute a callback on recipient.
    * @param spender The address allowed to transfer to
    * @param amount The amount allowed to be transferred
    * @return A boolean that indicates if the operation was successful.
    */
    function approveAndCall(address spender, uint256 amount) public virtual override returns (bool) {
        return approveAndCall(spender, amount, "");
    }

  /**
    * @dev Approve spender to transfer tokens and then execute a callback on recipient.
    * @param spender The address allowed to transfer to.
    * @param amount The amount allowed to be transferred.
    * @param data Additional daa with no specified format.
    * @return A boolean that indicates if the operation was successful.
    */
    function approveAndCall(
        address spender,
        uint256 amount,
        bytes memory data
    ) public virtual override returns (bool) {
        approve(spender, amount);
        require(_checkAndCallApprove(spender, amount, data), "ERC1363: _checkAndCallApprove reverts");
        return true;
    }

  /**
    * @dev Internal function to invoke `onTransferReceived` on a target address
    *  The call is not executed if the target address is not a contract
    * @param sender address Representing the previous owner of the given token value
    * @param recipient address Target address that will receive the tokens
    * @param amount uint256 The amount mount of tokens to be transferred
    * @param data bytes Optional data to send along with the call
    * @return whether the call correctly returned the expected magic value
    */
    function _checkAndCallTransfer(
        address sender,
        address recipient,
        uint256 amount,
        bytes memory data
    ) internal virtual returns (bool) {
        if (!recipient.isContract()) {
            return false;
        }
        bytes4 retval = IERC1363ReceiverUpgradeable(recipient).onTransferReceived(_msgSender(), sender, amount, data);
        return (retval == IERC1363ReceiverUpgradeable(recipient).onTransferReceived.selector);
    }

  /**
    * @dev Internal function to invoke `onApprovalReceived` on a target address
    *  The call is not executed if the target address is not a contract
    * @param spender address The address which will spend the funds
    * @param amount uint256 The amount of tokens to be spent
    * @param data bytes Optional data to send along with the call
    * @return whether the call correctly returned the expected magic value
    */
    function _checkAndCallApprove(
        address spender,
        uint256 amount,
        bytes memory data
    ) internal virtual returns (bool) {
        if (!spender.isContract()) {
            return false;
        }
        bytes4 retval = IERC1363SpenderUpgradeable(spender).onApprovalReceived(_msgSender(), amount, data);
        return (retval == IERC1363SpenderUpgradeable(spender).onApprovalReceived.selector);
    }
}