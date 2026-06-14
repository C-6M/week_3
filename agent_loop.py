import re
import requests
from datetime import datetime, timedelta


def search(query):
    knowledge_base = {
        "python": "Python 是一门解释型、面向对象的高级编程语言，由 Guido van Rossum 于 1991 年发布。广泛用于 Web 开发、数据分析、AI 等领域。",
        "深圳大学": "深圳大学成立于 1983 年，位于广东省深圳市南山区，是广东省高水平大学重点建设高校。",
        "正则表达式": "正则表达式（Regular Expression）是一种用于匹配字符串的模式。Python 中使用 re 模块处理正则。常用方法：search、findall、sub、split。",
        "递归": "递归是一种函数调用自身的编程技巧。需要设置终止条件防止无限循环。经典例子：阶乘、斐波那契数列、汉诺塔。",
        "json": "JSON（JavaScript Object Notation）是一种轻量级数据交换格式。Python 中使用 json 模块进行 dumps/loads/dump/load 操作。",
    }
    query_lower = query.lower()
    for key in knowledge_base:
        if key in query_lower:
            return "[搜索] " + key + "\n" + knowledge_base[key]
    return "[搜索] 没找到关于「" + query + "」的结果"


def calculator(expr):
    if re.fullmatch(r"[\d\s+\-*/().%]+", expr) is None:
        return "[计算器] 表达式有不合法的字符"
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        return "[计算器] " + expr + " = " + str(result)
    except ZeroDivisionError:
        return "[计算器] 不能除以 0"
    except SyntaxError:
        return "[计算器] 语法错误"
    except Exception as e:
        return "[计算器] 出错：" + str(e)


def get_weather(city):
    city = city.strip()
    if not city:
        return "[天气] 城市名不能为空"
    if re.match(r"^[一-鿿a-zA-Z\s\-]+$", city) is None:
        return "[天气] 城市名格式不对"

    try:
        resp = requests.get("https://wttr.in/" + city + "?format=j1", timeout=10)
        if resp.status_code != 200:
            return "[天气] 没有找到城市「" + city + "」"
        data = resp.json()
        current = data["current_condition"][0]
        utc_time = datetime.strptime(current["observation_time"], "%I:%M %p")
        beijing_time = utc_time + timedelta(hours=8)

        result = "[天气] " + city + "\n"
        result += "  温度: " + current["temp_C"] + "C\n"
        result += "  天气: " + current["weatherDesc"][0]["value"] + "\n"
        result += "  湿度: " + current["humidity"] + "%\n"
        result += "  体感: " + current["FeelsLikeC"] + "C\n"
        result += "  观测时间: " + beijing_time.strftime("%H:%M")
        return result
    except requests.exceptions.Timeout:
        return "[天气] 请求超时"
    except requests.exceptions.ConnectionError:
        return "[天气] 网络连接失败"
    except Exception as e:
        return "[天气] 出错：" + str(e)


def translate(text):
    text = text.strip()
    if not text:
        return "[翻译] 请输入文本"

    if re.search(r"[一-鿿]", text):
        from_lang, to_lang, direction = "zh", "en", "中 -> 英"
    else:
        from_lang, to_lang, direction = "en", "zh", "英 -> 中"

    try:
        resp = requests.post(
            "https://api.mymemory.translated.net/get",
            data={"q": text, "langpair": from_lang + "|" + to_lang},
            timeout=10
        )
        if resp.status_code != 200:
            return "[翻译] 服务出错"
        data = resp.json()
        translated = data["responseData"]["translatedText"]
        return "[翻译] " + direction + "\n  原文: " + text + "\n  译文: " + translated
    except requests.exceptions.Timeout:
        return "[翻译] 请求超时"
    except requests.exceptions.ConnectionError:
        return "[翻译] 网络连接失败"
    except Exception as e:
        return "[翻译] 出错：" + str(e)


TOOLS = {
    "search": {
        "func": search,
        "keywords": ["搜索", "查", "search"],
        "description": "搜索"
    },
    "calculator": {
        "func": calculator,
        "keywords": ["计算", "算", "=", "+", "-", "*", "/"],
        "description": "计算器"
    },
    "get_weather": {
        "func": get_weather,
        "keywords": ["天气", "weather", "气温", "温度"],
        "description": "天气"
    },
    "translate": {
        "func": translate,
        "keywords": ["翻译", "translate", "译", "英文"],
        "description": "翻译"
    },
}


def decide_tool(user_input):
    user_lower = user_input.lower()

    if re.search(r"[\d]+\s*[\+\-\*/]\s*[\d]+", user_input):
        return "calculator", user_input

    for tool_name in TOOLS:
        for kw in TOOLS[tool_name]["keywords"]:
            if kw in user_lower:
                if tool_name == "get_weather":
                    city = user_input
                    for w in ["天气", "weather", "查询", "查", "温度", "气温", "多少度"]:
                        city = city.replace(w, "")
                    city = city.strip()
                    if not city:
                        return None, "请提供城市名，比如：深圳天气"
                    return tool_name, city

                if tool_name == "search":
                    query = user_input
                    for p in ["搜索", "查", "search"]:
                        query = query.replace(p, "")
                    query = query.strip()
                    if not query:
                        return None, "请提供关键词，比如：搜索 Python"
                    return tool_name, query

                if tool_name == "translate":
                    text = user_input
                    for p in ["翻译", "translate", "译成英文", "译成中文"]:
                        text = text.replace(p, "")
                    text = text.strip()
                    if not text:
                        return None, "请提供文本，比如：翻译 hello"
                    return tool_name, text

                return tool_name, user_input

    return None, "试试：搜索 Python / 1+2*3 / 深圳天气 / 翻译 hello"


def run_agent():
    print("Agent Loop - 搜索 | 计算 | 天气 | 翻译")
    print("输入 q 退出，help 帮助\n")

    while True:
        try:
            user_input = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd in ("q", "quit", "exit"):
            print("再见！")
            break

        if cmd in ("help", "帮助"):
            print("深圳天气 / 1+2*3 / 搜索 Python / 翻译 hello\n")
            continue

        tool_name, arg = decide_tool(user_input)
        if tool_name is None:
            print("Bot > " + arg + "\n")
            continue

        print("Bot > [" + tool_name + "]")
        result = TOOLS[tool_name]["func"](arg)
        print("Bot > " + result + "\n")


if __name__ == "__main__":
    run_agent()
