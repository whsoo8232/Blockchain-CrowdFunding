import os
from dotenv import load_dotenv

from web3 import Web3
from coinbase.wallet.client import Client


### Common ###
def decimals():
    return 18


def coinbase_coin_spot_price(coin, currency):
    api_key = "organizations/1d87c8de-839b-4ef5-b73a-d6dca9bc9988/apiKeys/23fe4062-96b9-438c-b14f-e4b088fa8417"
    api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEINMjhjFpmI1H+BJ4Vrq51mwomQtiZuaVLOV9jrsmYA++oAoGCCqGSM49\nAwEHoUQDQgAE/erXjwh+7HVnEdL4RjHb3Au6iCORFxA3SqvJDG6EpDxFDEtqtUtr\nWxl2NmPUaFK10tuPb6gvodjDZswH5aJKBw==\n-----END EC PRIVATE KEY-----\n"
    client = Client(api_key, api_secret)
    coinPair = coin + "-" + currency
    priceData = client.get_spot_price(currency_pair=coinPair)
    return priceData  # return Dict


def connect_web3(connect_host, apikey):
    # Mainnet #
    if connect_host == "ethereum":
        rpc_url = "https://mainnet.infura.io/v3/" + apikey
    elif connect_host == "polygon":
        rpc_url = "https://polygon-mainnet.infura.io/v3/" + apikey
    # Testnet #
    elif connect_host == "sepolia":
        rpc_url = "https://sepolia.infura.io/v3/" + apikey
    elif connect_host == "amoy":
        rpc_url = "https://polygon-amoy.infura.io/v3/" + apikey
    else:
        return None
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    return web3


def get_contract(web3, contractAddress, contractAbi):
    file = open(contractAbi, "r", encoding="utf-8")
    contractAddr = web3.to_checksum_address(contractAddress)
    contract = web3.eth.contract(abi=file.read(), address=contractAddr)

    return contract


