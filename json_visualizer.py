import json
import os

CACHE_FILE = "weather_cache.json"


def load_weather_data():
    if not os.path.exists(CACHE_FILE):
        print("缓存文件 " + CACHE_FILE + " 不存在")
        print("请先运行 weather_tool.py 查询几个城市")
        return []

    f = open(CACHE_FILE, "r", encoding="utf-8")
    raw = json.load(f)
    f.close()

    records = []
    for city in raw:
        d = raw[city]["data"]
        records.append({
            "city": city,
            "temp": int(d["temp_C"]),
            "feels_like": int(d["feels_like"]),
            "humidity": int(d["humidity"]),
            "weather": d["weather_desc"],
            "obs_time": d["observation_time"],
        })
    return records


def show_table(data):
    data.sort(key=lambda x: x["temp"], reverse=True)

    max_temp = data[0]["temp"]
    min_temp = data[0]["temp"]
    total = 0
    for r in data:
        t = r["temp"]
        total += t
        if t > max_temp:
            max_temp = t
        if t < min_temp:
            min_temp = t
    avg = round(total / len(data), 1)

    print(f"{'城市':<10} {'温度':>5} {'体感':>5} {'湿度':>5} {'天气':<12} {'观测':>6}  趋势")
    print("-" * 60)

    for i in range(len(data)):
        r = data[i]
        temp = r["temp"]
        if temp == max_temp:
            trend = "最高"
        elif temp == min_temp:
            trend = "最低"
        elif i > 0 and temp > data[i-1]["temp"]:
            trend = "上升"
        elif i > 0 and temp < data[i-1]["temp"]:
            trend = "下降"
        else:
            trend = "持平"

        mark = ""
        if temp >= 35:
            mark = " [热]"
        elif temp <= 0:
            mark = " [冷]"

        print(f"{r['city']:<10} {str(temp)+'C'+mark:>10} {str(r['feels_like'])+'C':>5} {str(r['humidity'])+'%':>5} {r['weather']:<12} {r['obs_time']:>6}   {trend}")

    print("-" * 60)
    print("共 " + str(len(data)) + " 城市 | 平均 " + str(avg) + "C | 最高 " + str(max_temp) + "C | 最低 " + str(min_temp) + "C")


def show_bar(data):
    data.sort(key=lambda x: x["temp"], reverse=True)
    max_temp = data[0]["temp"]
    if max_temp <= 0:
        max_temp = 1

    print("\n温度柱状图")
    print("-" * 50)
    for r in data:
        bar_len = int(r["temp"] / max_temp * 25)
        if bar_len < 1:
            bar_len = 1
        print("  " + r["city"] + "  " + "#" * bar_len + "  " + str(r["temp"]) + "C")
    print("-" * 50)


if __name__ == "__main__":
    data = load_weather_data()
    if len(data) == 0:
        print("\n还没有天气数据，请先运行 weather_tool.py")
    else:
        show_table(data)
        show_bar(data)
