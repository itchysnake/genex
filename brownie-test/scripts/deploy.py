from brownie import accounts, GNXNative, GNXToken, GNXPoolFactory, GNXTokenFactory

# basically web3.py throughout here (some shit brownie specific syntax tho)

def main():
    # Deploy native
    tx = accounts[0].deploy(GNXNative)
    contract_native = GNXNative[0]

    # Deploy GNXPoolFacotry (! need GNXNative address)
    tx = accounts[0].deploy(GNXPoolFactory, contract_native.address)
    contract_pool_factory = GNXPoolFactory[0]

    # Deploy GNXTokenFacotry
    tx = accounts[0].deploy(GNXTokenFactory)
    contract_token_factory = GNXTokenFactory[0]
