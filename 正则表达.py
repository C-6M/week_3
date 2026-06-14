import re

  # 提取手机号
print(re.findall(r"1[3-9]\d{9}", "我手机13812345678，备用15987654321"))

  # 提取邮箱
print(re.findall(r"\w+@\w+\.\w+", "联系我abc@qq.com或test@gmail.com",re.ASCII))

  # 提取日期
print(re.findall(r"\d{4}-\d{2}-\d{2}", "2024-01-15会议，2024-03-20截止"))
text = "电话13812345678，邮编518060"
print(re.search(r"\d+", text))     # 找第一个匹配 → match对象，用 .group() 取值
print(re.findall(r"\d+", text))    # 找所有匹配 → 返回列表 ['13812345678','518060']
print(re.match(r"\d+", text))      # 只在字符串开头匹配（text开头是"电"，返回None）
print(re.sub(r"\d+", "***", text)) # 替换 → "电话***，邮编***"
print(re.split(r"\d+", text))     # 按正则切分 → ['电话','，邮编','']
print(re.findall(r"\d{3}$", "邮编518060"))   # ['060'] — 最后3位
print(re.findall(r"^\d{3}", "518060邮编"))   # ['518'] — 开头3位
