

# deposit ether
# swap ether for weth or any other wrapped token

from scripts.helpers import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3


AMOUNT = Web3.toWei(0.1, "ether")
def main():
    account = get_account()
    erc20_token_address = config["networks"][network.show_active()]["weth_token"]
    
    # to test on a local testnet we need to get some weth
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
        
    # we need the ABI & contract address
    lending_pool = get_lending_pool()
    approve_tx = approve_erc(AMOUNT, lending_pool.address, erc20_token_address, account)
    
    print("DEPOSITING..")
    tx = lending_pool.deposit(erc20_token_address, AMOUNT, account.address, 0, {"from": account})
    tx.wait(1)
    print("DEPOSIT COMPLETE")
    
    # return the borrowed eth available and total debt in ether
    borrow_ether, total_debt  =  get_borrow_data(lending_pool, account)
    
    print('Lets borrow some DAI....')
    # 2. - lets get the price for dai and eth using chainlink pricefeed 
    dai_to_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    
    # now lets calculate the amount of dai to borrow
    # .92 used a buffer to ensure the helath score is better
    dai_borrow_amount = (1 / dai_to_eth_price) * (borrow_ether * 0.95)
    print(f'WE ARE ABOUT TO BORROW {dai_borrow_amount} DAI')
    
    # NOW TO BORROW
    # 1. Get the DAI address
    dai_address = config["networks"][network.show_active()]["dai_token"]
    
    # Create the borrow transaction
    borrow_tx = lending_pool.borrow(
        dai_address, 
        Web3.toWei(dai_borrow_amount, "ether"),
        1, 
        0, 
        account.address, 
        {"from": account}
    )
    
    # wait for the borrow to complete
    borrow_tx.wait(1)
    
    # confirm borrowed
    print('JUST BORROWED SOME DAI!!!')
    
    # this should return the new lending pool data if the borrowing is successful
    get_borrow_data(lending_pool, account)
    
    # lets repay the debt
    
    # repay_all(AMOUNT, lending_pool, account)
    print("TOTAL DEBT REPAID")
    
    
    
    
def repay_all(amount, lending_pool, account):

    # we need to first approve the token
    approve_erc(
        Web3.toWei(amount, "ether"), 
        lending_pool, config["networks"][network.show_active()]["dai_token"],
        account
        )
    
    # once approve, we can use the dai we got to pay back
    
    repay_tx = lending_pool.repay(config["networks"][network.show_active()]["dai_token"],
                                  amount,
                                  1,
                                  account.address,
                                  {'from': account}
                                  )
    repay_tx.wait(1)
    print("DEBT REPAID")
    
    
    
def get_asset_price(price_feed_address):
    # Ok - we are interacting with a contract. so we need:
    # ABI - interface
    # Address
    daith_eth_price_feed = interface.IAggregatorV3Interface(price_feed_address)
    latest_price = daith_eth_price_feed.latestRoundData()[1]
    converted_lasted_price = Web3.fromWei(latest_price, "ether")
    formated = format(converted_lasted_price, 'f')
    
    print(f'DAI/ETH price is {formated}')
    return float(formated)

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
     


    
    
    