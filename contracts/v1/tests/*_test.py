import pytest
import brownie

from brownie import accounts, GNXNative, GNXToken, GNXPool, GNXPoolFactory, GNXTokenFactory


# Create Token on behalf of User
# <!-- Old way! Now using fixtures ! -->
#tx = tokenfactory.createGNXToken("Test Token","TST", 1000, accounts[1], {"from":accounts[0]})
#test_token = tx.new_contracts[0] # gives address of new contract
#test_token = GNXToken.at(test_token) # creates new contract from address
# test_token = GNXToken.at(tx.new_contracts[0]) <!-- alternative way of writing above inline

@pytest.fixture
def native():
    return accounts[0].deploy(GNXNative)

@pytest.fixture
def poolfactory(native):
    return accounts[0].deploy(GNXPoolFactory, native)

@pytest.fixture
def tokenfactory():
    return accounts[0].deploy(GNXTokenFactory)

@pytest.fixture
def test_token(tokenfactory):
    tx = tokenfactory.createGNXToken("Test Token", "TST", 1000, accounts[1], {"from":accounts[0]})
    contract = GNXToken.at(tx.new_contracts[0])
    return contract

@pytest.fixture
def test_pool(poolfactory, test_token):
    tx =  poolfactory.createPool(test_token, {"from":accounts[0]})
    contract = GNXPool.at(tx.new_contracts[0])
    return contract

@pytest.fixture
def liquid_pool(poolfactory, test_token, native):
    tx =  poolfactory.createPool(test_token, {"from":accounts[0]})
    contract = GNXPool.at(tx.new_contracts[0])

    native.transfer(accounts[1], 1000, {"from":accounts[0]})            # Give Account 1 native
    native.approve(contract, 1000, {"from":accounts[1]})                # Approve liquidity pool for native
    test_token.approve(contract, 1000, {"from":accounts[1]})            # Approve liquidity pool for TST

    contract.addLiquidity(1000,1000, {"from":accounts[1]})              # Add liquidity

    return contract

# Every function name has to have "test_..."
def test_deployment(native, poolfactory, tokenfactory):

    assert native.balanceOf(accounts[0]) == 10**9
    assert poolfactory.hasRole(poolfactory.DEFAULT_ADMIN_ROLE(),accounts[0]) == True      
    assert tokenfactory.hasRole(tokenfactory.DEFAULT_ADMIN_ROLE(),accounts[0]) == True

# User 1 creates token
def test_user_token(test_token):

    assert test_token.issuer() == accounts[1]
    assert test_token.balanceOf(accounts[0]) == 0
    assert test_token.balanceOf(accounts[1]) == 1000

# User 1 creates pool
def test_create_pool(test_pool, poolfactory, native, test_token):

    assert test_pool.factory() == poolfactory
    assert test_pool.native() == native
    assert test_pool.token() == test_token
    assert test_pool.totalSupply() == 0

# User 1 adds liquidity
def test_add_liquidity(native, test_token, test_pool):

    native.transfer(accounts[1], 1000, {"from":accounts[0]})
    native.approve(test_pool, 1000, {"from":accounts[1]})
    test_token.approve(test_pool, 1000, {"from":accounts[1]})
    test_pool.addLiquidity(1000,1000, {"from":accounts[1]})

    assert test_pool.nativeReserve() == 1000
    assert test_pool.tokenReserve() == 1000
    assert test_pool.balanceOf(accounts[1]) == 1000

# User 2 buys User 1 token (TST)
def test_user_purchase(liquid_pool, native, test_token):

    native.transfer(accounts[2], 1000, {"from":accounts[0]})    # send Native to Account 2

    native.approve(liquid_pool, 500, {"from":accounts[2]})      # approve liquidity pool to use GNX
    liquid_pool.buyTokens(380, 500, {"from":accounts[2]})       # buy tokens with GNX

    assert test_token.balanceOf(accounts[2]) > 0                # account to should have received TST
    assert native.balanceOf(liquid_pool) > 1000                 # amount of GNX in pool should have increased

# Fraud User (3) tries to create token
def test_fraud_token(tokenfactory):
    with brownie.reverts():
        fraud_token = tokenfactory.createGNXToken("Fraud Token", "FRT", 1000, accounts[3], {"from":accounts[3]})
    
# Fraud User (3) tries to create liquidity pool with User 1 token
def test_fraud_pool(poolfactory, test_token):
    with brownie.reverts():
        fraud_pool = poolfactory.createPool(test_token, {"from":accounts[3]})

# User 4 creates a new token and pool !
def test_new_token(poolfactory, tokenfactory, native):

    tx = tokenfactory.createGNXToken("ABC Token", "ABC", 1000000, accounts[4], {"from":accounts[0]})
    new_token = tx.events["GNXTokenCreated"]["GNXToken"]
    new_token = GNXToken.at(new_token)

    tx = poolfactory.createPool(new_token, {"from":accounts[0]})
    new_pool = tx.events["poolCreated"]["pool"]
    new_pool = GNXPool.at(new_pool)

    assert new_pool.native() == native