# LangChain学习日志

这是一个小白学习LangChain的学习日志，记录学习过程中的笔记、代码示例和心得体会。

## 📚 学习路径规划

| 天数 | 主题 | 核心内容 | 状态 |
|------|------|----------|------|
| **Day 1** | 模型配置 | OpenAI客户端配置、API调用、LLM无记忆特性 | ✅ 完成 |
| **Day 2** | 模型记忆 | 对话历史管理、上下文机制、遗忘机制（滑动窗口） | ✅ 完成 |
| **Day 3** | 工具调用 | Function Calling、工具注册与执行流程 | ✅ 完成 |
| **Day 4** | Agent初始化 | 代码模块化、BaseAgent类抽离 | ✅ 完成 |
| **Day 5** | Agent优化 | FileAgent子类、工具函数映射 | ✅ 完成 |
| **Day 6** | Prompt工程进阶 | 系统提示词配置接口、提示词管理 | ✅ 完成 |
| **Day 7** | 输出解析器 | StructuredOutputParser、Pydantic解析、JSON模式 | 🔄 进行中 |
| **Day 8** | LCEL基础 | 管道语法、RunnableParallel、错误处理 | 📋 待学习 |
| **Day 9** | Chains进阶 | SequentialChain、分支路由、条件链 | 📋 待学习 |
| **Day 10** | RAG入门 | Embeddings、向量数据库、文档加载 | 📋 待学习 |
| **Day 11** | RAG进阶 | 检索策略、文档分割、重排序 | 📋 待学习 |
| **Day 12** | LangGraph | 状态机、节点、条件边 | 📋 待学习 |
| **Day 13** | 多Agent协作 | AgentExecutor、工具共享、对话管理 | 📋 待学习 |
| **Day 14** | 高级工具 | 文件读写、API调用、计算器 | 📋 待学习 |
| **Day 15** | 部署与监控 | FastAPI封装、日志、性能监控 | 📋 待学习 |

## 🛠️ 技术栈

- **框架**: LangChain
- **模型**: OpenAI API (GPT-3.5/4)
- **语言**: Python 3.10+
- **依赖管理**: pip

## 📁 项目结构

```
LangChainLearning/
├── day1/           # 模型配置
├── day2/           # 模型记忆
├── day3/           # 工具调用
├── day4/           # Agent初始化
├── day5/           # Agent优化
├── day6/           # Prompt工程进阶
├── LangchainLearning/  # 额外示例代码
└── readme.md       # 项目说明
```

## 🚀 使用方法

```bash
# 进入对应天数的目录
cd day6

# 安装依赖
pip install -r requirement.txt

# 配置API密钥
cp configSample.json config.json
# 编辑 config.json，填入你的API密钥

# 运行代码
python main.py
```

## 📝 学习目标

1. ✅ 掌握LangChain核心概念
2. ✅ 实现带记忆的多轮聊天机器人
3. ✅ 实现工具调用能力
4. 📋 实现RAG知识库问答系统
5. 📋 构建可部署的AI应用

## 📌 重要提醒

API密钥是敏感信息，切勿暴露给他人。上传代码到GitHub等公共仓库时，务必删除或替换配置文件中的API密钥。建议使用环境变量来管理API密钥。