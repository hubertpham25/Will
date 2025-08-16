import time, jsonify

wallet_address_cache = dict()
sec_in_day = 86400
def calc_reputation(urlPath):
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
                    "wallet adress: ": wallet_address,
                    "wallet reputation score: ": new_score
                   })

def extract_wallet_address(urlPath):
    # urlPath comes in as "/reputation/0x12a343...", 
    # strip removes "/reputation/", giving us the wallet address
    wallet_address = urlPath.strip("/reputation/")
    return wallet_address

def calc_new_rep(address):
    pass



