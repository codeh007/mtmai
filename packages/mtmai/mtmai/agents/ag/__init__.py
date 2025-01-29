from opentelemetry.instrumentation.openai import OpenAIInstrumentor

# auth gen 官方文档:
# https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html


OpenAIInstrumentor().instrument()

print("初始化 autogen 环境")
