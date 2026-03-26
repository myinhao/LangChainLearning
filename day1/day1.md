# 模型的配置
这里是所有LLM开发的第一步
## 配置模型信息
```python
client = OpenAI(
    api_key=config['api_key'],
    base_url=config['model_url']
)
```
## 调用模型
```python
response = client.chat.completions.create(
    model=config['model_type'],
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": user_input}
    ]
)

# 提取并打印回复
assistant_reply = response.choices[0].message.content
print(f"LLM: {assistant_reply}")
print("-" * 50)
```

# LLM本质是没有记忆能力的
参考coversation.txt 记录的内容，两次调用模型，模型都没有记住第一次调用的内容。
这个是很重要的一点，目前的LLM就是一个接口，一个黑匣子，只能接受文本的输入，只能返回文本的输出。
个人认为这其实是好事，因为相当于控制模型的已知信息。我可以优化掉不需要的记忆。这个在后面会提起。