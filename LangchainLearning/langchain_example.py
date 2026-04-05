import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def load_config():
    """从 day5/config.json 加载配置文件"""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'day5', 'config.json'))
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # 加载配置文件
    config = load_config()
    
    # 获取配置信息
    api_key = config.get('api_key')
    model_url = config.get('model_url', 'https://api.openai.com/v1')
    model_type = config.get('model_type', 'gpt-3.5-turbo')
    
    # 检查 API 密钥
    if not api_key or api_key == 'your-api-key-here':
        print("提示: 配置文件已成功加载！")
        print(f"当前 API 地址: {model_url}")
        print(f"当前模型类型: {model_type}")
        print(f"当前 API 密钥: {api_key}")
        print("\n请在 day5/config.json 中设置有效的 API 密钥以使用完整功能")
        print("示例: \"api_key\": \"sk-你的实际API密钥\"")
        return
    
    # 初始化聊天模型（支持 OpenAI 兼容的 API，如 Moonshot）
    # Moonshot 的 kimi-k2.5 模型只允许 temperature=1
    temperature = 1 if model_type == 'kimi-k2.5' else 0.7
    llm = ChatOpenAI(
        model=model_type,
        temperature=temperature,
        api_key=api_key,
        base_url=model_url
    )
    
    # 定义系统提示和用户消息
    messages = [
        SystemMessage(content="你是一个 helpful 的 AI 助手，回答用户的问题。"),
        HumanMessage(content="请介绍一下 LangChain 框架")
    ]
    
    # 调用模型生成回复
    response = llm.invoke(messages)
    
    # 打印结果
    print("AI 回复:")
    print(response.content)

if __name__ == "__main__":
    main()
