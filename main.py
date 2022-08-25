import requests
import time
import json
import threading

config = open("config.json", "r")
config = json.load(config)

cookie = config["cookie"]

itemIds = config["itemIDsToSnipe"]
pricesToBuy = config["pricesToBuyIDsAtInSameOrder"]

productIds = []

proxies = {
    "http": config["rotatingProxyURL"],
    "https": config["rotatingProxyURL"]
}

authurl = "https://auth.roblox.com/v2/logout"
def getXsrf():
    xsrfRequest = requests.post(authurl, cookies={
        '.ROBLOSECURITY': cookie
    })
    try:
        return xsrfRequest.headers["x-csrf-token"]
    except:
        return -1

xsrfToken = getXsrf()

def getProductId(itemId):
    url = "https://api.roblox.com/Marketplace/ProductInfo?assetId=" + str(itemId)
    r = requests.get(url)
    r = r.json()
    productId = r["ProductId"]
    return productId

for item in itemIds:
    productIds.append([str(item), getProductId(item)])


def purchaseItem(uaid, bestPrice, productId, sellerId):
    headers = {
        'x-csrf-token': xsrfToken,
        'content-type': 'application/json; charset=UTF-8' }
    data = {
        'expectedSellerId': int(sellerId),
        'expectedCurrency': 1,
        'expectedPrice': int(bestPrice),
        'userAssetId': int(uaid) }
    cookies = {
        '.ROBLOSECURITY': cookie }
    dataLoad = json.dumps(data)
    buyres = requests.post('https://economy.roblox.com/v1/purchases/product/' + str(productId), headers = headers, data = dataLoad, cookies = cookies)
    buyresData = buyres.json()
    if buyresData['purchased'] == True:
        print('Succesfully purchased the item ' + str(id) + ' at a price of ' + str(bestPrice))
        return True
    else:
        print('lol your vps/proxies arent fast enough LLLLL')
        return False

def checkItem(itemIdPos):
    url = "https://economy.roblox.com/v1/assets/" + str(productIds[itemIdPos][0]) + "/resellers"
    headers = {"x-csrf-token": xsrfToken}
    cookies = {".ROBLOSECURITY": cookie}
    while True:
        try:
            r = requests.get(url, headers = headers, cookies = cookies, proxies = proxies)
        except:
            checkItem(itemIdPos)
        data = r.json()
        price = data["data"][0]["price"]
        uaid = data["data"][0]["userAssetId"]
        sellerId = data["data"][0]["seller"]["id"]

        if price <= pricesToBuy[itemIdPos]:
            purchaseItem(uaid, price, productIds[itemIdPos][1], sellerId)
    

    

#Below is actually running the program


for index in range(len(productIds)):
    thread = threading.Thread(target = checkItem, args = [index])
    thread.start()

print("started sniping")

while True:
    time.sleep(1680)
    xsrfToken = getXsrf()


