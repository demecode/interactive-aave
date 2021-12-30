
from scripts.helpers import get_account
from brownie import interface, network, config

def get_weth():
    """ mints weth by depositing ehter"""
        # get an account
    account = get_account()
    
    # get weth contract using interface
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])

    # now lets use the weth function
    tx = weth.deposit({"from": account, "value":0.1 * 10 ** 18 })
    tx.wait(2)
    print('Got 0.1 weth')
    
def main():
    get_weth() 
    