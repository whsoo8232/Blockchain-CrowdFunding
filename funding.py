import os
from dotenv import load_dotenv

from web3 import Web3
from coinbase.wallet.client import Client


### Common ###
def decimals():
    return 18


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


def coinbase_coin_spot_price(coin, currency):
    api_key = "organizations/1d87c8de-839b-4ef5-b73a-d6dca9bc9988/apiKeys/23fe4062-96b9-438c-b14f-e4b088fa8417"
    api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEINMjhjFpmI1H+BJ4Vrq51mwomQtiZuaVLOV9jrsmYA++oAoGCCqGSM49\nAwEHoUQDQgAE/erXjwh+7HVnEdL4RjHb3Au6iCORFxA3SqvJDG6EpDxFDEtqtUtr\nWxl2NmPUaFK10tuPb6gvodjDZswH5aJKBw==\n-----END EC PRIVATE KEY-----\n"
    client = Client(api_key, api_secret)
    coinPair = coin + "-" + currency
    priceData = client.get_spot_price(currency_pair=coinPair)
    return priceData  # return Dict


def rewardToken_approve_to_fundingContract(
    web3,
    rewardTokenContract,
    rewardToken_owner_address,
    rewardToken_owner_pk,
    fundingContract_address,
    tokenAmount,
):
    From_add = web3.to_checksum_address(rewardToken_owner_address)
    To_add = web3.to_checksum_address(fundingContract_address)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    safeAllow = 100  # For exchange rate fluctuations during transaction
    tokenAmount = (tokenAmount + safeAllow) * 10 ** decimals()
    tx = rewardTokenContract.functions.approve(To_add, tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, rewardToken_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


### ETH_Funding
def buy_rewardToken_with_ETH(
    web3,
    fundingContract,
    buyer,
    buyer_pk,
    depositETH_amount,
    serviceFee,
    rewardToken_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    rewardToken_amount = int(rewardToken_amount * 10 ** decimals())
    depositETH_amount = int(depositETH_amount * 10 ** decimals())
    serviceFee = int(serviceFee * 10 ** decimals())
    tx = fundingContract.functions.buyToken(
        rewardToken_amount, serviceFee
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


def get_fundingContract_totalETH(fundingContract):
    totalBalance = fundingContract.functions.contractBalance().call()

    return totalBalance


def withdraw_fundingContract_ETH(
    web3, fundingContract, fundingContract_owner, fundingContract_owner_pk
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    tx = fundingContract.functions.withdrawETH().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


### Token Funding (USDT)
def payToken_approve_to_fundingContract(
    web3,
    payTokenContract,
    buyer,
    buyer_pk,
    fundingContract_address,
    payTokenAmount,
    serviceFee,
):
    From_add = web3.to_checksum_address(buyer)
    To_add = web3.to_checksum_address(fundingContract_address)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    payTokenAmount = payTokenAmount * 10 ** decimals()
    serviceFee = serviceFee * 10 ** decimals()
    tokenAmount = payTokenAmount + serviceFee
    tx = payTokenContract.functions.approve(To_add, tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def buy_rewardToken_with_token(
    web3,
    fundingContract,
    buyer,
    buyer_pk,
    payToken_amount,
    serviceFee,
    rewardToken_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    rewardToken_amount = int(rewardToken_amount * 10 ** decimals())
    payToken_amount = int(payToken_amount * 10 ** decimals())
    serviceFee = int(serviceFee * 10 ** decimals())
    tx = fundingContract.functions.buyToken(
        payToken_amount, rewardToken_amount, serviceFee
    ).build_transaction({"from": From_add, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def get_fundingContract_totalToken(fundingContract):
    totalBalance = fundingContract.functions.contractBalance().call()

    return totalBalance


def withdraw_fundingContract_token(
    web3,
    tokenFundingContract,
    tokenFundingContract_owner,
    tokenFundingContract_owner_pk,
):
    Owner_add = web3.to_checksum_address(tokenFundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    tx = tokenFundingContract.functions.withdrawToken().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, tokenFundingContract_owner_pk)
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
    web3 = Web3(Web3.HTTPProvider("https://1rpc.io/sepolia"))

    # reward token Contract (ARTC)
    rewardTokenContract_address = "0x130ac05a2a5C8ba2e83021eFC0E442EA2B297f5d"
    rewardTokenContract_abi = "./contracts/testGovernance/testGovernance.abi"
    rewardTokenContract = get_contract(
        web3, rewardTokenContract_address, rewardTokenContract_abi
    )
    rewardTokenOwner = MY_TESTMAIN
    rewardTokenOwner_pk = MY_TESTMAIN_PK

    # ETH Funding Contract
    ETHFundingContract_addr = "0xf1Eb1927C5C7e336f9f127062cD939D55e5dA6d1"
    ETHFundingContract_abi = "./contracts/ETH_Funding/ETH_Funding.abi"
    ETHFundingContract = get_contract(
        web3, ETHFundingContract_addr, ETHFundingContract_abi
    )
    ETHFundingContract_owner = MY_TESTMAIN
    ETHFundingContract_owner_pk = MY_TESTMAIN_PK

    # Token Funding contract (USDT)
    TokenFundingContract_addr = "0x433602e22a8380ad0eDaD95345D1C4D06A4b3763"
    TokenFundingContract_abi = "./contracts/Token_Funding/Token_Funding.abi"
    TokenFundingContract = get_contract(
        web3, TokenFundingContract_addr, TokenFundingContract_abi
    )
    TokenFundingContract_owner = MY_TESTMAIN
    TokenFundingContract_owner_pk = MY_TESTMAIN_PK

    # payToken contract
    payTokenContract_addr = "0x777af890456cFcF93431D37E756ec06bf190e3a7"
    payTokenContract_abi = "./contracts/payToken/payToken.abi"
    payTokenContract = get_contract(web3, payTokenContract_addr, payTokenContract_abi)

    # crypto change rate
    ETH_USDT = coinbase_coin_spot_price("ETH", "USDT")


### transaction part
## Buy with ETH--------------
# Buy script
buyer = MY_TESTTEST
buyer_pk = MY_TESTTEST_PK
deposit_ETH = 0.001
serviceFee = 0.0004
tokenAmount = int(deposit_ETH * float(ETH_USDT["amount"]) * 10)
rewardToken_approve_to_fundingContract(
    web3,
    rewardTokenContract,
    rewardTokenOwner,
    rewardTokenOwner_pk,
    ETHFundingContract_addr,
    tokenAmount,
)
buy_rewardToken_with_ETH(
    web3, ETHFundingContract, buyer, buyer_pk, deposit_ETH, serviceFee, tokenAmount
)

# # get contract total ETH
contractBalance = get_fundingContract_totalETH(ETHFundingContract)
print(contractBalance)

# # withdraw contracts ETH to contractOwner
withdraw_fundingContract_ETH(
    web3, ETHFundingContract, ETHFundingContract_owner, ETHFundingContract_owner_pk
)

## Buy with Token-------------
# Buy script
buyer = MY_TESTTEST
buyer_pk = MY_TESTTEST_PK
deposit_token = 100000
serviceFee = 100
tokenAmount = int(deposit_token) * 10  # USDT
payToken_approve_to_fundingContract(
    web3,
    payTokenContract,
    buyer,
    buyer_pk,
    TokenFundingContract_addr,
    deposit_token,
    serviceFee,
)
rewardToken_approve_to_fundingContract(
    web3,
    rewardTokenContract,
    rewardTokenOwner,
    rewardTokenOwner_pk,
    TokenFundingContract_addr,
    tokenAmount,
)
buy_rewardToken_with_token(
    web3, TokenFundingContract, buyer, buyer_pk, deposit_token, serviceFee, tokenAmount
)

# get contract total ETH
contractBalance = get_fundingContract_totalETH(TokenFundingContract)
print(contractBalance)

# withdraw contracts ETH to contractOwner
withdraw_fundingContract_token(
    web3,
    TokenFundingContract,
    TokenFundingContract_owner,
    TokenFundingContract_owner_pk,
)
