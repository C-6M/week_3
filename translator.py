import requests
def translate(text, from_lang, to_lang):
    try:
        resp = requests.post("https://api.mymemory.translated.net/get", data={"q": text, "langpair": f"{from_lang}|{to_lang}"}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        translation = data['responseData']["translatedText"]
        print(f"翻译结果：{translation},匹配度：{data['responseData']['match']}")
    except requests.exceptions.Timeout:
        print("请求超时，请稍后再试")
    except requests.exceptions.HTTPError:
        print(f"服务器返回错误：{resp.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
    except Exception as e:
        print(f"翻译出错：{e}")
direction = "to_chinese"   # 默认英译中
label = "英->中"
while True:
      print(f"\n[{label}] 请输入（s=切换方向 q=退出）：", end="")
      text = input().strip()
      if text.lower() == "q":          # 退出
          print("再见！")
          break
      if text.lower() == "s":          # 切换方向
          if direction == "to_chinese":
              direction = "to_english"
              label = "中->英"
          else:
              direction = "to_chinese"
              label = "英->中"
          print(f"已切换到：{label}")
          continue
      if not text:
          continue
      if direction == "to_chinese":
          translate(text, "en", "zh")
      else:
          translate(text, "zh", "en")
