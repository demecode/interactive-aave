from brownie import network, config, accounts


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "ganache-local-3", "mainnet-fork"]
def get_account(index=None, id=None):
    # accounts[0] is ganache
    # accounts.add("env") - local env variables
    # accounts.load("id")
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None
