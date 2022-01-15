from brownie import accounts, config, network, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken
from web3 import Web3

FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
INITIAL_VALUE = 200000000000

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    
    if id:
        return accounts.load(id)
    
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in  FORKED_LOCAL_ENVIRONMENT:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config if defined, 
    else it will deploy a mock version of tht contract and return the mock contract
    
        Args:
            contract_name (string)
        
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of this
            contract     
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        
        contract = contract_type[-1]
    
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    
    return contract
         
def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks Deployed")
