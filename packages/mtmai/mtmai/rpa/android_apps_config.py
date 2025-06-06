androidAppConfig = {
  "instagram": {
    "package_name": "com.instagram.android",
    "app_name": "Instagram",
    # "apk_url": "https://mtreleases.yuepa8.com/apk/instgram_v2.apk",
    "apk_url": "https://apk2.yuepa8.com/apk/instgram_v2.apk",
  },
}


def get_android_app_info(package_name: str):
  return androidAppConfig[package_name]
