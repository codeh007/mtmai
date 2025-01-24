import asyncio
import json
import pprint
import threading
from typing import Callable

from fastapi import APIRouter
import structlog

router = APIRouter()
LOG = structlog.get_logger()



counter = 0
stop_event = asyncio.Event()
counter_lock = threading.Lock()


@router.get("/counter_stop")
async def counter_stop():
    global stop_event
    stop_event.set()  # Signal the background task to stop
    return {"message": "Counter will stop soon"}


@router.get("/get_counter")
async def get_count():
    print("get_counter")
    global counter
    with counter_lock:
        current_counter = counter
    return {"counter": current_counter}


class DemoTaskRunner:
    def __init__(self, streamer: Callable[[str], None]):
        self.streamer = streamer

    async def run(self):
        for i in range(1, 15):
            await asyncio.sleep(0.5)
            if self.streamer:
                self.streamer(f"0:{json.dumps({'task_id': i})}\n")


# dbFile = ".vol/demo_users.db"


# def initMysqlLiteDb():
#     import sqlite3

#     # 连接到SQLite数据库（如果不存在则创建）
#     if os.path.exists(dbFile):
#         print("删除旧数据库", dbFile)
#         os.remove(dbFile)

#     if not os.path.exists(".vol"):
#         os.mkdir(".vol")
#     conn = sqlite3.connect(dbFile)
#     cursor = conn.cursor()

#     # 创建用户表
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#         age INTEGER,
#         email TEXT UNIQUE,
#         registration_date DATE,
#         last_login DATETIME
#     )
#     """)

#     # 生成示例数据
#     names = [
#         "Alice",
#         "Bob",
#         "Charlie",
#         "David",
#         "Eva",
#         "Frank",
#         "Grace",
#         "Henry",
#         "Ivy",
#         "Jack",
#         "Liang",
#         "Boci",
#         "Zhang",
#     ]
#     domains = [
#         "gmail.com",
#         "yahoo.com",
#         "hotmail.com",
#         "example.com",
#         "example2.com",
#         "example3.com",
#     ]

#     for i in range(20):  # 创建50个用户记录
#         name = random.choice(names)
#         age = random.randint(18, 70)
#         email = f"{name.lower()}{random.randint(1, 100)}@{random.choice(domains)}"
#         registration_date = datetime.now() - timedelta(days=random.randint(1, 1000))
#         last_login = registration_date + timedelta(days=random.randint(1, 500))

#         cursor.execute(
#             """
#         INSERT INTO users (name, age, email, registration_date, last_login)
#         VALUES (?, ?, ?, ?, ?)
#         """,
#             (name, age, email, registration_date.date(), last_login),
#         )

#     # 提交更改并关闭连接
#     conn.commit()
#     conn.close()

#     print("Demo database 'demo_users.db' created successfully with sample data.")

#     # 函数用于显示表格内容
#     def display_table_contents():
#         conn = sqlite3.connect(dbFile)
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users LIMIT 5")
#         rows = cursor.fetchall()

#         print("\nSample data from the users table:")
#         for row in rows:
#             print(row)

#         conn.close()

#     display_table_contents()


# 定义使用的模型名称
MODEL = "llama3-groq-70b-8192-tool-use-preview"


async def calculate(expression):
    """计算数学表达式"""
    try:
        # 使用eval函数评估表达式
        result = eval(expression)
        # 返回JSON格式的结果
        return json.dumps({"result": result})
    except Exception:
        # 如果计算出错，返回错误信息
        return json.dumps({"error": "Invalid expression"})


async def run_conversation(user_prompt):
    """
    tool use 本质是多轮对话，当上一轮 ai 返回了 tool_calls 答复，本地根据tool_calls 调用对应的函数，然后将结果附加到消息末尾，再次提交给ai，然后ai完成下一轮的答复。
    """
    aiClient = get_default_openai_client()
    # 定义对话的消息列表
    messages = [
        {
            "role": "system",
            "content": "你是一个计算器助手。使用计算函数执行数学运算并提供结果.",
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    # 定义可用的工具（函数）
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "计算数学表达式",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "要评估的数学表达式",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]

    print("第一次信息输出: {messages}\n")
    # 作用和目的：
    # 初始化对话：将用户的问题发送给 AI 模型。
    # 提供工具信息：告诉模型可以使用哪些工具（在这里是 calculate 函数）。
    # 获取模型的初步响应：模型可能会直接回答，或者决定使用提供的工具。

    # 特点：
    # 包含了初始的对话历史（系统提示和用户问题）。
    # 提供了 tools 参数，定义了可用的函数。
    # 使用 tool_choice="auto"，允许模型自主决定是否使用工具。
    response = aiClient.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto", max_tokens=4096
    )
    print("输出response {response}\n")
    # 获取响应消息和工具调用
    response_message = response.choices[0].message
    print(f"第一次响应输出: {response_message} \n")
    tool_calls = response_message.tool_calls
    print("输出tool_calls信息: \n")
    pprint.pprint(tool_calls)
    print("\n")

    # 如果有工具调用
    if tool_calls:
        # 定义可用的函数字典
        available_functions = {
            "calculate": calculate,
        }
        # 将响应消息添加到对话历史
        messages.append(response_message)

        # 处理每个工具调用
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            # 解析函数参数
            function_args = json.loads(tool_call.function.arguments)
            # 调用函数并获取响应
            function_response = await function_to_call(
                expression=function_args.get("expression")
            )
            print("\n输出function_response " + function_response + "\n")
            # 将函数调用结果添加到对话历史
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        print("第二次信息输出 : {messages} \n")
        second_response = aiClient.chat.completions.create(
            model=MODEL, messages=messages
        )
        # 返回最终响应内容
        return second_response.choices[0].message.content
