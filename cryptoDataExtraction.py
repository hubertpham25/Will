from web3 import Web3

alchemyNodeURL = "https://eth-mainnet.g.alchemy.com/v2/jeCvmjj_CZDDvzJxXxyq_"
w3 = Web3(Web3.HTTPProvider(alchemyNodeURL))

address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
currentWeiBalance = w3.eth.get_balance(address)
currentEtherBalance = Web3.from_wei(currentWeiBalance, "ether")

print(f'Current balance is {currentEtherBalance}')