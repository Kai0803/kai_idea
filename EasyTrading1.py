import requests
import hmac
import hashlib
import time
import Sdata
API_KEY = Sdata.API_KEY 
SECRET = Sdata.SECRET

def get_account_info():
    timestamp = str(int(time.time() * 1000))
    message = timestamp + 'GET' + '/api/v1/account/balances'
    signature = hmac.new(SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

    headers = {
        'X-MBX-APIKEY': API_KEY,
        'X-MBX-SIGNATURE': signature
    }

    response = requests.get('https://api.pionex.com', headers=headers, params={'timestamp': timestamp})
    return response.json()

account_info = get_account_info()
print(account_info)


# # 設定初始參數
# initial_position_value = 1000  # 初始倉位市值
# current_position_value = initial_position_value  # 當前倉位市值
# fixed_additional_amount = 500  # 加倉固定額度
# profit_target = 1.2 * initial_position_value  # 目標利潤 (20%增加)
# loss_threshold = 0.5 * initial_position_value  # 當前市值 = 50% 初始值

# # 模擬價格波動
# price_changes = [...]

# for price in price_changes:
#     current_position_value *= price
    
#     # 檢查是否達到目標利潤
#     if current_position_value >= profit_target:
#         print(f"利潤達到20%，賣出，結束交易。")
#         break
    
#     # 檢查是否達到虧損100%
#     elif current_position_value <= loss_threshold:
#         print(f"虧損100%，加倉固定額度。")
#         current_position_value += fixed_additional_amount
#         # 更新虧損閾值以反映加倉後的情況
#         loss_threshold = (current_position_value / 2)