def ARTC_approve_to_fundingContract(
    web3,
    ARTC_contract,
    ARTC_owner_address,
    ARTC_owner_pk,
    fundingContract_address,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(ARTC_owner_address)
    To_add = web3.to_checksum_address(fundingContract_address)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    safeAllow = 100  # For exchange rate fluctuations during transaction
    ARTC_amount = (ARTC_amount + safeAllow) * 10 ** decimals()
    tx = ARTC_contract.functions.approve(To_add, ARTC_amount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, ARTC_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def USDT_approve_to_fundingContract(
    web3,
    USDT_contract,
    buyer,
    buyer_pk,
    fundingContract_address,
    USDT_amount,
    serviceFee,
):
    From_add = web3.to_checksum_address(buyer)
    To_add = web3.to_checksum_address(fundingContract_address)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    USDT_amount = USDT_amount * 10 ** decimals()
    serviceFee = serviceFee * 10 ** decimals()
    tokenAmount = USDT_amount + serviceFee
    tx = USDT_contract.functions.approve(To_add, tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def get_fundingContract_totalETH(fundingContract):
    totalBalance = fundingContract.functions.contract_ETH_balance().call()

    return totalBalance


def get_fundingContract_totalUSDT(fundingContract):
    totalBalance = fundingContract.functions.contract_USDT_balance().call()

    return totalBalance


def buy_ARTC_with_ETH(
    web3,
    fundingContract,
    buyer,
    buyer_pk,
    depositETH_amount,
    serviceFee,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    ARTC_amount = int(ARTC_amount * 10 ** decimals())
    depositETH_amount = int(depositETH_amount * 10 ** decimals())
    serviceFee = int(serviceFee * 10 ** decimals())
    tx = fundingContract.functions.buy_ARTC_with_ETH(
        ARTC_amount, serviceFee
    ).build_transaction(
        {
            "from": From_add,
            "nonce": nonce,
            "gasPrice": gas_price,
            "value": depositETH_amount + serviceFee,
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def buy_ARTC_with_USDT(
    web3,
    fundingContract,
    buyer,
    buyer_pk,
    USDT_amount,
    serviceFee,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    ARTC_amount = int(ARTC_amount * 10 ** decimals())
    USDT_amount = int(USDT_amount * 10 ** decimals())
    serviceFee = int(serviceFee * 10 ** decimals())
    tx = fundingContract.functions.buy_ARTC_with_USDT(
        USDT_amount, ARTC_amount, serviceFee
    ).build_transaction({"from": From_add, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def withdraw_fundingContract_ETH(
    web3, fundingContract, fundingContract_owner, fundingContract_owner_pk
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    tx = fundingContract.functions.withdraw_ETH().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def withdraw_fundingContract_USDT(
    web3,
    fundingContract,
    fundingContract_owner,
    fundingContract_owner_pk,
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    tx = fundingContract.functions.withdraw_USDT().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


if __name__ == "__main__":
    load_dotenv(".env")
    INFURA_KEY = os.getenv("INFURA_API_KEY")
    MY_TESTMAIN = os.getenv("MY_TESTMAIN")
    MY_TESTMAIN_PK = os.getenv("MY_TESTMAIN_PK")
    MY_TESTTEST = os.getenv("MY_TESTTEST")
    MY_TESTTEST_PK = os.getenv("MY_TESTTEST_PK")

    # WEB3 setup
    network = "sepolia"
    web3 = connect_web3(network, INFURA_KEY)

    # ETH Funding Contract
    fundingContract_addr = "0x0404b75Cd5B46656D2C656b6DE3e79fA26b2771C"
    fundingContract_abi = "./contracts/ARTC_Funding/ARTC_Funding.abi"
    fundingContract = get_contract(web3, fundingContract_addr, fundingContract_abi)
    fundingContract_owner = MY_TESTMAIN  # tmp
    fundingContract_owner_pk = MY_TESTMAIN_PK  # tmp

    # ARTC Contract
    ARTC_contract_address = "0x130ac05a2a5C8ba2e83021eFC0E442EA2B297f5d"
    ARTC_contract_abi = "./contracts/testGovernance/testGovernance.abi"
    ARTC_contract = get_contract(web3, ARTC_contract_address, ARTC_contract_abi)
    ARTC_owner = MY_TESTMAIN  # tmp
    ARTC_owner_pk = MY_TESTMAIN_PK  # tmp

    # USDT contract
    USDT_contract_addr = "0x777af890456cFcF93431D37E756ec06bf190e3a7"
    USDT_contract_abi = "./contracts/payToken/payToken.abi"
    USDT_contract = get_contract(web3, USDT_contract_addr, USDT_contract_abi)

    # crypto change rate
    ETH_USDT = coinbase_coin_spot_price("ETH", "USDT")


### transaction part

# SET
buyer = "0x87460F55439594674891824dFF32ee5207d28A2f"
buyer_pk = "cc2a7a9600f102a3f0ab847bef6365bc59820afa7f8fed7d8bb4d4424da9b353"
tokenAmount = 100000
tokenAmount = tokenAmount * 10 ** decimals()

From_add = web3.to_checksum_address(fundingContract_addr)
To_add = web3.to_checksum_address(buyer)
gas_price = web3.eth.gas_price
nonce = web3.eth.get_transaction_count(From_add)
tx = ARTC_contract.functions.transfer(To_add, tokenAmount).build_transaction(
    {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
)
signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)


# buy ARTC with ETH
# deposit_ETH = 0.0001
# serviceFee = 0.0004
# tokenAmount = int(deposit_ETH * float(ETH_USDT["amount"]) * 10)
# ARTC_approve_to_fundingContract(
#     web3, ARTC_contract, ARTC_owner, ARTC_owner_pk, fundingContract_addr, tokenAmount
# )
allow = ARTC_contract.functions.allowance(ARTC_owner, fundingContract_addr).call()
print(allow)
# buy_ARTC_with_ETH(
#     web3, fundingContract, buyer, buyer_pk, deposit_ETH, serviceFee, tokenAmount
# )  # User sign with wallet


# # buy ARTC with USDT
# deposit_USDT = 100000
# serviceFee = 100
# tokenAmount = int(deposit_USDT) * 10  # USDT
# USDT_approve_to_fundingContract(
#     web3, USDT_contract, buyer, buyer_pk, fundingContract_addr, deposit_USDT, serviceFee
# )  # User sign with wallet
# ARTC_approve_to_fundingContract(
#     web3, ARTC_contract, ARTC_owner, ARTC_owner_pk, fundingContract_addr, tokenAmount
# )
# buy_ARTC_with_USDT(
#     web3, fundingContract, buyer, buyer_pk, deposit_USDT, serviceFee, tokenAmount
# )  # User sign with wallet
