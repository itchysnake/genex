// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import {GNXToken} from "../tokens/GNXToken.sol";
import {GNXNative} from "../tokens/GNXNative.sol";
import {GNXPoolFactory} from "./GNXPoolFactory.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

  /** 
    * @title GNXPool - Liquidity trading pools for wrapped GNXToken and GNXNative
    * @author Bailey de Villiers (https://github.com/itchysnake)
    * @dev Liquidity pool derived from Uniswap-V1. To be used specifically with
    * GNX Pool Factory, GNX Tokens, and GNX Native.
    */

interface IGNXPool {
    function tokenReserve() external view returns (uint256);
    function nativeReserve() external view returns (uint256);
    function addLiquidity(uint256 tokenDeposit, uint256 nativeDeposit) external returns (uint256);
    function removeLiquidity(uint256 amount) external returns (uint256, uint256);
    function nativeToToken(uint256 nativeSold) external returns (uint256);
    function tokenToNative(uint256 tokensSold) external returns (uint256);
    function buyNative(uint256 minNative, uint256 tokensSold) external returns (uint256);
    function buyTokens(uint256 minTokens, uint256 nativeSold) external returns (uint256);
    function tokenSwap(uint256 tokensSold, uint256 minTokens, address GNXTokenAddress) external;
    function _tokenSwap(uint256 minTokens, uint256 nativeSold, address recipient) external;
    
    event liquidityChange(address indexed from, address indexed to, uint256 amount);
    event Trade(address indexed trader, address output, uint256 inputAmount, uint256 outputAmount);
}

