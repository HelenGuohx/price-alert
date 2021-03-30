from dotenv import load_dotenv

load_dotenv()


from models.store import Store
from models.alert import Alert
from models.item import Item

stores = [
    # ["ebay", "https://www.ebay.com", "span", {"id": "prcIsum"}],
    ["target", "https://www.target.com", "div", {"data-test": "product-price"}],
    # ["walmart", "https://www.walmart.com", "span", {"class": "price-characteristic"}]
    ]

walmart_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Sec-WebSocket-Version": "13",
    "Origin": "https://www.walmart.com",
    "Sec-WebSocket-Extensions": "permessage-deflate",
    "Sec-WebSocket-Key": "MW7/zV09JfaRpM+jEHrdBA==",
    "Connection": "keep-alive, Upgrade",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade": "websocket",
}

# for store in stores:
#     Store(*store).save_to_mongo()



alert_name = "airpod"
# item_url = "https://www.walmart.com/ip/Apple-AirPods-with-Charging-Case-Latest-Model/604342441?wmlspartner=wlpa&selectedSellerId=18439&&adid=22222222227281354149&wl0=&wl1=g&wl2=c&wl3=339987579106&wl4=pla-667825192756&wl5=9029805&wl6=&wl7=&wl8=&wl9=pla&wl10=125198988&wl11=online&wl12=604342441&veh=sem&gclid=Cj0KCQjwjPaCBhDkARIsAISZN7TbRgYfETgVQDJA2fFltLwD2Rh717oo-AAoRTCcD18KBbVQVes0vqMaAibKEALw_wcB&gclsrc=aw.ds"
# item_url = "https://www.target.com/p/apple-ipad-pro-12-9-inch-wi-fi-only-2020-model/-/A-79767127?preselect=77616896#lnk=sametab"
item_url = "https://www.bestbuy.com/site/ultimate-ears-megaboom-3-portable-bluetooth-speaker-night-black/6288538.p?skuId=6288538"
price_limit = float("100")

store = Store.find_by_url(item_url)
item = Item(item_url, store.tag_name, store.query)
item.load_price()
item.save_to_mongo()
Alert(alert_name, item._id, price_limit).save_to_mongo()
