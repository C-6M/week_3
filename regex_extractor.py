import re

phone_pattern = r"1[3-9]\d{9}"
email_pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
date_ymd = r"\d{4}-\d{1,2}-\d{1,2}"
date_slash = r"\d{4}/\d{1,2}/\d{1,2}"
date_dot = r"\d{4}\.\d{1,2}\.\d{1,2}"
date_cn = r"\d{4}年\d{1,2}月\d{1,2}日"


def extract_phones(text):
    return re.findall(phone_pattern, text)


def extract_emails(text):
    return re.findall(email_pattern, text)


def extract_dates(text):
    result = {}
    m1 = re.findall(date_ymd, text)
    if m1:
        result["YYYY-MM-DD"] = m1
    m2 = re.findall(date_slash, text)
    if m2:
        result["YYYY/MM/DD"] = m2
    m3 = re.findall(date_dot, text)
    if m3:
        result["YYYY.MM.DD"] = m3
    m4 = re.findall(date_cn, text)
    if m4:
        result["YYYY年MM月DD日"] = m4
    return result


def extract_all(text):
    phones = extract_phones(text)
    emails = extract_emails(text)
    dates = extract_dates(text)
    total_dates = 0
    for dl in dates.values():
        total_dates = total_dates + len(dl)
    summary = "找到 " + str(len(phones)) + " 个手机号，" + str(len(emails)) + " 个邮箱，" + str(total_dates) + " 个日期"
    return {"phones": phones, "emails": emails, "dates": dates, "summary": summary}


if __name__ == "__main__":
    print("正则提取工具 - 手机号 | 邮箱 | 日期")
    print("输入 1-4 看演示，q 退出\n")

    s1 = "请联系我：手机 13812345678，邮箱 abc@qq.com，日期 2024-01-15"
    s2 = "张三 15987654321 zhang@szu.edu.cn 2024/03/20 参会；李四 18866668888 li@163.com 2024年06月14日截止"
    s3 = "客服热线：400-800-1234，邮箱 support@example.com，订单日期 2024.06.14"
    s4 = "简历：手机13912345678，邮箱test@gmail.com，出生日期1999-12-31，工作经历2020/01/01至2024/12/31"

    while True:
        cmd = input("文本 > ").strip()
        if cmd == "q":
            print("再见！")
            break
        if cmd == "":
            continue
        if cmd == "1":
            text = s1
        elif cmd == "2":
            text = s2
        elif cmd == "3":
            text = s3
        elif cmd == "4":
            text = s4
        else:
            text = cmd

        r = extract_all(text)
        print("\n" + r["summary"])
        print("-" * 40)
        if r["phones"]:
            print("手机号 (" + str(len(r["phones"])) + "个):")
            for p in r["phones"]:
                print("  - " + p)
        if r["emails"]:
            print("邮箱 (" + str(len(r["emails"])) + "个):")
            for e in r["emails"]:
                print("  - " + e)
        if r["dates"]:
            count = 0
            for dl in r["dates"].values():
                count = count + len(dl)
            print("日期 (" + str(count) + "个):")
            for fmt in r["dates"]:
                for d in r["dates"][fmt]:
                    print("  - " + d + "  (" + fmt + ")")
        print("-" * 40 + "\n")
