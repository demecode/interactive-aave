

# deposit ether
# swap ether for weth or any other wrapped token

from scripts.helpers import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3


amount = Web3.toWei(0.1, "ether")
def main():
    account = get_account()
    erc20_token_address = config["networks"][network.show_active()]["weth_token"]
    
    # to test on a local testnet we need to get some weth
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
        
    # we need the ABI & contract address
    lending_pool = get_lending_pool()
    print(lending_pool)
    approve_erc(amount, lending_pool.address, erc20_token_address, account)
    
    print("DEPOSITING..")
    tx = lending_pool.deposit(erc20_token_address, amount, account.address, 0, {"from": account})
    tx.wait(1)
    print("DEPOSIT COMPLETE")
    
# We need a function to approve sending out the ERC20 tokens
def approve_erc(amount, spender, erc_address, account):
    print("APPROVING ERC TOKEN")
    erc = interface.IERC20(erc_address)
    tx = erc.approve(spender, amount, {'from': account})
    tx.wait(1)
    print("APPROVED")
    return tx
    
    
def get_lending_pool():
    # to get the lending pool, which is a contract
    # we need the abi and contract address
    
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    # able to use the getLendingPool functions as the address is returned
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    
    # get lending pool abi
    
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
    # now we can interact with the lending pool for aave


    
    

    