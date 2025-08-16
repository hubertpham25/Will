from web3 import Web3
from dotenv import load_dotenv
import os
import requests

load_dotenv()

alchemyNodeURL = "https://eth-mainnet.g.alchemy.com/v2/jeCvmjj_CZDDvzJxXxyq_"
etherscanKey = os.getenv("ETHERSCAN_API")
w3 = Web3(Web3.HTTPProvider(alchemyNodeURL))

address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

#list of scam addresses taken from CrytoScamDB
scamAddresses = ["0x08389B19ad52f0d983609ab785b3a43A0E90355F",
                 "0x7bb386c33486fe345168d0af94bef03897e16022",
                 "0xfa2e4bddb3899dFB0d91A70744739d9f76692755",
                 "0x5d82db63cf0c54d47006d416bdc7dab09ea2f3f1",
                 "0xA82C7c0Ef05080463E4ac55DB8b8531007f3A66C",
                 "0xdcd2fb1c1b103c5a591e76798704cfaa27baf6b9",
                 "0x5efb7d2ab258b18c8166b0c74fc4117716e52515",
                 "0x414bca672494b8f078112c52ae258f9e8de1a4a0",
                 "0x3dfE9F7Af8864DF0b7Cc2a20430006fd1af8dA1a",
                 "0x5B6D3d66E18Dfd31ed9A753C406963C401f356C0",
                 "0xc8c3234Aea55a5F746b2aE585a849ba0BFa57785",
                 "0x774148e22F021972bfe082e1548E5d9dC6e1D76E",
                 "0xeeCC46A74ceA6133a12672bD62D5167877B4d521",
                 "0xeeCC46A74ceA6133a12672bD62D5167877B4d521",
                 "0xe5b913f91f2b90c5cd04d711e1eb3214c56dba98"]

def getWalletBalance(address):
    currentWeiBalance = w3.eth.get_balance(address)
    currentEtherBalance = Web3.from_wei(currentWeiBalance, "ether")
    return currentEtherBalance

def getTransactions(address):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=asc&apikey={etherscanKey}"
    response = requests.get(url).json()
    
    totalTransactions = response["result"] #list of dictionaries for each transactions
    numOfTransactions = len(totalTransactions) #number of transactions on address
    
def scamInteraction(address):
    
    
    