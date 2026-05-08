# Prompt工程进阶

## 核心概念

在 `BaseAgent` 类中添加系统提示词配置接口，实现灵活的提示词管理。

## 新增接口

### 1. set_system_prompt(prompt)
设置系统提示词，不会重置现有对话历史

```python
agent = FileAgent()
agent.set_system_prompt("你是一个专业的助手")
```

### 2. get_system_prompt()
获取当前系统提示词

```python
current_prompt = agent.get_system_prompt()
print(current_prompt)
```

### 3. update_system_prompt(new_prompt)
更新系统提示词，会重置对话历史

```python
agent.update_system_prompt("你是一个幽默的聊天机器人")
```

## 实现原理

```python
def set_system_prompt(self, prompt):
    self.system_prompt = prompt
    if self.system_prompt and not any(msg.get('role') == 'system' for msg in self.messages):
        self.messages.insert(0, {"role": "system", "content": self.system_prompt})
```

## 小结

今日在 `BaseAgent` 类中添加了三个提示词配置接口：
- `set_system_prompt()`: 追加方式设置提示词
- `get_system_prompt()`: 获取当前提示词
- `update_system_prompt()`: 更新并重置对话

这些接口使得 Agent 的行为可以灵活配置，为后续的 Prompt 工程进阶打下基础。

## 下一步

学习输出解析器（Output Parsers），让 LLM 输出结构化数据。