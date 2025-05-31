import asyncio
import base64

import httpx


async def decode_clash_config(url: str):
  """clash 订阅, 解密

  原理: 网址返回的是使用了 base64 编码的 clash 配置文件, 需要解码
  """
  content = httpx.get(url).text
  # print(content)
  decoded_content = base64.b64decode(content).decode("utf-8")
  print(decoded_content)


if __name__ == "__main__":
  asyncio.run(
    decode_clash_config("https://link02.qytsub02.pro/api/v1/client/subscribe?token=17e621c7b8dd557d829c00afbfee8d93")
  )
