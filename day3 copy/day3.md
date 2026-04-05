# tools
OpenAI正式发布Function Calling。
LLM可以调用外部函数，比如读写文件、调用API等。
https://openai.com/index/function-calling-and-other-api-updates/

> July 20, 2023 update:
> 
> We previously communicated to developers that gpt-3.5-turbo-0301, gpt-4-0314 and gpt-4-32k-0314 models were scheduled for sunset on Sept 13, 2023. After reviewing feedback from customers and our community, we are extending support for those models until at least June 13, 2024.

# 小结
今天项目添加了工具调用，LLM终于有手和脚了hhh。
核心是配Json 加 函数调用的代码。
1、Agent告诉LLM，我有x个tool可以用。
2、LLM根据问题，调用对应的函数。
3、Agent执行完成后，告诉LLM。
4、LLM根据Agent的回复，继续调用其他函数。