pragma solidity ^0.8.0;

/* @title GENEX Protocol for human derived assets
 * @author GENEX
 * @dev Interface of the GNX20 standard.
 */

interface IGNX01 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function setAdmin(address account) external returns (bool);
    function repurchase(address account, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed owner, uint256 value);
}

contract GNX01 is IGNX01 {

    mapping(address => uint256) private balance;

    address private _admin;
    address private _owner;
    string private _name;
    string private _symbol;
    uint256 private _totalSupply;

    constructor(
        address admin_,
        address owner_,
        // ideally is bytes32 but cannot dynamically hex value from constructor input
        string memory name_,
        string memory symbol_,
        uint256 totalSupply_
    ) public {
        _admin = admin_;
        _owner = owner_;
        _name = name_;
        _symbol = symbol_;
        _totalSupply = totalSupply_;
        
        // Address of initial supply
        balance[msg.sender] = _totalSupply;
    }

    function admin() public view returns (address) {
        return _admin;
    }

    function owner() public view returns (address) {
        return _owner;
    }

    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    function decimals() public pure returns (uint8) {
        return 18;
    }

    function balanceOf(address account) public view virtual override returns (uint256) {
        return balance[account];
    }

    // transfer
    
    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
        _transfer(msg.sender, recipient, amount);
        return true;
    }
    
    function _transfer(
        address sender,
        address recipient,
        uint256 amount
    ) internal virtual {
        require(sender != address(0), "GNX01: Cannot transfer from address (0)");
        require(recipient != address(0), "GNX01: Cannot transfer to address(0) - did you mean to burn()?");

        // check if sender has enough to transfer
        uint256 senderBalance = balance[sender];
        require(senderBalance >= amount, "GNX01: Transfer amount exceeds available balance");
        
        // SafeMath
        unchecked {
            balance[sender] = senderBalance - amount;
        }
        
        // update recipient balance
        balance[recipient] += amount;

        emit Transfer(sender, recipient, amount); 
    }  
    
    // mint
    
    function mint(address account, uint256 amount) public virtual override returns (bool) {
        _mint(msg.sender, account, amount);
        return true;
    }
    
    function _mint(
        address msgSender,
        address account,
        uint256 amount
    ) internal virtual {
    
        // can only be initiated by owner or admin
        require(msgSender == _owner || msgSender == _admin);

        // update account balance
        balance[account] += amount;
        
        // increase totalSupply
        _totalSupply += amount;
        
        emit Transfer(address(0), account, amount);
    }

    // burn
    
    function burn(uint256 amount) public virtual override returns (bool) {
        _burn(msg.sender, amount);
        return true;
    }
    
    function _burn(address msgSender, uint256 amount) internal virtual {

        // can only be initiated by owner or admin
        require(msgSender == _owner || msgSender == _admin);
    
        // only burn from owner account
        balance[_owner] -= amount;
    
        // reduce total supply
        _totalSupply -= amount;
        
        emit Burn(_owner, amount);
    }
    
    // repurchase
    
    function repurchase(
        address account,
        uint256 amount
    ) public virtual override returns (bool) {
        _repurchase(msg.sender, account, amount);
        return true;
    }
    
    function _repurchase(
        address msgSender,
        address account,
        uint256 amount
    ) internal virtual {

        // only admin can initiate
        require(msgSender == _admin, "GNX01: Admin permissions required");
        
        //  recipient must always be _owner address
        _transfer(account, _owner, amount);
        
        emit Transfer(account, _owner, amount);
    }
    
    // setAdmin

    function setAdmin(address account) public virtual override returns (bool) {
        _setAdmin(msg.sender, account);
        return true;
    }
    
    function _setAdmin(address fromAcc, address toAcc) internal virtual {
        require(fromAcc == _admin);
        _admin = toAcc;
    }
}