import requests

def get_contracts():
    contracts =  []

    res = requests.get("https://www.bitmex.com/api/v1/instrument/active")

    for contract in res.json():
        contracts.append(contract["symbol"])
        
    return contracts        