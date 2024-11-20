from IPython.display import clear_output,display, update_display
import time
import psycopg2
from psycopg2 import sql
from pybit.unified_trading import HTTP
from datetime import datetime, timezone
import sys
#sys.path.append('/home/kai')
from Sdata import bybitkey,bybit_Secret
import sys
import os
import django
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

symbol = "BTCUSDT"
#min_qty = 0.001  # 最小下單數量 根據交易對調整
print('init processing...')
#output = display("start trading...", display_id=True)


def update_strategy_info(strategy_name, current_position, profit_loss):
    StrategyInfo.objects.create(
        strategy_name=strategy_name,
        current_position=current_position,
        profit_loss=profit_loss
    )

# 資料庫連接參數
db_params = {
    "host": "123.241.217.251",
    "database": "mydatabase",
    "user": "myuser",
    "password": "mysecretpassword",
    "port": "5432"
}
trad_types = ['Buy','Sell']
# 連接資料庫
def connect_to_db():
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("連接資料庫時出錯:", error)
        return None

# 執行查詢
def execute_query(conn, query, params=None):
    try:
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("執行時出錯:", error)

symbol = "BTCUSDT"
min_qty = 0.001  # 最小下單數量
print('init processing...')
output = display("start trading...", display_id=True)

def close_all_position(trad_type):
    if trad_type == 'Buy':
        trad_type = 'Sell'
    else:
        trad_type = 'Buy'
    positions = session.get_positions(category="linear", symbol="BTCUSDT")
    response = session.place_order(
    category="linear",  # 或 "inverse"，根據合約類型設定
    symbol="BTCUSDT",
    side=trad_type,  # 平掉多單的方向為 "Sell"
    orderType="Market",
    qty=positions['result']['list'][0]['size'],
    reduceOnly=True,  # 設定為 True 確保這是一個平倉訂單
    timeInForce="GTC",  # Good Till Cancel
    positionIdx=0, #平掉多單是1 空單 2 單向持倉0
    )
    return response

def print_with_clear(message):
    clear_output(wait=True)
    print(message)


def place_order(side, qty):
    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty
        )
        return order
    except Exception as e:
        print(f"order fail: {e}")
        return None

def get_position():
    try:
        position = session.get_positions(category="linear", symbol=symbol)
        return position['result']['list'][0]
    except Exception as e:
        print(f"获取持仓信息失败: {e}")
        return None

def calculate_roi(position,trad_type):
    mode = 1
    if trad_type == 'Buy':
        mode = -1
    entry_price = float(position['avgPrice'])
    current_price = float(position['markPrice'])
    return (entry_price - current_price) / entry_price * 100 *mode #*-1代表作多

def trading_strategy(trad_type):
    while True:
        position = get_position()
        if position is None:
            continue

        size = float(position['size'])
        
        if size == 0:
            # if not order，start treading (small_order)
            place_order(trad_type, min_qty)
            input_db_trading_data()
        else:
            roi = calculate_roi(position,trad_type) * 100
            # update_display(f'ROI: {roi} % time=>{datetime.now()}', display_id=output.display_id)
            time.sleep(1)
            # ROI == +20% 平倉
            if roi >= 20:
                ans = close_all_position(trad_type)
                print('平倉',ans)
                time.sleep(13)
            elif roi <= -86:
                print(f'Order puls {trad_type}')
                place_order(trad_type, min_qty)
                input_db_trading_data()

                

def input_db_trading_data():
    conn = connect_to_db()
    positions = session.get_positions(category="linear", symbol="BTCUSDT")

    symbol= positions['result']['list'][0]['symbol']
    PositionIM= positions['result']['list'][0]['positionIM'] 
    Leverage= positions['result']['list'][0]['leverage']
    markPrice= positions['result']['list'][0]['markPrice'] 
    AvgPrice= positions['result']['list'][0]['avgPrice'] 
    Size= positions['result']['list'][0]['size']
    Side= positions['result']['list'][0]['side']
    CurRealisedPnl= positions['result']['list'][0]['curRealisedPnl'] 
    PositionValue= positions['result']['list'][0]['positionValue'] 
    createdTime= datetime.fromtimestamp(int(positions['result']['list'][0]['updatedTime']) / 1000, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
    Time= datetime.fromtimestamp(int(positions['time']) / 1000, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
    # 更新 Django 模型
    position = positions['result']['list'][0]
    StrategyInfo.objects.create(
        strategy_name=position['symbol'],
        current_position=float(position['size']),
        profit_loss=float(position['curRealisedPnl']),
        leverage=float(position['leverage']),
        mark_price=float(position['markPrice']),
        avg_price=float(position['avgPrice']),
        side=position['side'],
        position_value=float(position['positionValue']),
        created_time=datetime.fromtimestamp(int(position['updatedTime']) / 1000, timezone.utc),
        transaction_time=datetime.fromtimestamp(int(positions['time']) / 1000, timezone.utc)
    )
    if conn:
        insert_query = sql.SQL("""
        INSERT INTO sptd.tdata 
        (symbol, asset, leverage, buy_price, sell_price, quantity, transaction_type, CurRealisedPnl, PositionValue, create_transaction_time, transaction_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        
        params = (
            symbol, PositionIM, Leverage, markPrice, AvgPrice, Size, Side, 
            CurRealisedPnl, PositionValue, createdTime, Time
        )
        
        execute_query(conn, insert_query, params)

        conn.close()
def get_real_time_position():
    try:
        positions = session.get_positions(category="linear", symbol="BTCUSDT")
        position = positions['result']['list'][0]
        return {
            'symbol': position['symbol'],
            'size': float(position['size']),
            'side': position['side'],
            'entry_price': float(position['avgPrice']),
            'leverage': float(position['leverage']),
            'unrealised_pnl': float(position['unrealisedPnl']),
            'mark_price': float(position['markPrice'])
        }
    except Exception as e:
        print(f"獲取倉位信息失敗: {e}")
        return None 
if __name__ == "__main__":
    # 在您的策略代碼中適當的位置調用此函數
    update_strategy_info("My Strategy", 100.0, 50.0)
    trading_strategy(trad_types[1])
