import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def chat_example():
    """基本聊天示例"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请先设置 OPENAI_API_KEY 环境变量")
        return
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=api_key)
    
    messages = [
        SystemMessage(content="你是一个专业的 Python 编程助手"),
        HumanMessage(content="请解释什么是 Python 的装饰器")
    ]
    
    response = llm.invoke(messages)
    print("基本聊天示例:")
    print(response.content)
    print("-" * 50)

def prompt_template_example():
    """Prompt Template 示例"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请先设置 OPENAI_API_KEY 环境变量")
        return
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=api_key)
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个翻译助手"),
        ("human", "请将以下文本翻译成英文: {text}")
    ])
    
    # 创建链
    chain = prompt | llm | StrOutputParser()
    
    # 调用链
    result = chain.invoke({"text": "你好，世界！这是一个测试。"})
    print("Prompt Template 示例:")
    print(result)
    print("-" * 50)

def main():
    print("LangChain 高级示例")
    print("=" * 50)
    
    chat_example()
    prompt_template_example()

if __name__ == "__main__":
    main()
