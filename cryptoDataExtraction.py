#justin
from web3 import Web3
from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import requests


load_dotenv()

#alchemy and web3 initiation variables
alchemyNodeURL = "https://eth-mainnet.g.alchemy.com/v2/jeCvmjj_CZDDvzJxXxyq_"
w3 = Web3(Web3.HTTPProvider(alchemyNodeURL))

#etherscan initiation variables
etherscanKey = os.getenv("ETHERSCAN_API")

#list of scam addresses taken from CrytoScamDB
scamAddresses = {"0x08389B19ad52f0d983609ab785b3a43A0E90355F",
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
                 "0xe5b913f91f2b90c5cd04d711e1eb3214c56dba98"}

#convert to checksum address
def toCheckSum(address):
    return Web3.to_checksum_address(address)

#get current wallet balance 
def getWalletBalance(address):
    currentWeiBalance = w3.eth.get_balance(address)
    currentEtherBalance = Web3.from_wei(currentWeiBalance, "ether")
    return currentEtherBalance

#get total transactions - FIXED: now uses the address parameter properly
def getTransactions(address):
    etherscanURL = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=asc&apikey={etherscanKey}"
    response = requests.get(etherscanURL).json()
    
    totalTransactions = response["result"] #list of dictionaries for each transactions
    numOfTransactions = len(totalTransactions) #number of transactions on address
    return numOfTransactions

#scan for scam interactions
def scamInteraction(address, scamAddresses):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=asc&apikey={etherscanKey}"
    
    normalizedScamAddresses = {addr.lower() for addr in scamAddresses}
    
    response = requests.get(url)
    transactions = response.json().get("result", [])
    
    for transaction in transactions:
        toAddress = transaction["to"].lower() if transaction["to"] else "" #additional code added to to and from address to prevent error
        fromAddress = transaction["from"].lower() if transaction["from"] else ""
        
        if toAddress in normalizedScamAddresses or fromAddress in normalizedScamAddresses:
            return True
        
    return False

#check if wallet ever got liquidated
def gotLiquidated(address):
    
    lendingPoolAddress = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9" #smart contract address for Aave that holds all funds
    checkSummedPoolAddress = toCheckSum(lendingPoolAddress)
    
    #basic ABI for liquidationCalls
    lendingPoolABI = [
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "name": "collateralAsset", "type": "address"},
                {"indexed": True, "name": "debtAsset", "type": "address"},
                {"indexed": True, "name": "user", "type": "address"},
                {"indexed": False, "name": "debtToCover", "type": "uint256"},
                {"indexed": False, "name": "liquidatedCollateralAmount", "type": "uint256"},
                {"indexed": True, "name": "liquidator", "type": "address"},
                {"indexed": False, "name": "receiveAToken", "type": "bool"}
            ],
            "name": "LiquidationCall",
            "type": "event"
        }
    ]
    
    #create the lending pool contract
    lendingPool = w3.eth.contract(address=lendingPoolAddress, abi=lendingPoolABI)
    
    #checks for liquidation events from late 2021 to now
    
    from_block = 12000000
    to_block = w3.eth.block_number
    step = 10000
    allEvents = []
    
    while from_block <= to_block:
        end_block = min(from_block + step - 1, to_block)
        eventFilter = lendingPool.events.LiquidationCall.create_filter(
            from_block = from_block,
            to_block = end_block,
            argument_filters={"user": address}
        )
        events = eventFilter.get_all_entries()
        allEvents.extend(events)
        from_block = end_block + 1
    
    #if account has not been liquidated before
    if not allEvents:
        return {
            "liquidated": False,
            "count": 0,
            "lastLiquidation": None
        }
    
    #if account has been liquidated before, find last liquidation event
    lastEvent = allEvents[-1]
    blockNumber = lastEvent["blockNumber"]
    block = w3.eth.get_block(blockNumber)
    timestamp = datetime.fromtimestamp(block["timestamp"], tz = timezone.utc)
    
    return {
        "liquidated": True,
        "count": len(allEvents),
        "lastLiquidation": str(timestamp)
    }

# NEW FUNCTION - This is what you'll import and use in your code
def get_crypto_data(wallet_address):
    """Main function to get all crypto data for any wallet address"""
    checkedSumAddress = toCheckSum(wallet_address)
    
    cryptoDB = {
        "Wallet Balance": getWalletBalance(checkedSumAddress),
        "Liquidations": gotLiquidated(checkedSumAddress),
        "Scam Status": scamInteraction(checkedSumAddress, scamAddresses),
        "Amount of Transactions": getTransactions(checkedSumAddress),
    }
    
    return cryptoDB