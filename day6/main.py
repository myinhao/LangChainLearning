from agentBaseInit import FileAgent

def main():
    print("Day 6 - Prompt工程进阶")
    print("=" * 50)
    
    agent = FileAgent()
    
    while True:
        print("\n请选择操作：")
        print("1. 设置系统提示词")
        print("2. 获取当前提示词")
        print("3. 更新提示词（重置对话）")
        print("4. 启动聊天模式")
        print("5. 退出")
        
        choice = input("输入选择(1-5): ")
        
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
            agent.run_chat_loop()
        elif choice == "5":
            print("再见！")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()