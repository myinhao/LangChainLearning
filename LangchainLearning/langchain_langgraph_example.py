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
    topic: str
    content: str
    file_path: str
    review: str
    agent: str

def writer_agent(state: State, llm):
    """写文件的 Agent"""
    print("=== Writer Agent 正在生成内容 ===")
    
    # 生成内容
    messages = [
        SystemMessage(content="你是一个专业的内容创作者，擅长撰写各种主题的文章。"),
        HumanMessage(content=f"请写一篇关于 '{state['topic']}' 的简短文章，约200字。")
    ]
    
    response = llm.invoke(messages)
    state['content'] = response.content
    print("生成的内容:")
    print(state['content'])
    
    # 写入文件
    state['file_path'] = f"{state['topic'].replace(' ', '_')}.md"
    try:
        with open(state['file_path'], 'w', encoding='utf-8') as f:
            f.write(state['content'])
        print(f"\n成功写入文件: {state['file_path']}")
    except Exception as e:
        print(f"\n写入文件失败: {str(e)}")
    
    state['agent'] = "writer"
    return state

def reviewer_agent(state: State, llm):
    """审查文件的 Agent"""
    print("\n=== Reviewer Agent 正在审查文件 ===")
    
    # 读取文件内容
    try:
        with open(state['file_path'], 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        print(f"读取文件失败: {str(e)}")
        state['review'] = f"读取文件失败: {str(e)}"
        state['agent'] = "reviewer"
        return state
    
    # 审查内容
    messages = [
        SystemMessage(content="你是一个专业的内容审查员，擅长评估文章的质量、结构、语法和逻辑。"),
        HumanMessage(content=f"请审查以下内容，提供详细的评估和改进建议：\n\n{file_content}")
    ]
    
    response = llm.invoke(messages)
    state['review'] = response.content
    print("\n审查意见:")
    print(state['review'])
    
    state['agent'] = "reviewer"
    return state

def should_continue(state: State):
    """决定是否继续流程"""
    if state['agent'] == "writer":
        return "review"
    else:
        return END

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
    workflow.add_node("write", lambda state: writer_agent(state, llm))
    workflow.add_node("review", lambda state: reviewer_agent(state, llm))
    
    # 添加边
    workflow.set_entry_point("write")
    workflow.add_conditional_edges(
        "write",
        should_continue,
        {"review": "review", END: END}
    )
    workflow.add_conditional_edges(
        "review",
        should_continue,
        {END: END}
    )
    
    # 编译图
    app = workflow.compile()
    
    # 运行图
    initial_state = {
        "topic": "人工智能的未来发展",
        "content": "",
        "file_path": "",
        "review": "",
        "agent": ""
    }
    
    result = app.invoke(initial_state)
    print("\n=== 流程完成 ===")
    print(f"主题: {result['topic']}")
    print(f"文件: {result['file_path']}")
    print("审查完成")

if __name__ == "__main__":
    main()
