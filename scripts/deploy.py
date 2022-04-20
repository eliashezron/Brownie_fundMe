from brownie import FundMe, MockV3Aggregator, accounts, network, config
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    deployMocks,
    get_PriceFeed,
    getAccount,
)


def deploy():
    # Deploy the contract
    account = getAccount()
    priceFeed = get_PriceFeed()
    fund_me = FundMe.deploy(
        priceFeed,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Contract address:", fund_me.address)
    return fund_me


def main():
    deploy()
