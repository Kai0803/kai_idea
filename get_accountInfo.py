from datetime import datetime, timedelta,timezone
from IPython.display import clear_output,display, update_display
import time
import psycopg2
from psycopg2 import sql
from pybit.unified_trading import HTTP
from datetime import datetime, timezone
import sys
#sys.path.append('/home/kai')
from Sdata import bybitkey,bybit_Secret
import os
import django
import code
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kai_idea.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()
from trading_api.models import StrategyInfo
#visit to http://localhost:8000/api/strategy-info/


# init bybit session
session = HTTP(
    testnet=False,
    api_key=bybitkey,
    api_secret=bybit_Secret
)

def get_account_info():
    # 獲取帳戶餘額
    try:
        balance = session.get_wallet_balance(accountType="UNIFIED")
        print(f"Account Balance: {balance['result']['list'][0]['totalEquity']} USDT")
    except Exception as e:
        print(f"Get Account Balance Error: {e}")

def get_position_info():
    # 獲取持倉資訊
    try:
        positions = session.get_positions(category="linear", symbol="ETHUSDT")

        print(f"Symbol: {positions['result']['list'][0]['symbol']}")
        print(f"PositionIM: {positions['result']['list'][0]['positionIM']} USDT")
        print(f"Leverage: {positions['result']['list'][0]['leverage']} X")
        print(f"Mark Price: {positions['result']['list'][0]['markPrice']} USDT")
        print(f"Avg Price: {positions['result']['list'][0]['avgPrice']} USDT")
        print(f"Size: {positions['result']['list'][0]['size']} ETH")
        print(f"Side: {positions['result']['list'][0]['side']}")
        print(f"CurRealisedPnl: {positions['result']['list'][0]['curRealisedPnl']} USDT")
        print(f"Position Value: {positions['result']['list'][0]['positionValue']} USDT")
        print(f"Created Time: {datetime.fromtimestamp(int(positions['result']['list'][0]['updatedTime']) / 1000, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Time: {datetime.fromtimestamp(int(positions['time']) / 1000, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"Get Contract Info Error: {e}")
def get_history_info():
    # 獲取今天的 UTC 起始和結束時間戳
    def get_today_timestamps():
        now = datetime.now(timezone.utc)
        day_choice = input("please enter a day to visit history: ")
        match day_choice:
            case 'today':
                today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
            case 'yesterday':
                today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc) - timedelta(days = 1)
            case 'user':
                day_input = input("please input datetime(format:%y-%m-%d): ")
                date_obj = datetime.strptime(day_input, "%Y%m%d")
                # 格式化為 'YYYY-MM-DD'
                formatted_date = date_obj.strftime("%Y-%m-%d")
                date_combine = f'{formatted_date} 00:00:00+00:00'
                date_format = "%Y-%m-%d %H:%M:%S%z"  # 時區部分使用 %z 來解析
                today_start = datetime.strptime(date_combine, date_format)
            case _:
                today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
                #print(today_start,yesterday_start)
        today_end = today_start + timedelta(days=1) - timedelta(seconds=1)
        return int(today_start.timestamp() * 1000), int(today_end.timestamp() * 1000)

    start_time, end_time = get_today_timestamps()

    # 查詢今天的訂單
    try:
        cursor = None
        today_orders = []

        while True:
            # 獲取訂單記錄（帶時間範圍過濾）
            response = session.get_order_history(
                category="linear", 
                symbol="ETHUSDT", 
                startTime=start_time, 
                endTime=end_time, 
                cursor=cursor
            )
            orders = response['result']['list']
            today_orders.extend(orders)

            # 如果有下一頁，繼續查詢
            cursor = response['result'].get('nextPageCursor')
            if not cursor:
                break

        # 處理今天的訂單
        print(f"今天的訂單數量: {len(today_orders)}")
        total_pnl = 0
        earn_num = 0 #紀錄一天結單筆數
        for order in today_orders:
            if order['orderStatus'] == "Filled" and order['side'] == "Sell":  # 篩選已完成訂單
                #pnl = float(order['cumExecValue']) - (float(order['cumExecFee'])*2) 
                #pnl =  (float(order['cumExecValue']) * 0.2 * float(order['cumExecQty'])) - (float(order['cumExecFee']) *2 )
                pnl =  (float(order['cumExecValue']) * 0.2 /100 ) - (float(order['cumExecFee']) *2 )
                total_pnl += (pnl)
                temp = int(int(order['updatedTime']) / 1000)
                print(f"訂單ID: {order['orderId']}, 實現盈虧: {pnl}, 更新時間: {datetime.fromtimestamp(temp)}")
                earn_num += 1
                #code.interact(local=locals())
                #break
        print(f"今天總盈虧: {total_pnl}")
        print(f"今天總結單數: {earn_num}")
        # (float(order['price']) - float(order['avgPrice']))
    except Exception as e:
        print(f"查詢今天訂單時出錯: {e}")
choice = input('please enter 1 to show account_info\n       enter 2 to show position_info\n       enter 3 to show order_history: ')
print('-'*13)
match choice:
    case '1':
        get_account_info()
    case '2':
        get_position_info()
    case '3':
        get_history_info()
    case _:
        print('error_input')
print('-'*13)
#code.interact(local=locals())
