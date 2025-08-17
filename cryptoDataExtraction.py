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
address = "0xA97b29B1ee80ED31eB9977E1B3fcda4a803A65f9"
etherscanURL = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=asc&apikey={etherscanKey}"

#graph initiation variables
graphKey = os.getenv("GRAPH_API_KEY")
graphURL = f"https://gateway.thegraph.com/api/{graphKey}/subgraphs/id/C2zniPn45RnLDGzVeGZCx2Sw3GXrbc9gL4ZfL8B8Em2j"

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

#get total transactions
def getTransactions(address):
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
    
    query = """
    query($user: String!) {
      liquidations(where: {user: $user}, orderBy: timestamp, orderDirection: desc) {
        id
        user
        collateralAsset
        debtAsset
        liquidator
        debtToCover
        liquidatedCollateralAmount
        timestamp
      }
    }
    """
    
    variables = {"user": address.lower()}
    
    response = requests.post(graphURL, json={"query": query, "variables": variables})
    #checks for liquidation events from late 2021 to now
    
    liquidations = response.json()["data"]["liquidations"]
    
    #if account has not been liquidated before
    if not liquidations:
        return {
            "liquidated": False,
            "count": 0,
            "lastLiquidation": None
        }
    
    #if account has been liquidated before, find last liquidation event
    lastLiquidation = liquidations[0]
    lastLiquidationTime = datetime.fromtimestamp(
        int(lastLiquidation["timestamp"]), tz=timezone.utc
    )
    
    return {
        "liquidated": True,
        "count": len(liquidations),
        "lastLiquidation": str(lastLiquidationTime)
    }

checkedSumAddress = toCheckSum(address)
print(gotLiquidated(checkedSumAddress))