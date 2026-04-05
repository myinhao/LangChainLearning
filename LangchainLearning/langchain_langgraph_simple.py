import json
import os
import sys
import io
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# 设置标准输出为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_config():
    """从 day5/config.json 加载配置文件"""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'day5', 'config.json'))
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

class State(TypedDict):
    """定义图的状态"""
    input_text: str
    processed_text: str
    summary: str

def process_node(state: State, llm):
    """处理节点：分析输入文本"""
    print("=== Process Node 正在运行 ===")
    
    messages = [
        SystemMessage(content="你是一个文本分析助手。"),
        HumanMessage(content=f"请分析以下文本并给出关键点：\n{state['input_text']}")
    ]
    
    response = llm.invoke(messages)
    state['processed_text'] = response.content
    print(f"处理结果: {state['processed_text']}")
    
    return state

def summarize_node(state: State, llm):
    """总结节点：总结处理后的文本"""
    print("\n=== Summarize Node 正在运行 ===")
    
    messages = [
        SystemMessage(content="你是一个总结助手。"),
        HumanMessage(content=f"请总结以下内容：\n{state['processed_text']}")
    ]
    
    response = llm.invoke(messages)
    state['summary'] = response.content
    print(f"总结结果: {state['summary']}")
    
    return state

def main():
    # 加载配置文件
    config = load_config()
    
    # 获取配置信息
    api_key = config.get('api_key')
    model_url = config.get('model_url', 'https://api.openai.com/v1')
    model_type = config.get('model_type', 'gpt-3.5-turbo')
    
    # 检查 API 密钥
    if not api_key or api_key == 'your-api-key-here':
        print("提示: 请在 day5/config.json 中设置有效的 API 密钥")
        return
    
    # 初始化聊天模型
    temperature = 1 if model_type == 'kimi-k2.5' else 0.7
    llm = ChatOpenAI(
        model=model_type,
        temperature=temperature,
        api_key=api_key,
        base_url=model_url
    )
    
    # 创建图
    workflow = StateGraph(State)
    
    # 添加节点
    workflow.add_node("process", lambda state: process_node(state, llm))
    workflow.add_node("summarize", lambda state: summarize_node(state, llm))
    
    # 添加边
    workflow.set_entry_point("process")
    workflow.add_edge("process", "summarize")
    workflow.add_edge("summarize", END)
    
    # 编译图
    app = workflow.compile()
    
    # 运行图
    initial_state = {
        "input_text": "人工智能正在改变我们的生活方式。它在医疗、教育、金融等领域都有广泛应用。人工智能的发展也带来了一些挑战，比如就业问题和隐私保护。",
        "processed_text": "",
        "summary": ""
    }
    
    result = app.invoke(initial_state)
    print("\n=== 流程完成 ===")
    print(f"最终总结: {result['summary']}")

if __name__ == "__main__":
    main()
