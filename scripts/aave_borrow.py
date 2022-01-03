

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
    
    # return the borrowed eth available and total debt in ether
    borrow_ether, total_debt  =  get_borrow_data(lending_pool, account)
    
    
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
    
    # now we can interact with the lending pool for aave cos we return the lending pool
    return lending_pool
    


# we are using the getAccountData function from the lendingpool
# this function takes an address(lending pool address..I think) & a user (account)
# returns 6 types of data 

def get_borrow_data(lending_pool, account):
    (total_collaterallending, total_debt_eth, avail_borrow_eth,
     current_liquidation_threshold, ltv, health_factor) = lending_pool.getUserAccountData(account.address)
    
    # it will return sum in weth so need to convert to eth
    avail_borrow_eth = Web3.fromWei(avail_borrow_eth, "ether")
    total_collaterallending = Web3.fromWei(total_collaterallending, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    
    print(f'You gots {avail_borrow_eth} avaialbel to borrow eth depositied')
    print(f'You gots {total_collaterallending} available collateral in ether  to lend depositied')
    print(f'You gots {total_debt_eth} debt in ether depositied')
    
    return(float(avail_borrow_eth), float(total_debt_eth))
    
    
    