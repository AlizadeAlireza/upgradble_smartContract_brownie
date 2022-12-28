import pytest
from brownie import (
    Box,
    BoxV2,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    Contract,
    exceptions,
)
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy(
        {"from": account},
    )
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    box_v2 = BoxV2.deploy(
        {"from": account},
    )  # v2 implementatino
    # slapping boxV2.abi to the proxy.address
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    # this test will pass if this throws an error
    # we want this to throw error the first time we call it
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
