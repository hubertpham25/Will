import time, jsonify
from cryptoDataExtraction import cryptoDB

wallet_address_cache = dict()
sec_in_day = 86400
def calc_rep(urlPath):
    wallet_address = extract_wallet_address(urlPath)
    if wallet_address in wallet_address_cache:
        cached_score, timestamp = wallet_address_cache[wallet_address]

        # checks if the current time and the timestamp of the address is less than seconds in a day
        if time.time() - timestamp < sec_in_day:
            return jsonify({ 
                            "wallet address: ": wallet_address, 
                            "wallet reputation score: ": cached_score 
                        })
    
    # if not, it will get a new score for the day
    new_score = calc_new_rep(wallet_address)
    wallet_address_cache[wallet_address] = (new_score, time.time())
    return jsonify({
                    "wallet address": wallet_address,
                    "wallet reputation score": new_score
                   })

def extract_wallet_address(urlPath):
    # urlPath comes in as "/reputation/0x12a343...", 
    # strip removes "/reputation/", giving us the wallet address
    wallet_address = urlPath.strip("/reputation/")
    return wallet_address

def calc_new_rep(address):
    # dictionary from cde.py will return number of transactions, 
    # if the address has been apart of a scam, 
    # liquidation data which is another dictionary
    
    num_of_transaction = cryptoDB["Amounts of Transaction"]
    wallet_age = cryptoDB["Wallet Age"]
    rep_score = get_rep_score(num_of_transaction, address)

def get_rep_score(num_of_transaction, address):
    max_score = 300
    cached_score, timestamp = wallet_address_cache[address]
    rep_score = 0
    if cached_score != 0:
        rep_score = cached_score
    
    if num_of_transaction <= 20:
        rep_score += num_of_transaction*0.05
    
    elif 20 < num_of_transaction <= 100:
        rep_score += num_of_transaction*0.07

    elif 100 < num_of_transaction <= 500:
        rep_score += num_of_transaction*0.1
    
    elif num_of_transaction > 500 and rep_score < max_score:
        rep_score += num_of_transaction*0.12
    
    else: 
        rep_score = 300
        
    return rep_score

