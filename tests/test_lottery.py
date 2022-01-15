# 0.038
# 380000000000000000
 

from brownie import Lottery, accounts, network, config
from scripts import helpful_scripts
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"], {"from": account})
    
    assert lottery.getEntranceFee() > Web3.toWei(1.5, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(2.2, "ether")