import logging
import os

import gradio as gr
from fastapi import FastAPI
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)


def getInferenceClient():
    """
    For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
    """
    if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        raise ValueError("HUGGINGFACEHUB_API_TOKEN 未设置")
    return InferenceClient(
        "HuggingFaceH4/zephyr-7b-beta",
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    )


def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in getInferenceClient().chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content

        response += token
        yield response


def greet(name):
    return "Hello greeter " + name + "!"


# 新增一个示例函数
def calculate(a: int, b: int, operation: str):
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    return None


with gr.Blocks() as demo:
    # 聊天界面
    chatbot = gr.ChatInterface(
        respond,
        additional_inputs=[
            gr.Textbox(value="You are a friendly Chatbot.", label="System message222"),
            gr.Slider(
                minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"
            ),
            gr.Slider(
                minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"
            ),
            gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.95,
                step=0.05,
                label="Top-p (nucleus sampling)",
            ),
        ],
    )

    # 添加 greet API
    gr.Interface(
        fn=greet,
        inputs=gr.Textbox(label="Name"),
        outputs=gr.Textbox(label="Output"),
        api_name="greet",  # 这将创建 /greet 端点
    )

    # 添加 calculate API
    gr.Interface(
        fn=calculate,
        inputs=[
            gr.Number(label="First Number"),
            gr.Number(label="Second Number"),
            gr.Radio(choices=["add", "multiply"], label="Operation"),
        ],
        outputs=gr.Number(label="Result"),
        api_name="calculate",  # 这将创建 /calculate 端点
    )


def mount_gradio_app(app: FastAPI):
    """
    将 gradio 应用挂载到 fastapi 的根
    """
    import gradio as gr

    from .gradio_app import demo

    logger.info("mount_gradio_app")
    gr.mount_gradio_app(app, demo, path="/")


if __name__ == "__main__":
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=18089,
    )
