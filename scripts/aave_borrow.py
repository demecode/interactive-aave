

# deposit ether
# swap ether for weth or any other wrapped token

from scripts.helpers import get_account
from brownie import network, config
from scripts.get_weth import get_weth


def main():
    account = get_account()
    erc20_token_address = config["networks"][network.show_active()]["weth_token"]
    
    # to test on a local testnet we need to get some weth
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
        
    
    # we need the ABI & contract address
    lending_pool = get_lending_pool()
    
def get_lending_pool():
    # to get the lending pool, which is a contract
    # we need the abi and contract address
    
    
    

    