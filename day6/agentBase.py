import json
import os
from openai import OpenAI
from datetime import datetime

class BaseAgent:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, 'config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.client = OpenAI(
            api_key=self.config['api_key'],
            base_url=self.config['model_url']
        )
        
        self.tools = self._register_tools()
        self.available_functions = self._get_function_mappings()
        
        self.messages = []
        self.system_prompt = None
    
    def _register_tools(self):
        return []
    
    def _get_function_mappings(self):
        return {}
    
    def set_system_prompt(self, prompt):
        """配置系统提示词"""
        self.system_prompt = prompt
        if self.system_prompt and not any(msg.get('role') == 'system' for msg in self.messages):
            self.messages.insert(0, {"role": "system", "content": self.system_prompt})
    
    def get_system_prompt(self):
        """获取当前系统提示词"""
        return self.system_prompt
    
    def update_system_prompt(self, new_prompt):
        """更新系统提示词（会重置对话历史）"""
        self.system_prompt = new_prompt
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})
    
    def chat(self, user_input):
        try:
            if self.system_prompt:
                has_system = any(msg.get('role') == 'system' for msg in self.messages)
                if not has_system:
                    self.messages.insert(0, {"role": "system", "content": self.system_prompt})
            
            self.messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model=self.config['model_type'],
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            assistant_reply = response.choices[0].message.content
            
            if response.choices[0].message.tool_calls:
                tool_calls = response.choices[0].message.tool_calls
                print(f"工具调用: {tool_calls}")
                
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(**function_args)
                    tool_results.append(function_response)
                
                for i, result in enumerate(tool_results):
                    print(f"工具执行结果 {i+1}: {result}")
                print("-" * 50)
                
                self.messages.append({
                    "role": "user",
                    "content": f"工具执行结果: {tool_results}"
                })
                
                response = self.client.chat.completions.create(
                    model=self.config['model_type'],
                    messages=self.messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
                assistant_reply = response.choices[0].message.content
            
            if len(self.messages) > 15:
                self.messages = self.messages[-15:]
            
            return assistant_reply
            
        except Exception as e:
            print(f"错误: {e}")
            print("-" * 50)
            return f"发生错误: {str(e)}"
    
    def chat_with_string(self, user_input):
        return self.chat(user_input)
    
    def clear_messages(self):
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})
    
    def run_chat_loop(self):
        print("输入'退出'或'exit'结束对话")
        print("-" * 50)
        
        while True:
            user_input = input("你: ")
            
            if user_input.lower() in ['退出', 'exit']:
                print("再见！")
                break
            
            assistant_reply = self.chat(user_input)
            print(f"LLM: {assistant_reply}")
            print("-" * 50)