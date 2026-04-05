import json
import os
from openai import OpenAI

# 加载配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 初始化OpenAI客户端
client = OpenAI(
    api_key=config['api_key'],
    base_url=config['model_url']
)

def main():
    print("输入'退出'或'exit'结束对话")
    print("-" * 50)
    
    while True:
        # 读取用户输入
        user_input = input("你: ")
        
        # 检查是否退出
        if user_input.lower() in ['退出', 'exit']:
            print("再见！")
            break
        
        try:
            # 初始化历史对话记录（在函数开头添加）
            if 'messages' not in main.__dict__:
                main.messages = []
            
            # 将用户输入添加到历史记录
            main.messages.append({"role": "user", "content": user_input})
            
            # 调用OpenAI API
            response = client.chat.completions.create(
                model=config['model_type'],
                messages=main.messages
            )
            
            # 提取并打印回复
            assistant_reply = response.choices[0].message.content
            print(f"LLM: {assistant_reply}")
            print("-" * 50)
            
            # 将助手回复添加到历史记录，不把LLM的回复直接加入记忆中，因为浪费token。
            # main.messages.append({"role": "assistant", "content": assistant_reply})
            
            # 滑动窗口：保留最近15条对话记录
            if len(main.messages) > 15:
                main.messages = main.messages[-15:]
            
        except Exception as e:
            print(f"错误: {e}")
            print("-" * 50)

if __name__ == "__main__":
    main()