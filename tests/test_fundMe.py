from brownie import network, accounts, config, MockV3Aggregator, FundMe, exceptions
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    deployMocks,
    getAccount,
    get_PriceFeed,
)
from scripts.deploy import deploy
from web3 import Web3
import pytest

# arrange
def test_fund():
    account = getAccount()
    priceFeed = get_PriceFeed()
    fund_me = FundMe.deploy(
        priceFeed,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # act
    contract = fund_me.fund({"from": getAccount(), "value": Web3.toWei(60, "ether")})
    contract.wait(1)
    print("Funding complete!")
    # assert
    assert fund_me.addressToAmountFunded(account.address) == Web3.toWei(60, "ether")
    tx = fund_me.withdraw({"from": getAccount()})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
