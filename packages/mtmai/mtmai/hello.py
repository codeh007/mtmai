from openai import OpenAI
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

print("start")
completion = client.chat.completions.create(
  model="deepseek-ai/deepseek-r1",
  messages=[{"role":"user","content":"hello"}],
  temperature=0.6,
  top_p=0.7,
  max_tokens=4096,
  stream=True
)

print("response:\n")
for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

print("\n")