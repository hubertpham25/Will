from web3 import Web3

alchemyNodeURL = "https://eth-mainnet.g.alchemy.com/v2/jeCvmjj_CZDDvzJxXxyq_"
w3 = Web3(Web3.HTTPProvider(alchemyNodeURL))

address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
currentWeiBalance = w3.eth.get_balance(address)
currentEtherBalance = Web3.from_wei(currentWeiBalance, "ether")

def scoreCounter(walletAge, transactionCount, scamInteraction, noScamInteraction):
    score = 0
    if 1 <= walletAge <= 3:
        score += 10
    elif walletAge > 3:
        score += 20
    elif transactionCount > 100:
        score += 20
    elif scamInteraction == True:
        score -= 50
    elif noScamInteraction == True:
        score += 30
    return score