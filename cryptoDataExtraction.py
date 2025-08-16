from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv

alchemyNodeURL = "https://eth-mainnet.g.alchemy.com/v2/jeCvmjj_CZDDvzJxXxyq_"
etherscankey = os.getenv("ETHERSCAN_API")
w3 = Web3(Web3.HTTPProvider(alchemyNodeURL))
print(etherscankey)

address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

def getWalletBalance(address):
    currentWeiBalance = w3.eth.get_balance(address)
    currentEtherBalance = Web3.from_wei(currentWeiBalance, "ether")
    return currentEtherBalance

def getTransactions(address):
    return None