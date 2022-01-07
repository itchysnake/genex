from web3 import Web3
import solcx

# compiling with solc
"""
compiled = solcx.compile_files(
                source_files = ["/Users/baileydevilliers/Desktop/Code/genex/ganache-test/token.sol"],
                output_values = ["bin","abi"])
"""

# mainnet related
"""
# link to unfura
infura_url = "https://mainnet.infura.io/v3/573f58ae51344e73bd2084be51163d83"

web3 = Web3(Web3.HTTPProvider(infura_url))

print(web3.isConnected())
print(web3.eth.getBalance("0x90e63c3d53E0Ea496845b7a03ec7548B70014A91"))

# ABI (interface) is required to interact with on-chain contract from off-chain
# This is typical ERC20 ABI
abi = [{"constant":True,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":False,"inputs":[],"name":"Pause","type":"event"},{"anonymous":False,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]
address = "0xd26114cd6EE289AccF82350c8d8487fedB8A0C07"
contract = web3.eth.contract(address = address, abi = abi)

total_supply = contract.functions.totalSupply().call()
print(total_supply/(10**18))
"""

# Ganache testing
"""
# link to local ganache chain
ganache_url = "HTTP://127.0.0.1:7545"

# instantiate web3 instance
web3 = Web3(Web3.HTTPProvider(ganache_url))

account_1 = "0x436481Ff70631BC0Db3b9b326af021fFB5ff3a88"
priv_key = "3aff41642042a2baeb8445eebc34475770d75011abed453ac5e03faf050fbae7"
account_2 = "0xf962129643943A4135B9B0607f767674f7819FF1"
# building the transaction
nonce = web3.eth.getTransactionCount(account_1)

tx = {
      "nonce": nonce,
      "to": account_2,
      "value": 1 * 10**18,
      "gas":2000000,
      "gasPrice": 5 * 10**9
}

# signing transaction
signed_tx = web3.eth.account.signTransaction(tx, priv_key)

# send transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(web3.toHex(tx_hash))
"""

# deploying a contract
"""
import json

# contract details
abi = json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
bytecode = "6060604052341561000f57600080fd5b6040805190810160405280600581526020017f48656c6c6f0000000000000000000000000000000000000000000000000000008152506000908051906020019061005a929190610060565b50610105565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100a157805160ff19168380011785556100cf565b828001600101855582156100cf579182015b828111156100ce5782518255916020019190600101906100b3565b5b5090506100dc91906100e0565b5090565b61010291905b808211156100fe5760008160009055506001016100e6565b5090565b90565b61041a806101146000396000f300606060405260043610610057576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063a41368621461005c578063cfae3217146100b9578063ef690cc014610147575b600080fd5b341561006757600080fd5b6100b7600480803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919050506101d5565b005b34156100c457600080fd5b6100cc6101ef565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561010c5780820151818401526020810190506100f1565b50505050905090810190601f1680156101395780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561015257600080fd5b61015a610297565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561019a57808201518184015260208101905061017f565b50505050905090810190601f1680156101c75780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b80600090805190602001906101eb929190610335565b5050565b6101f76103b5565b60008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561028d5780601f106102625761010080835404028352916020019161028d565b820191906000526020600020905b81548152906001019060200180831161027057829003601f168201915b5050505050905090565b60008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561032d5780601f106103025761010080835404028352916020019161032d565b820191906000526020600020905b81548152906001019060200180831161031057829003601f168201915b505050505081565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061037657805160ff19168380011785556103a4565b828001600101855582156103a4579182015b828111156103a3578251825591602001919060010190610388565b5b5090506103b191906103c9565b5090565b602060405190810160405280600081525090565b6103eb91905b808211156103e75760008160009055506001016103cf565b5090565b905600a165627a7a7230582006f39b9b9b558a328403f9c048af30519c79e6536660d7660e8002af27f240930029"

web3.eth.defaultAccount = web3.eth.accounts[0]

# create contract
contract = web3.eth.contract(abi = abi, bytecode= bytecode)

# deployment and hash
tx_hash = contract.constructor().transact()
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

# create contract object from chain
contract_obj = web3.eth.contract(
    address = tx_receipt.contractAddress,
    abi = abi)

print("Address: ",tx_receipt.contractAddress)
print("Current greeting: ",contract_obj.functions.greet().call())
"""

# inspecting mainnet blocks
"""
from web3 import Web3

infura_url = "https://mainnet.infura.io/v3/573f58ae51344e73bd2084be51163d83"

web3 = Web3(Web3.HTTPProvider(infura_url))

print(web3.eth.getBlock("latest"))
"""