import os

from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
from dotenv import load_dotenv


def get_contract(web3, contractAddress, contractAbi):
    file = open(contractAbi, 'r', encoding='utf-8')
    contractAddr = web3.to_checksum_address(contractAddress)
    contract = web3.eth.contract(abi=file.read(), address=contractAddr)
    
    return contract

def token_approve(web3, contract, From, From_pk, To, tokenAmount):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = contract.functions.approve(To_add, tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return txHash, tx_receipt

def buy_token(web3, contract, From, From_pk, tokenAmount):
    From_add = web3.to_checksum_address(From)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = contract.functions.buyToken().build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price, "value": tokenAmount}
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

    network = "amoy"

    web3 = Web3(Web3.HTTPProvider('https://polygon-amoy.infura.io/v3/ce98e0c088a74995bc3fd43d52a81c39'))
    
    tokenContractAddr = "0xBafBe8Dc6b88868A7b58F6E5df89c3054dec93bB"
    tokenContractAbi = "./TGV.abi"
    tokenContract = get_contract(web3, tokenContractAddr, tokenContractAbi)
    
    contractAddr = "0x670a6EeBc4E9119B12cE69425dDC56c7B9930724"
    contractAbi = "./contract.abi"
    contract = get_contract(web3, contractAddr, contractAbi)
    
# transaction
    tokenOwner = '0x64a86158D40A628d626e6F6D4e707667048853eb'
    tokenOwner_pk = '0x119b1e18189153f894f5ccee62a23dac9233df290e159ed6b2d727bad19a142b'
    
    buyer = '0x2c18787A16E8Be7cF2cBCdC44AD97f616d1f7C0f'
    buyer_pk = '0x80fe9145298e6ac85a54331c9727aea41467aa996541fcb957829727ac6e1158'
    deposit_ETH = 1
    
    ETHAmount = deposit_ETH * 10**tokenContract.functions.decimals().call()
    print(ETHAmount)
    tokenAmount = ETHAmount * 100000
    print(tokenAmount)
    
    # token_approve(web3, tokenContract, tokenOwner, tokenOwner_pk, contractAddr, tokenAmount)
    
    # buy_token(web3, contract, buyer, buyer_pk, ETHAmount)
    
    withdrawETH(web3, contract, tokenOwner, tokenOwner_pk)
    
    
    