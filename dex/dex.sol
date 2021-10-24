pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DEX {
    
    IERC20 token;
    uint256 public totalLiquidity;
    
    /* Account liquidity */
    mapping (address => uint256) public liquidity;
    
    constructor (address token_address) public {
        token = IERC20(token_address);
    }
    

    function init(uint256 tokens) public payable returns (uint256) {
        /* checks if already init'd */
        require(totalLiquidity == 0, "GNXDEX: Liquidity established");
        
        /* sets dex liquidity to this acc balance (not sure bal of what) */
        totalLiquidity == address(this).balance;
        
        /* sets address(this).liquidity to total liquidity => can be written better */
        liquidity[msg.sender] = totalLiquidty;
        
        /* ERC20 token transfer to build pool */
        require(token.transferFrom(msg.sender), address(this), tokens));
        
        return totalLiquidity
    }

    function price(
        uint256 input_amount,
        uint256 input_reserve,
        uint256 output_reserve
    ) public view returns (uint256) {
        uint256 input_amount_with_fee = input_amount.mul(997);
        uint256 numerator = inpput_amount_with_fee.mul(output_reserve);
        uint256 denominator = input_reserve.mul(1000).add(input_amount_with_fee);
        return numerator/denominator
    }
    
    function ethToToken() public payable returns (uint256) {
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 tokens_bought = price(msg.value, address(this).balance.sub(msg.value), token_reserve);
        require(token.transfer(msg.sender, tokens_bought));
        return tokens_bought
    }

}