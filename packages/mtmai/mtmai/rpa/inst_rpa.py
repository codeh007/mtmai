from urllib.parse import urlparse

from lamda import client

# def start_instagram():
#   app = d.application("com.instagram.android")
#   app.start()

#   goodsid = input("Please input a taobao goods id (item_id) (eg. 123456): ")
#   if goodsid.isdigit():
#     intent = {
#       "package": "com.instagram.android",
#       "action": "android.intent.action.VIEW",
#       "component": "com.instagram.android/com.instagram.nux.activity.BloksSignedOutFragmentActivity",
#       "data": f"https://www.instagram.com/p/{goodsid}/",
#     }
#     d.start_activity(**intent)


class InstagramAutomation:
  def __init__(self, endpoint: str):
    uri = urlparse(endpoint)
    self.host = uri.hostname
    self.port = uri.port
    self.d = client.Device(self.host, self.port)

  async def start(self):
    self.app = self.d.application("com.instagram.android")
    await self.app.start()

  async def open_clash(self):
    self.clash_app = self.d.application("com.github.kr328.clash")
    await self.clash_app.start()
    intent = {
      "package": "com.github.kr328.clash",
      "action": "android.intent.action.MAIN",
      "component": "com.github.kr328.clash/.MainActivity",
    }
    await self.d.start_activity(**intent)
    await self.d.show_toast("Hello from Lamda!")
