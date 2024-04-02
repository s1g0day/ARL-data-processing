import idna

# 中文域名转ASCII
def convert_to_ascii(domain):
    try:
        ascii_domain = idna.encode(domain).decode('ascii')
        return ascii_domain
    except Exception as e:
        print("转换失败:", e)
        return None

def is_chinese_domain(domain):
    for char in domain:
        if ord(char) > 127:  # 如果字符的 ASCII 编码大于 127，则说明是非 ASCII 字符，可能是中文字符
            return True
    return False