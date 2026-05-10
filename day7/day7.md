# 输出解析器

## 核心概念

输出解析器（Output Parser）可以让 LLM 输出结构化的数据格式，如 JSON、XML、Pydantic 对象等，而不是纯文本。这使得程序能够更方便地处理和使用 LLM 的输出结果。

## 新增文件

### outputParser.py

创建了独立的解析器工厂类，支持三种解析器类型：

```python
class OutputParserFactory:
    @staticmethod
    def create_parser(parser_type='json', schema_type='analysis'):
        if parser_type == 'pydantic':
            if schema_type == 'weather':
                return PydanticOutputParser(pydantic_object=WeatherReport)
            else:
                return PydanticOutputParser(pydantic_object=AnalysisResult)
        elif parser_type == 'structured':
            response_schemas = [...]
            return StructuredOutputParser.from_response_schemas(response_schemas)
        else:
            return JsonOutputParser()
```

## Pydantic Schema 定义

```python
class WeatherReport(BaseModel):
    temperature: float = Field(description="当前温度，单位摄氏度")
    humidity: float = Field(description="湿度百分比，0-100")
    condition: str = Field(description="天气状况")
    wind_speed: float = Field(description="风速，单位km/h")

class AnalysisResult(BaseModel):
    answer: str = Field(description="问题的答案")
    confidence: float = Field(description="置信度，0-1之间")
    sources: list = Field(description="信息来源列表")
```

## 对 BaseAgent 的增量修改

### 新增属性
- `self.output_parser = None`

### 新增方法

1. **set_output_parser(parser)** - 设置输出解析器
2. **parse_output(text)** - 解析 LLM 输出
3. **chat_with_parse(user_input)** - 带解析的聊天方法
4. **run_parsed_chat_loop()** - 带解析输出的聊天循环

### 修改方法

- **chat()** - 在用户输入后追加解析器格式指令

## 使用示例

```python
from agentBaseInit import FileAgent
from outputParser import OutputParserFactory

agent = FileAgent()
parser = OutputParserFactory.create_parser('pydantic', 'weather')
agent.set_output_parser(parser)

result = agent.chat_with_parse("请分析北京今天的天气")
print(f"温度: {result.temperature}°C")
print(f"湿度: {result.humidity}%")
```

## 小结

今日新增内容：
- 创建了 `outputParser.py` 文件，包含解析器工厂和 Pydantic 模型定义
- 在 `BaseAgent` 类中添加了 4 个新方法：`set_output_parser()`, `parse_output()`, `chat_with_parse()`, `run_parsed_chat_loop()`
- 修改了 `chat()` 方法以支持解析器格式指令
- 更新了 `main.py` 添加解析器配置菜单

这些功能使得 LLM 输出可以被程序化处理，为后续的数据处理和业务逻辑集成打下基础。

## 下一步

学习 LCEL（LangChain Expression Language），掌握管道语法和并行执行。