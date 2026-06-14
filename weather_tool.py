import requests
import json
import re
import os
from datetime import datetime, timedelta

CACHE_FILE = "weather_cache.json"


class WeatherTool:

    def __init__(self):
        self.cache = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            f = open(CACHE_FILE, "r", encoding="utf-8")
            self.cache = json.load(f)
            f.close()
            print("[缓存] 加载了 " + str(len(self.cache)) + " 条记录")

    def save_cache(self):
        f = open(CACHE_FILE, "w", encoding="utf-8")
        json.dump(self.cache, f, ensure_ascii=False, indent=2)
        f.close()

    def check_cache(self, city):
        if city not in self.cache:
            return None
        entry = self.cache[city]
        cached_time = datetime.fromisoformat(entry["time"])
        if datetime.now() - cached_time < timedelta(hours=1):
            print("[缓存命中] " + city)
            return entry["data"]
        else:
            del self.cache[city]
            return None

    def add_cache(self, city, data):
        self.cache[city] = {
            "time": datetime.now().isoformat(),
            "data": data
        }
        self.save_cache()

    def check_city_name(self, city):
        if not city or not city.strip():
            return False, "城市名不能为空"
        city = city.strip()
        if len(city) > 50:
            return False, "城市名太长"
        if re.match(r"^[一-鿿a-zA-Z\s\-]+$", city) is None:
            return False, "城市名只能包含中英文、空格和连字符"
        return True, city

    def query(self, city):
        ok, result = self.check_city_name(city)
        if not ok:
            return {"error": result}
        city = result

        cached_data = self.check_cache(city)
        if cached_data is not None:
            return cached_data

        url = "https://wttr.in/" + city + "?format=j1"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 404:
                return {"error": "没有找到城市「" + city + "」"}
            if resp.status_code != 200:
                return {"error": "服务器错误，状态码：" + str(resp.status_code)}
            data = resp.json()
        except requests.exceptions.Timeout:
            return {"error": "请求超时，请稍后再试"}
        except requests.exceptions.ConnectionError:
            return {"error": "网络连接失败"}
        except Exception as e:
            return {"error": "请求出错：" + str(e)}

        try:
            current = data["current_condition"][0]
            utc_time = datetime.strptime(current["observation_time"], "%I:%M %p")
            beijing_time = utc_time + timedelta(hours=8)

            weather_data = {
                "city": city,
                "temp_C": current["temp_C"],
                "weather_desc": current["weatherDesc"][0]["value"],
                "humidity": current["humidity"],
                "feels_like": current["FeelsLikeC"],
                "observation_time": beijing_time.strftime("%H:%M"),
            }

            temp = int(weather_data["temp_C"])
            if temp <= 0:
                weather_data["alert"] = "气温零下，注意保暖！"
            elif temp <= 10:
                weather_data["alert"] = "气温较低，建议穿厚外套"
            elif temp >= 35:
                weather_data["alert"] = "高温预警，注意防暑！"

            self.add_cache(city, weather_data)
            return weather_data
        except Exception as e:
            return {"error": "数据解析失败：" + str(e)}

    def batch_query(self, cities_str):
        city_list = re.split(r"[,，\s]+", cities_str.strip())
        city_list = [c.strip() for c in city_list if c.strip() != ""]
        if len(city_list) == 0:
            return "请至少输入一个城市名"

        results = []
        for city in city_list:
            print("  查询中: " + city + "...")
            results.append(self.query(city))

        return self.format_table(results)

    def format_table(self, results):
        lines = [
            "城市         温度    天气          湿度   体感    观测时间    备注",
            "-" * 70
        ]
        for r in results:
            if "error" in r:
                lines.append(r.get("city", "?") + "    查询失败：" + r["error"])
            else:
                alert = r.get("alert", "")
                line = f"{r['city']:<10} {r['temp_C']:>4}C   {r['weather_desc']:<10} {r['humidity']:>4}%  {r['feels_like']:>4}C   {r['observation_time']:>6}    {alert}"
                lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    tool = WeatherTool()
    print("天气查询小工具")

    while True:
        print("\n1. 查城市  2. 批量查  3. 缓存  4. 清缓存  q. 退出")
        choice = input("请选择: ").strip()

        if choice == "q":
            print("再见！")
            break
        elif choice == "1":
            city = input("城市名: ").strip()
            r = tool.query(city)
            if "error" in r:
                print("出错了：" + r["error"])
            else:
                print("")
                print("  " + r["city"])
                print("  温度: " + r["temp_C"] + "C")
                print("  天气: " + r["weather_desc"])
                print("  湿度: " + r["humidity"] + "%")
                print("  体感: " + r["feels_like"] + "C")
                print("  观测时间: " + r["observation_time"])
                if "alert" in r:
                    print("  " + r["alert"])
        elif choice == "2":
            cities = input("城市名（逗号或空格隔开）: ").strip()
            print("\n" + tool.batch_query(cities))
        elif choice == "3":
            if len(tool.cache) == 0:
                print("缓存为空")
            else:
                print("共 " + str(len(tool.cache)) + " 条：")
                for city in tool.cache:
                    t = tool.cache[city]["data"]["temp_C"]
                    print("  " + city + ": " + t + "C")
        elif choice == "4":
            tool.cache = {}
            tool.save_cache()
            print("缓存已清空")
