import requests
from datetime import datetime,timedelta
def get_weather(city):
    try:
      resp = requests.get(f"https://wttr.in/{city}/?format=j1", timeout=5)
      resp.raise_for_status()         # 不是 200 就抛异常
      data = resp.json()
      weather = data["current_condition"][0]
      print(weather.keys())
      UTC_time = datetime.strptime(weather['observation_time'],"%I:%M %p")
      beijing_time = UTC_time + timedelta(hours=8)
      print(f"{city}：{weather['temp_C']}°C，{weather['weatherDesc'][0]['value']}，体感温度{weather['FeelsLikeC']}°C，观测时间{beijing_time.strftime('%H:%M')}")
    except requests.exceptions.Timeout:
      print("请求超时，请稍后再试")
    except requests.exceptions.HTTPError:
      print(f"服务器返回错误：{resp.status_code}")
    except requests.exceptions.RequestException as e:
      print(f"请求失败：{e}")
if __name__ == "__main__":
    city = input("请输入城市名称：")
    get_weather(city)