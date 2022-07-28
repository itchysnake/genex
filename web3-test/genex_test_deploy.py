from web3 import Web3
import json
import solcx

class Paths:
    
    def __init__(self):
        self.root = "/Users/baileydevilliers/Desktop/Code/genex/contracts/v1"
        self.pool = self.root+"/dex/GNXPool.sol"
        self.pool_factory = self.root+"/dex/GNXPoolFactory.sol"
        self.token_factory = self.root+"/dex/GNXtokenFactory.sol"
        self.native = self.root+"/tokens/GNXNative.sol"
        self.token = self.root+"/tokens/GNXToken.sol"

def test_connect():
    try:
        ganache_url = "HTTP://127.0.0.1:7545"
        
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        
        if web3 != None:
            print("true")
        
        else:
            print("false")
    except:
        print("false")

def compile_contracts():
    
    paths = Paths()
    
    output = solcx.compile_files(
        source_files = [paths.pool,
                        paths.pool_factory,
                        paths.token_factory,
                        paths.native,
                        paths.token],
        output_values = ["bin","abi"])
        
    return output

def build_deploy_contracts():

    # link to ganache
    ganache_url = "HTTP://127.0.0.1:7545"
    
    # instantiate web3
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    
    # choose account
    web3.eth.defaultAccount = web3.eth.accounts[0]
    
    # get all compiled contracts
    output = compile_contracts()
    
    # ! GENEX infrastructure (fixed) !
    

    # build native
    GNXNative = web3.eth.contract(abi = abi, bytecode= bytecode)
    # deploy native
    
    # build pool_factory
    # deploy pool_factory
    
    # build token_factory
    # deploy token_factory
    
    # ! User related (variable) !
    # build token
    # deploy token
    # build pool
    # deploy token
    
    # deploy and wait tx hash
    
    tx_hash = GNXNative.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    
    # py contract object
    contract = web3.eth.contract(
        address = tx_receipt.contractAddress,
        abi = abi)
    
    return contract.address

if __name__ == "__main__":
    output = compile_contracts()
    print(type(output))
    for i in output:
        print(i)