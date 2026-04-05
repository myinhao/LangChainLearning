import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def load_config():
    """从 day5/config.json 加载配置文件"""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'day5', 'config.json'))
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

class WriterAgent:
    """写文件的 Agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def write_file(self, file_path, content):
        """写入文件内容"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"成功写入文件: {file_path}"
        except Exception as e:
            return f"写入文件失败: {str(e)}"
    
    def generate_content(self, topic):
        """生成内容"""
        messages = [
            SystemMessage(content="你是一个专业的内容创作者，撰写简洁的文章。"),
            HumanMessage(content=f"请写一篇关于 '{topic}' 的简短文章，约200字。")
        ]
        
        response = self.llm.invoke(messages)
        return response.content

class ReviewerAgent:
    """审查文件的 Agent"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def read_file(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"
    
    def review_content(self, content):
        """审查内容"""
        messages = [
            SystemMessage(content="你是一个内容审查员，提供简要的评估。"),
            HumanMessage(content=f"请简要评估以下内容，指出优点和改进建议：\n\n{content}")
        ]
        
        response = self.llm.invoke(messages)
        return response.content

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
    writer = WriterAgent(llm)
    reviewer = ReviewerAgent(llm)
    
    # 示例主题
    topic = "人工智能的未来发展"
    file_path = f"{topic.replace(' ', '_')}.md"
    
    print("=== Writer Agent 正在生成内容 ===")
    content = writer.generate_content(topic)
    print("生成的内容:")
    print(content)
    
    print("\n=== Writer Agent 正在写入文件 ===")
    result = writer.write_file(file_path, content)
    print(result)
    
    print("\n=== Reviewer Agent 正在审查文件 ===")
    file_content = reviewer.read_file(file_path)
    review = reviewer.review_content(file_content)
    print("\n审查意见:")
    print(review)

if __name__ == "__main__":
    main()
