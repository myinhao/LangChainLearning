from email import message
import json
import os
from openai import OpenAI
from datetime import datetime

# 加载配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 初始化OpenAI客户端
client = OpenAI(
    api_key=config['api_key'],
    base_url=config['model_url']
)
# 定义工具函数
def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_file(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败: {str(e)}"

def write_file(file_path, content):
    """写入内容到文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"成功写入文件: {file_path}"
    except Exception as e:
        return f"写入文件失败: {str(e)}"


# 注册工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取指定文件的内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件路径"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "将指定内容写入指定文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入的内容"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    }
]

# 工具函数映射
available_functions = {
    "get_current_time": get_current_time,
    "read_file": read_file,
    "write_file": write_file
}

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
                messages=main.messages,
                tools=tools,              # 注册工具
                tool_choice="auto"        # 自动选择工具
            )
            
            # 提取并打印回复
            assistant_reply = response.choices[0].message.content
            
            # 检查是否有工具调用
            if response.choices[0].message.tool_calls:
                tool_calls = response.choices[0].message.tool_calls
                print(f"工具调用: {tool_calls}")
                
                # 执行工具调用并收集结果
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # 执行函数
                    function_response = function_to_call(**function_args)
                    tool_results.append(function_response)
                
                # 将工具调用结果返回给用户
                for i, result in enumerate(tool_results):
                    print(f"工具执行结果 {i+1}: {result}")
                print("-" * 50)
                
                # 将工具调用结果作为用户消息添加到历史
                main.messages.append({
                    "role": "user",
                    "content": f"工具执行结果: {tool_results}"
                })
                
                # 再次调用LLM获取最终回复
                response = client.chat.completions.create(
                    model=config['model_type'],
                    messages=main.messages,
                    tools=tools,
                    tool_choice="auto"
                )
                assistant_reply = response.choices[0].message.content
            
            # 打印最终回复
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
