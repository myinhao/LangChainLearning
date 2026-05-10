from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

class WeatherReport(BaseModel):
    temperature: float = Field(description="当前温度，单位摄氏度")
    humidity: float = Field(description="湿度百分比，0-100")
    condition: str = Field(description="天气状况，如晴天、多云、雨天等")
    wind_speed: float = Field(description="风速，单位km/h")

class AnalysisResult(BaseModel):
    answer: str = Field(description="问题的答案")
    confidence: float = Field(description="置信度，0-1之间")
    sources: list = Field(description="信息来源列表")

class OutputParserFactory:
    @staticmethod
    def create_parser(parser_type='json', schema_type='analysis'):
        if parser_type == 'pydantic':
            if schema_type == 'weather':
                return PydanticOutputParser(pydantic_object=WeatherReport)
            else:
                return PydanticOutputParser(pydantic_object=AnalysisResult)
        else:
            return JsonOutputParser()