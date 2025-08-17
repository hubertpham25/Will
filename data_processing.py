import time
from cryptoDataExtraction import get_crypto_data  # Fixed import

wallet_address_cache = dict()
sec_in_day = 86400

def calc_rep(wallet_address):  # Fixed parameter name
    if wallet_address in wallet_address_cache:
        cached_score, timestamp = wallet_address_cache[wallet_address]
        
        if time.time() - timestamp < sec_in_day:
            evaluation = get_evaluation(cached_score, 200)  # Fixed: define evaluation
            return { 
                "Wallet Address": wallet_address, 
                "Wallet Reputation Score": cached_score,
                "Safe Address": evaluation
            }
    
    # Calculate new score
    new_score = calc_new_rep(wallet_address)
    evaluation = get_evaluation(new_score, 200)
    
    wallet_address_cache[wallet_address] = (new_score, time.time())
    return {
        "wallet address": wallet_address,
        "wallet reputation score": new_score,
        "Safe Address": evaluation
    }

def get_evaluation(score, max_score):
    ratio = score / max_score
    if ratio < 0.2:
        return "Not reputable. User does not have enough transaction history."
    elif ratio < 0.6:
        return "Slightly reputable. User has enough transactions. However, still proceed with caution."
    else:
        return "Reputable. User has enough transactions. Still proceed with caution as always."

def calc_new_rep(address):
    # Get fresh data for this specific address
    crypto_data = get_crypto_data(address)  # Fixed: dynamic data
    
    num_of_transaction = crypto_data["Amount of Transactions"]
    rep_score = get_rep_score(num_of_transaction)  # Fixed: removed address param
    scam_status = crypto_data["Scam Status"]
    liquidated = crypto_data["Liquidations"]["liquidated"]

    if liquidated:
        rep_score *= 0.05
    if scam_status:
        rep_score *= 0.125

    return rep_score

def get_rep_score(num_of_transaction):  # Fixed: removed cache logic
    rep_score = 0
    
    if num_of_transaction <= 20:
        rep_score = num_of_transaction * 0.05
    elif num_of_transaction <= 100:
        rep_score = num_of_transaction * 0.07
    elif num_of_transaction <= 500:
        rep_score = num_of_transaction * 0.1
    else:
        rep_score = min(num_of_transaction * 0.12, 200)
    
    return rep_score