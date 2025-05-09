from g4f.client import Client

client = Client()
response = client.images.generate(
    model="flux", prompt="a white siamese cat", response_format="url"
)

print(f"Generated image URL: {response.data[0].url}")


# response = client.chat.completions.create(
#     model="gemini-2.0-flash-exp",
#     messages=[{"role": "user", "content": "Hello, how are you?"}],
# )

# print(response)


# sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.1
# from g4f.gui.webview import run_webview

# run_webview(debug=True)
