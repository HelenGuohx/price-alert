from dotenv import load_dotenv

load_dotenv()


from models import Alert

alerts = Alert.all()
for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()

if not alerts:
    print("No alerts have been created. Add an item and an alert to begin!")