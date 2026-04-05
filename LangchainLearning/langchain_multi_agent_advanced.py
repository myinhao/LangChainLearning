import json
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.openai_tools import create_openai_tools_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate

def load_config():
    """从 day5/config.json 加载配置文件"""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'day5', 'config.json'))
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@tool
def write_file(file_path: str, content: str) -> str:
    """写入内容到指定文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"成功写入文件: {file_path}"
    except Exception as e:
        return f"写入文件失败: {str(e)}"

@tool
def read_file(file_path: str) -> str:
    """读取指定文件的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败: {str(e)}"

def create_writer_agent(llm):
    """创建写文件的 Agent"""
    tools = [write_file]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的内容创作者，负责生成内容并写入文件。"),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}")
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def create_reviewer_agent(llm):
    """创建审查文件的 Agent"""
    tools = [read_file]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的内容审查员，负责审查文件内容并提供评估。"),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}")
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

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
    
    # 创建 Agent
    writer_agent = create_writer_agent(llm)
    reviewer_agent = create_reviewer_agent(llm)
    
    # 任务流程
    topic = "人工智能的未来发展"
    file_path = f"{topic.replace(' ', '_')}.md"
    
    print("=== Writer Agent 正在工作 ===")
    writer_input = f"请写一篇关于 '{topic}' 的简短文章（约200字），并将内容写入文件 '{file_path}'"
    writer_result = writer_agent.invoke({"input": writer_input})
    print(f"\nWriter Agent 结果: {writer_result['output']}")
    
    print("\n=== Reviewer Agent 正在工作 ===")
    reviewer_input = f"请审查文件 '{file_path}' 的内容，提供详细的评估和改进建议"
    reviewer_result = reviewer_agent.invoke({"input": reviewer_input})
    print(f"\nReviewer Agent 结果: {reviewer_result['output']}")

if __name__ == "__main__":
    main()
