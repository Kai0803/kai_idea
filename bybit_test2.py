from IPython.display import clear_output,display, update_display
import time
from pybit.unified_trading import HTTP
from datetime import datetime, timezone
from Sdata import bybitkey,bybit_Secret
# init bybit session
session = HTTP(
    testnet=False,
    api_key=bybitkey,
    api_secret=bybit_Secret
)

symbol = "BTCUSDT"
min_qty = 0.001  # 最小下單數量 根據交易對調整
print('init processing...')
#output = display("start trading...", display_id=True)

def print_with_clear(message):
    clear_output(wait=True)
    print(message)

def close_all_position():
    positions = session.get_positions(category="linear", symbol="BTCUSDT")
    response = session.place_order(
    category="linear",  # 或 "inverse"，根據合約類型設定
    symbol="BTCUSDT",
    side="Sell",  # 平掉多單的方向為 "Sell"
    orderType="Market",
    qty=positions['result']['list'][0]['size'],
    reduceOnly=True,  # 設定為 True 確保這是一個平倉訂單
    timeInForce="GTC",  # Good Till Cancel
    positionIdx=1,
    )
    return response

def place_order(side, qty):
    try:
        position_idx = 1 if side == "Buy" else 2  #做多用 1 做空用 2
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            positionIdx=position_idx
        )
        print(f"下單成功: {side} {qty} {symbol}")
        return order
    except Exception as e:
        print(f"下單失敗: {e}")
        return None
def get_position():
    try:
        position = session.get_positions(category="linear", symbol=symbol)
        return position['result']['list'][0]
    except Exception as e:
        print(f"獲取持倉資訊失敗: {e}")
        return None

def calculate_roi(position):
    entry_price = float(position['avgPrice'])
    current_price = float(position['markPrice'])
    return (entry_price - current_price) / entry_price * 100 #*-1 #*-1代表作多

def trading_strategy():
    while True:
        position = get_position()
        if position is None:
            continue

        size = float(position['size'])
        
        if size == 0:
            # if not order，start treading (small_order)
            place_order("Sell", min_qty)
        else:
            roi = calculate_roi(position) * 100
            # print(f'ROI: {roi} %')
            # print_with_clear(f'ROI: {roi} %')
            #update_display(f'ROI: {roi} %', display_id=output.display_id)
            time.sleep(1)
            if roi >= 2000:
                # ROI == 20%，平倉重新開始
                # place_order("Buy", size)
                # print('Order Buy')
                # time.sleep(1)  # 等待 order 執行
                # place_order("Sell", min_qty)
                # print('Order Sell')
                ans = close_all_position()
                print('平倉',ans)
            elif roi <= -75:
                print('Order puls Sell')
                # ROI == -50%，加倉
                place_order("Sell", min_qty)
    
        # time.sleep(5)  # 每 5 秒更新 output

if __name__ == "__main__":
    trading_strategy()