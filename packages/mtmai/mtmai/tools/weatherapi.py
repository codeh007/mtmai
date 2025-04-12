import requests

from mtmai.core.config import settings

# 城市名称映射字典，将中文城市名映射到英文
CITY_NAME_MAP = {
    "纽约": "New York",
    "伦敦": "London",
    "东京": "Tokyo",
    "北京": "Beijing",
    "上海": "Shanghai",
    "巴黎": "Paris",
    "柏林": "Berlin",
    "悉尼": "Sydney",
    "莫斯科": "Moscow",
    "迪拜": "Dubai",
    "深圳": "Shenzhen",
    "广州": "Guangzhou",
    "成都": "Chengdu",
    "重庆": "Chongqing",
    "西安": "Xi'an",
    "长沙": "Changsha",
    # 可以继续添加更多常用城市
}


def get_weather(city: str) -> dict:
    """获取指定城市的当前天气报告。

    使用weatherapi.com的API获取实时天气数据。
    支持中文城市名，内部会自动转换为英文名。

    参数:
        city (str): 要获取天气报告的城市名称（中文或英文）。

    返回:
        dict: 包含状态和结果或错误信息的字典。
    """
    # API密钥和基础URL
    api_key = settings.WEATHER_API_KEY
    base_url = "http://api.weatherapi.com/v1/current.json"

    # 检查城市名是否需要转换为英文
    query_city = CITY_NAME_MAP.get(city, city)

    try:
        params = {"key": api_key, "q": query_city}

        # 天气API
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            # 提取相关天气信息
            location = data["location"]["name"]
            country = data["location"]["country"]
            temp_c = data["current"]["temp_c"]
            temp_f = data["current"]["temp_f"]
            condition = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]

            # 构建天气报告（使用原始输入的城市名）
            report = (
                f"当前{city}({country})的天气为{condition}，"
                f"温度{temp_c}°C ({temp_f}°F)，"
                f"湿度{humidity}%，风速{wind_kph}公里/小时。"
            )

            return {
                "status": "success",
                "report": report,
            }
        else:
            return {
                "status": "error",
                "error_message": f"无法获取'{city}'的天气信息。API响应代码: {response.status_code}，请检查城市名称是否正确。",
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"获取'{city}'的天气信息时出错: {str(e)}",
        }


def get_current_time(city: str) -> dict:
    """获取指定城市的当前时间。

    使用weatherapi.com的API获取城市的时区信息，
    然后根据时区计算当前时间。
    支持中文城市名，内部会自动转换为英文名。

    参数:
        city (str): 要获取当前时间的城市名称（中文或英文）。

    返回:
        dict: 包含状态和结果或错误信息的字典。
    """
    # API密钥和基础URL（与天气API相同）
    api_key = settings.WEATHER_API_KEY
    base_url = "http://api.weatherapi.com/v1/current.json"

    # 检查城市名是否需要转换为英文
    query_city = CITY_NAME_MAP.get(city, city)

    try:
        params = {"key": api_key, "q": query_city}
        # 获取时区信息
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()

            # 提取时区ID和本地时间
            tz_id = data["location"]["tz_id"]
            localtime = data["location"]["localtime"]

            report = f"当前{city}的时间是 {localtime} ({tz_id}时区)"

            return {"status": "success", "report": report}
        else:
            return {
                "status": "error",
                "error_message": f"无法获取'{city}'的时区信息。API响应代码: {response.status_code}，请检查城市名称是否正确。",
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"获取'{city}'的时间信息时出错: {str(e)}",
        }
