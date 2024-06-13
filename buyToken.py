import os
from dotenv import load_dotenv

from web3 import Web3
from coinbase.wallet.client import Client

def get_contract(web3, contractAddress, contractAbi):
    file = open(contractAbi, 'r', encoding='utf-8')
    contractAddr = web3.to_checksum_address(contractAddress)
    contract = web3.eth.contract(abi=file.read(), address=contractAddr)
    
    return contract

def coinbase_coin_spot_price(coin, currency):
    api_key = "organizations/1d87c8de-839b-4ef5-b73a-d6dca9bc9988/apiKeys/23fe4062-96b9-438c-b14f-e4b088fa8417"
    api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEINMjhjFpmI1H+BJ4Vrq51mwomQtiZuaVLOV9jrsmYA++oAoGCCqGSM49\nAwEHoUQDQgAE/erXjwh+7HVnEdL4RjHb3Au6iCORFxA3SqvJDG6EpDxFDEtqtUtr\nWxl2NmPUaFK10tuPb6gvodjDZswH5aJKBw==\n-----END EC PRIVATE KEY-----\n"
    client = Client(api_key, api_secret)
    coinPair = coin + "-" + currency
    priceData = client.get_spot_price(currency_pair = coinPair)
    return priceData #return Dict

def get_contract_totalETH(contract):
    totalBalance = contract.functions.contractBalance().call()
    
    return totalBalance

def token_approve(web3, contract, From, From_pk, To, tokenAmount):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    safeAllow = 100
    tokenAmount = (tokenAmount + safeAllow) * 10**18
    print(tokenAmount)
    tx = contract.functions.approve(To_add, tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt

def buy_token(web3, contract, From, From_pk, ETHAmount, tokenAmount):
    From_add = web3.to_checksum_address(From)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    ETHAmount = ETHAmount * contract.functions.decimals().call()
    serviceFee = contract.functions.FEE().call()
    tx = contract.functions.buyToken(tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price, "value": ETHAmount+serviceFee}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt

def withdrawETH(web3, contract, Owner, Owner_pk):
    Owner_add = web3.to_checksum_address(Owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    tx = contract.functions.withdrawETH().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, Owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt


if __name__ == "__main__":
    load_dotenv(".env")
    INFURA_KEY = os.getenv('INFURA_API_KEY')
    MY_TESTMAIN_PK = os.getenv('MY_TESTMAIN_PK')
    MY_TESTTEST = os.getenv('MY_TESTTEST')
    MY_TESTTEST_PK = os.getenv('MY_TESTTEST_PK')
    
# WEB3 setup
    network = "amoy"
    rpc_url = 'https://polygon-amoy.infura.io/v3/' + INFURA_KEY
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    contractAddr = "0xb18e018Af935F0b3a26AC8aE3eB4B1fc4d3624AB"
    contractAbi = "./abi/contract.abi"
    contract = get_contract(web3, contractAddr, contractAbi)
    contractOwner = contract.functions.owner().call()
    contractOwner_pk = MY_TESTMAIN_PK
    
    tokenContractAddr = "0xBafBe8Dc6b88868A7b58F6E5df89c3054dec93bB"
    tokenContractAbi = "./abi/token.abi"
    tokenContract = get_contract(web3, tokenContractAddr, tokenContractAbi)
    tokenOwner = tokenContract.functions.owner().call()
    tokenOwner_pk = MY_TESTMAIN_PK
    
    ETH_USD = coinbase_coin_spot_price("ETH","USD")
    
# transaction part
    # Buy script
    buyer = MY_TESTTEST
    buyer_pk = MY_TESTTEST_PK
    deposit_ETH = 1
    tokenAmount = int(deposit_ETH * float(ETH_USD['amount']) * 10)
    token_approve(web3, tokenContract, tokenOwner, tokenOwner_pk, contractAddr, tokenAmount)
    buy_token(web3, contract, buyer, buyer_pk, deposit_ETH, tokenAmount)
    
    # get contract total ETH
    contractBalance = get_contract_totalETH(contract)
    print(contractBalance)
    
    # withdraw contracts ETH to contractOwner
    withdrawETH(web3, contract, contractOwner, contractOwner_pk)
    
    