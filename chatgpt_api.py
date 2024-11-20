import openai
import os
from Sdata import openapi
# 設定 OpenAI API 密鑰
openai.api_key = openapi

# 定義發送請求並獲取回應的函數
def chat_with_gpt(prompt):
    try:
        # 發送請求到 OpenAI API 並獲取回應
        response = openai.Completion.create(
            engine="text-davinci-003",  # 這裡指定使用 GPT-3 模型，或根據需要選擇 GPT-4
            prompt=prompt,
            max_tokens=150,  # 回應的最大長度
            n=1,             # 請求 1 個回應
            stop=None,       # 沒有自定義的停止詞
            temperature=0.7  # 控制回答的隨機性（0.0 到 1.0）
        )
        
        # 從回應中提取生成的文本並返回
        return response.choices[0].text.strip()
    
    except Exception as e:
        print(f"Error: {e}")
        return None

# 測試與 GPT 聊天
if __name__ == "__main__":
    prompt = "Hello, how are you today?"
    print("Prompt: ", prompt)
    
    result = chat_with_gpt(prompt)
    
    if result:
        print("ChatGPT Response: ", result)
