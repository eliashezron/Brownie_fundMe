from brownie import network, accounts, config, MockV3Aggregator, FundMe
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    deployMocks,
    getAccount,
    get_PriceFeed,
)
from web3 import Web3


def fund():
    # Fund the contract
    if len(FundMe) > 0:
        print("Funding contract...")
        FundMe[-1].fund({"from": getAccount(), "value": Web3.toWei(60, "ether")})
        print("Funding complete!")
    else:
        account = getAccount()
        priceFeed = get_PriceFeed()
        fund_me = FundMe.deploy(
            priceFeed,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get("verify"),
        )
        contract = fund_me.fund(
            {"from": getAccount(), "value": Web3.toWei(60, "ether")}
        )
        contract.wait(1)
        print("Funding complete!")


def withdraw():
    # Withdraw funds from the contract
    if len(FundMe) > 0:
        print("Withdrawing funds...")
        FundMe[-1].withdraw({"from": getAccount()})
        print("Withdrawal complete!")
    else:
        account = getAccount()
        priceFeed = get_PriceFeed()
        fund_me = FundMe.deploy(
            priceFeed,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get("verify"),
        )
        contract = fund_me.withdraw({"from": getAccount()})
        contract.wait(1)
        print("Withdrawal complete!")


def main():
    fund()
    withdraw()
