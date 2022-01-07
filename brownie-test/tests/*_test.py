from brownie import accounts, GNXNative, GNXToken, GNXPoolFactory, GNXTokenFactory
import pytest

def test_native():
    tx = accounts[0].deploy(GNXNative)
    contract = GNXNative[0]

    # quantity to to accounts [0] correct
    assert contract.balanceOf(accounts[0]) == 10**9

    # accounts [0] is minter
    contract.mint(accounts[0], 1, {'from': accounts[0]})
    assert contract.balanceOf(accounts[0]) == (10**9)+1

def 