androidAppConfig = {
  "instagram": {
    "package_name": "com.instagram.android",
    "app_name": "Instagram",
    "apk_url": "instagram.apk",
  },
}


def get_android_app_info(package_name: str):
  return androidAppConfig[package_name]
