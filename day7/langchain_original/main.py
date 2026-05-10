from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from pydantic import BaseModel, Field
import json
import os

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

api_key = config.get('api_key')
base_url = config.get('model_url')

class AnalysisResult(BaseModel):
    answer: str = Field(description="问题的答案")
    confidence: float = Field(description="置信度，0-1之间")
    steps: list = Field(description="思考步骤列表")

class WeatherReport(BaseModel):
    temperature: float = Field(description="当前温度，单位摄氏度")
    humidity: float = Field(description="湿度百分比，0-100")
    condition: str = Field(description="天气状况")
    recommendation: str = Field(description="出行建议")

pydantic_parser = PydanticOutputParser(pydantic_object=AnalysisResult)
json_parser = JsonOutputParser()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=api_key,
    base_url=base_url,
    temperature=0
)

def demo_output_parsers():
    print("\n=== LangChain 输出解析器演示 ===")
    
    print("\n1. Pydantic 解析器演示：")
    format_instructions = pydantic_parser.get_format_instructions()
    structured_prompt = ChatPromptTemplate.from_template(
        "请按照以下格式输出：\n{format_instructions}\n\n问题：{question}"
    )
    
    chain = structured_prompt | llm | pydantic_parser
    result = chain.invoke({
        "format_instructions": format_instructions,
        "question": "分析一下：人工智能的发展趋势是什么？"
    })
    
    print("Pydantic 解析结果（结构化对象）：")
    print(f"类型: {type(result)}")
    print(f"答案: {result.answer}")
    print(f"置信度: {result.confidence}")
    print(f"思考步骤: {result.steps}")
    
    print("\n2. JSON 解析器演示：")
    json_prompt = ChatPromptTemplate.from_template(
        "请以JSON格式输出天气信息，包含temperature, humidity, condition, recommendation字段。问题：{question}"
    )
    
    json_chain = json_prompt | llm | json_parser
    json_result = json_chain.invoke({
        "question": "描述北京今天的天气"
    })
    print(f"JSON 解析结果: {json_result}")
    print(f"类型: {type(json_result)}")

demo_output_parsers()