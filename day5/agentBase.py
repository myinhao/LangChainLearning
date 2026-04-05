import json
import os
from openai import OpenAI
from datetime import datetime

class BaseAgent:
    def __init__(self):
        # 获取当前文件所在目录
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, 'config.json')
        
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.config['api_key'],
            base_url=self.config['model_url']
        )
        
        # 初始化工具
        self.tools = self._register_tools()
        self.available_functions = self._get_function_mappings()
        
        # 初始化对话历史
        self.messages = []
    
    def _register_tools(self):
        """注册工具（子类可以重写）"""
        return []
    
    def _get_function_mappings(self):
        """获取工具函数映射（子类可以重写）"""
        return {}
    
    def chat(self, user_input):
        """执行对话逻辑"""
        try:
            # 将用户输入添加到历史记录
            self.messages.append({"role": "user", "content": user_input})
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.config['model_type'],
                messages=self.messages,
                tools=self.tools,              # 注册工具
                tool_choice="auto"        # 自动选择工具
            )
            
            # 提取回复
            assistant_reply = response.choices[0].message.content
            
            # 检查是否有工具调用
            if response.choices[0].message.tool_calls:
                tool_calls = response.choices[0].message.tool_calls
                print(f"工具调用: {tool_calls}")
                
                # 执行工具调用并收集结果
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # 执行函数
                    function_response = function_to_call(**function_args)
                    tool_results.append(function_response)
                
                # 将工具调用结果返回给用户
                for i, result in enumerate(tool_results):
                    print(f"工具执行结果 {i+1}: {result}")
                print("-" * 50)
                
                # 将工具调用结果作为用户消息添加到历史
                self.messages.append({
                    "role": "user",
                    "content": f"工具执行结果: {tool_results}"
                })
                
                # 再次调用LLM获取最终回复
                response = self.client.chat.completions.create(
                    model=self.config['model_type'],
                    messages=self.messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
                assistant_reply = response.choices[0].message.content
            
            # 滑动窗口：保留最近15条对话记录
            if len(self.messages) > 15:
                self.messages = self.messages[-15:]
            
            return assistant_reply
            
        except Exception as e:
            print(f"错误: {e}")
            print("-" * 50)
            return f"发生错误: {str(e)}"
    
    def chat_with_string(self, user_input):
        """带字符串参数的对话接口"""
        return self.chat(user_input)
    
    def clear_messages(self):
        """清空对话历史记录"""
        self.messages = []
    
    def run_chat_loop(self):
        """运行对话循环"""
        print("输入'退出'或'exit'结束对话")
        print("-" * 50)
        
        while True:
            # 读取用户输入
            user_input = input("你: ")
            
            # 检查是否退出
            if user_input.lower() in ['退出', 'exit']:
                print("再见！")
                break
            
            # 执行对话
            assistant_reply = self.chat(user_input)
            
            # 打印最终回复
            print(f"LLM: {assistant_reply}")
            print("-" * 50)