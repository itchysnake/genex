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

    /* Exchange functions */
    function price(
        uint256 input_amount,
        uint256 input_reserve,
        uint256 output_reserve
    ) public view returns (uint256) {
        uint256 input_amount_with_fee = input_amount.mul(997);
        uint256 numerator = inpput_amount_with_fee.mul(output_reserve);
        uint256 denominator = input_reserve.mul(1000).add(input_amount_with_fee);
        return numerator/denominator;
    }
    
    function ethToToken() public payable returns (uint256) {
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 tokens_bought = price(msg.value, address(this).balance.sub(msg.value), token_reserve);
        require(token.transfer(msg.sender, tokens_bought));
        return tokens_bought;
    }
    
    function tokenToEth(uint256 tokens) public returns (uint256) {
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 eth_bought = price(tokens, token_reserve, address(this).balance);
        msg.sender.transfer(eth_bought);
        require(token.transferFrom(msg.sender, address(this), tokens));
        return eth_bought;
    }

    /* Liquidity functions */
    function deposit() public payable returns (uint256) {
        uint256 eth_reserve = address(this).balance.sub(msg.value);
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 token_amount = (msg.value.mul(token_reserve) / eth_reserve.add(1));
        uint256 liquidity_minted = msg.value.mul(totalLiquidity) / eth_reserve;
        liquidity[msg.sender] = liquidity[msg.sender].add(liquidity_minted);
        require(token.transferFrom(msg.sender, address(this), token_amount));
        return liquidity_minted;
    }

    function withdraw(uint256 amount) public retrns (uint256) {
        uint256 token_reserve = token.balanceOf(address(this));
        uint256 eth_amount = amount.mul(address(this).balance) / totalLiquidity;
        uint256 token_amount = amount.mul(token_reserve) / totalLiquidity;
        liquidity[msg.sender] = liquidity[msg.sender].sub(eth_amount);
        totalLiquidity = totalLiquidity.sub(eth_amount);
        msg.sender.transfer(eth_amount);
        require(token.transfer(msg.sender, token_amount));
        return (eth_amount, token_amount);
    }

}