from agentBaseInit import FileAgent
from outputParser import OutputParserFactory

def main():
    print("Day 7 - 输出解析器")
    print("=" * 50)
    
    agent = FileAgent()
    
    while True:
        print("\n请选择操作：")
        print("1. 设置系统提示词")
        print("2. 获取当前提示词")
        print("3. 更新提示词（重置对话）")
        print("4. 设置输出解析器")
        print("5. 启动聊天模式")
        print("6. 启动结构化输出模式")
        print("7. 退出")
        
        choice = input("输入选择(1-7): ")
        
        if choice == "1":
            prompt = input("请输入系统提示词: ")
            agent.set_system_prompt(prompt)
            print("系统提示词已设置")
        elif choice == "2":
            current = agent.get_system_prompt()
            print(f"当前系统提示词: {current if current else '未设置'}")
        elif choice == "3":
            prompt = input("请输入新的系统提示词: ")
            agent.update_system_prompt(prompt)
            print("系统提示词已更新，对话历史已重置")
        elif choice == "4":
            print("\n选择解析器类型：")
            print("a. json - 简单JSON解析")
            print("b. pydantic - Pydantic对象解析")
            parser_choice = input("输入选择(a/b): ").lower()
            
            if parser_choice == 'a':
                parser = OutputParserFactory.create_parser('json')
                agent.set_output_parser(parser)
                print("已设置为 JSON 输出解析器")
            elif parser_choice == 'b':
                print("\n选择Pydantic schema：")
                print("1. analysis - 分析结果")
                print("2. weather - 天气报告")
                schema_choice = input("输入选择(1/2): ")
                schema_type = 'weather' if schema_choice == '2' else 'analysis'
                parser = OutputParserFactory.create_parser('pydantic', schema_type)
                agent.set_output_parser(parser)
                print(f"已设置为 Pydantic 输出解析器 (schema: {schema_type})")
            else:
                print("无效选择")
        elif choice == "5":
            agent.run_chat_loop()
        elif choice == "6":
            if agent.output_parser:
                agent.run_parsed_chat_loop()
            else:
                print("请先设置输出解析器（选项4）")
        elif choice == "7":
            print("再见！")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()