from datetime import datetime

day_d = (datetime.now() - datetime.fromtimestamp(1550868242)).total_seconds() / 86400
today = datetime.today()
start = datetime(today.year, today.month, today.day + 1, 0, 0)
print(start)