contract GNXPool is ERC20, IGNXPool {
    
    GNXToken public token;                  // Wrapped GNXToken
    GNXNative public native;                // GNXNative token
    address public factory;                 // Parent GNX pool factory

    // Contract is an ERC20 to provide LP rewards
    constructor(address _GNXToken, address _GNXNative) ERC20("GENEX-V1","GNXV1") {
        require(_GNXToken != address(0), "GNX: invalid token address");
        
        token = GNXToken(_GNXToken);
        native = GNXNative(_GNXNative);
        factory = msg.sender;
    }

  /** View function for GNXToken reserve
    * 
    * @notice View function for GNXTokens stored in this contract
    *
    * @return Amount of GNXNative held in this contract
    */
    function tokenReserve() public override(IGNXPool) view returns(uint256){
        return token.balanceOf(address(this));
    }
    
  /** View function for GNXNative reserve
    * 
    * @notice View function for GNXNative stored in this contract.
    *
    * @return Amount of GNXNative held in this contract.
    */
    function nativeReserve() public override(IGNXPool) view returns(uint256){
        return native.balanceOf(address(this));
    }

  /** Ability to add liquidity to the pool (mints LP tokens)
    * 
    * @notice Add liquidity of GNXToken and GNXNative to this trading pool. Users
    * are rewarded in LP which can be exchanged for liquidity and trading accrued
    * fees.
    *
    * @notice Liquidity of both tokens added must be equal. Technically only
    * one param required but having two params for both tokens makes it clear
    * that both are required to add liquidity.
    *
    * @dev ERC20 LP tokens are minted equal to the GNXNative deposit made.
    * Required deposit amount must be calculated in front-end. Equal deposit
    * is enforced by contract to prevent price manipulation.
    *
    * @param tokenDeposit Quantity of GNXToken deposited.
    * @param nativeDeposit Quantity of GNXNative deposited.
    *
    * @return Quantity of LP tokens minted to msg.sender.
    */
    function addLiquidity(uint256 tokenDeposit, uint256 nativeDeposit) public override(IGNXPool) returns (uint256) {
        
        // Iniital liquidity add
        if (tokenReserve() == 0) {
            // Pulling GNXToken
            token.transferFrom(msg.sender, address(this), tokenDeposit);
            // Pulling GNXNative
            native.transferFrom(msg.sender, address(this), nativeDeposit);
            
            // Sends LPs in exchange for initial deposit
            uint256 _nativeReserve = nativeReserve();
            _mint(msg.sender, _nativeReserve);

            emit liquidityChange(msg.sender, address(this), _nativeReserve);
            
            return _nativeReserve;
            
        // Normal liquidity add
        } else {
        
            uint256 _nativeReserve = nativeReserve() - nativeDeposit;
            uint256 _tokenReserve = tokenReserve();
            uint256 tokenOutput = (nativeDeposit * _tokenReserve) / _nativeReserve;
            
            require(nativeDeposit >= tokenOutput, "GNX: insufficient token amount"); // Maintains pool price
            
            // Pulls GNXToken
            token.transferFrom(msg.sender, address(this), tokenDeposit);
            // Pulls GNXNative
            native.transferFrom(msg.sender, address(this), nativeDeposit);
            
            // Mints LP tokens
            uint256 liquidityTokens = (totalSupply() * nativeDeposit) / _nativeReserve;
            _mint(msg.sender, liquidityTokens);

            emit liquidityChange(msg.sender, address(this), nativeDeposit);

            return liquidityTokens;
        }
    }
    
  /** Exchange LPs for equal return of GNXToken and GNXNative.
    * 
    * @notice Burn LP tokens in exchange for GNXNative and GNXTokens based 
    * on current reserves, and amount being submitted. Portion of accrued fees
    * are also returned in the respective token. Potentially results in
    * impermenant loss.
    *
    * @param amount Quantity of LP tokens submitted for exchange.
    *
    * @return Tuple of GNXNative output, and GNXToken output.
    */
    function removeLiquidity(uint256 amount) public override(IGNXPool) returns (uint256, uint256) {
        require(amount > 0, "GNX: amount too low");
        
        uint256 nativeOutput = (nativeReserve() * amount) / totalSupply();
        uint256 tokenOutput = (tokenReserve() * amount) / totalSupply();
        
        // returns an equal amount of GNXNative and GNXToken and burns LP tokens
        _burn(msg.sender, amount);
        token.transfer(msg.sender, tokenOutput);
        native.transfer(msg.sender, nativeOutput);
        
        emit liquidityChange(address(this), msg.sender, amount);
        
        return (nativeOutput, tokenOutput);
    }
        
  /** Private pricing function
    * 
    * @notice Private function used to determine "price," or output amount
    * of one of the two assets traded in the pool. Fee is set to 0.5% and 
    * is accrued in the token used as input.
    *
    * @dev Calculation is derived from uniswap's constant product AMM, x*y=k.
    *
    * @param inputAmount Quantity of tokens sent, or intend to be sent by user.
    * @param inputReserve Quantity of output tokens stored in contract.
    * @param outputReserve Quantity of output tokens stored in contract.
    *
    * @return Output token amount.
    */
    function getAmount(
        uint256 inputAmount,
        uint256 inputReserve,
        uint256 outputReserve
    ) private pure returns(uint256) {
        require(inputReserve > 0 && outputReserve > 0, "GNX: invalid reserves");
        
        // 0.5% fee
        uint256 inputAmountWithFee = inputAmount * 995;
        uint256 numerator = inputAmountWithFee * outputReserve;
        uint256 denominator = (inputReserve*1000) + inputAmountWithFee;
        
        // Returns (outputAmount, totalFee)
        return (numerator/denominator);
    }
    
  /** Lookup function
    * 
    * @notice Lookup function to call current price for selling GNXNative to
    * receive GNXToken.
    *
    * @param nativeSold Quantity of GNXNative to be sold.
    *
    * @return Output GNXToken amount.
    */
    function nativeToToken(uint256 nativeSold) public view override(IGNXPool) returns (uint256) {
        require(nativeSold > 0, "GNX: too few GNXNative");
        uint256 _tokenReserve = tokenReserve();
        uint256 _nativeReserve = nativeReserve();
        return getAmount(nativeSold, _nativeReserve, _tokenReserve);
    }
   
  /** Lookup function
    * 
    * @notice Lookup function to call current price for selling GNXToken to
    * receive GNXNative.
    *
    * @param tokensSold Quantity of GNXTokens to be sold.
    *
    * @return Output GNXNative amount.
    */
    function tokenToNative(uint256 tokensSold) public view override(IGNXPool) returns (uint256) {
        require(tokensSold > 0, "GNX: too few GNXToken");
        uint256 _tokenReserve = tokenReserve();
        uint256 _nativeReserve = nativeReserve();
        return getAmount(tokensSold, _tokenReserve, _nativeReserve);
    }
    
  /** Private buy function
    * 
    * @notice Private buy function which allows additional flexibility for
    * public buyToken functions (or variations thereof).
    *
    * @dev Used to provide additional flexibility in the two other methods of
    * tokens purchase. First method is generic purchase (buyTokens), while second
    * is reserved for _tokenSwap allowing two tokens to be exchanged from pool
    * to pool.
    *
    * @param minTokens Minimum number of tokens expected from output. Enforced
    * in front-end to prevent price spoofing with bots.
    * @param nativeSold Quantity of GNXNative sold.
    * @param recipient Recipient of the output quantity of GNXTokens.
    *
    * @return Quantity of GNXTokens output.
    */
    function _buyTokens(
        uint256 minTokens,
        uint256 nativeSold,
        address recipient
    ) private returns (uint256) {

        uint256 _tokenReserve = tokenReserve();
        uint256 _nativeReserve = nativeReserve();
        
        // Calculate tokenOutput for GNXNative user sent
        uint256 tokenOutput = getAmount(
            nativeSold, 
            _nativeReserve - nativeSold, 
            _tokenReserve
        );
        
        require(tokenOutput > minTokens, "GNX: minTokens not met");

        // Pull GNXNative
        token.transferFrom(msg.sender, address(this), nativeSold);
        // Send GNXToken
        native.transfer(recipient ,tokenOutput);
        
        emit Trade(recipient, address(token), nativeSold, tokenOutput);
        
        return tokenOutput;
    }
     
  /** Generic purchase function for GNXNative
    * 
    * @notice General purchase function where GNXTokens are sold in exchange 
    * for GNXNative. Requires stating a minimum expected return to prevent
    * price spoofing.
    *
    * @dev This function is akin to tokenSwawp. This is the base function
    * for switching from GNXTokens to GNXNative.
    *
    * @param minNative Minimum expected output quantity of GNXNative.
    * @param tokensSold Quantity of GNXTokens sold.
    *
    * @return Quantity of GNXNative output.
    */
    function buyNative(uint256 minNative, uint256 tokensSold) public override(IGNXPool) returns (uint256) {
        require(token.balanceOf(msg.sender) >= tokensSold, "GNX: not enough GNXTokens");

        uint256 _tokenReserve = tokenReserve();
        uint256 _nativeReserve = nativeReserve();
        
        uint256 nativeOutput = getAmount(tokensSold, _tokenReserve, _nativeReserve);
        
        require(nativeOutput > minNative, "GNX: minNative not met");

        // Pull GNXToken
        token.transferFrom(msg.sender, address(this), tokensSold);
        // Send GNXNative
        native.transfer(msg.sender, nativeOutput);
        
        emit Trade(msg.sender, address(native), tokensSold, nativeOutput);
        
        return nativeOutput;
    }
    
  /** Generic purchase function for GNXTokens.
    * 
    * @notice General purchase function for exchanging GNXNative for GNXTokens.
    *
    *
    * @param minTokens Minimum number of tokens expected from output.
    * @param nativeSold Quantity of GNXNative sold.
    *
    * @return Quantity of GNXTokens output.
    */
    function buyTokens(uint256 minTokens, uint256 nativeSold) public override(IGNXPool) returns (uint256) {
    
        // Checks if user has enough GNXNative to sell
        require(native.balanceOf(msg.sender) >= nativeSold,"GNX: not enough GNXNative");
        
        uint256 tokenOutput = _buyTokens(minTokens, nativeSold, msg.sender);
        
        return tokenOutput;
    }
    
  /** helper function specifically for tokenSwap --> only meant for other exchange contracts
    * ONLY FOR EXCHANGE CONTRACTS
    *
    * Helper function specifically for _tokenSwap / tokenSwap.
    *
    * @notice Facilitates token to token swaps. Allows the circumvension of 
    * double fees when changing from one GNXToken to another GNXToken. 
    *
    * @dev Used for GNXToken to GNXToken swaps. Done through exchanging GNXTokens
    * in an intial swap to GNXToken which is then swapped to another GNXToken.
    *
    * @dev Should not be interacted with directly by user calls. This exists
    * for other contracts to facilitate token swaps.
    *
    * @param minTokens Minimum number of tokens expected from output.
    * @param nativeSold Quantity of GNXNative sold.
    */
    function _tokenSwap(uint256 minTokens, uint256 nativeSold, address recipient) public override {
        _buyTokens(minTokens, nativeSold, recipient);
    }
    
    // Token to Token (GNXToken --> GNXToken) routed through Factory
    function tokenSwap(
        uint256 tokensSold,
        uint256 minTokens,
        address GNXTokenAddress
    ) public override(IGNXPool) {
    
        // Checks if there is an exchange for the other token contract listed on this factory
        address poolAddress = GNXPoolFactory(factory).getPool(GNXTokenAddress);
        
        require(
            poolAddress != address(this) && poolAddress != address(0),
            "GNX: invalid pool");
        
        // Swaps token for GNXNative
        uint256 _tokenReserve = tokenReserve();
        uint256 _nativeReserve = nativeReserve();
        uint256 nativeOutput = getAmount(tokensSold, _tokenReserve, _nativeReserve);

        // Pulls GNXToken
        token.transferFrom(msg.sender, address(this), tokensSold);
        
        // Uses nativeOutput for purchase function, fee only charged once
        
        // Sends GNXNative to other pool for swap
        IGNXPool(poolAddress)._tokenSwap(
            minTokens,
            nativeOutput,
            msg.sender);
    }
}