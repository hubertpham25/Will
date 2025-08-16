from web3 import Web3
from dotenv import load_dotenv
import os
import requests

load_dotenv()

alchemyNodeURL = "https://eth-mainnet.g.alchemy.com/v2/jeCvmjj_CZDDvzJxXxyq_"
etherscanKey = os.getenv("ETHERSCAN_API")
w3 = Web3(Web3.HTTPProvider(alchemyNodeURL))

address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

def getWalletBalance(address):
    currentWeiBalance = w3.eth.get_balance(address)
    currentEtherBalance = Web3.from_wei(currentWeiBalance, "ether")
    return currentEtherBalance

def getTransactions(address):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=asc&apikey={etherscanKey}"
    response = requests.get(url).json()
    
    totalTransactions = response["result"] #list of dictionaries for each transactions
    
    numOfTransactions = len(totalTransactions) #number of transactions on address
    
    