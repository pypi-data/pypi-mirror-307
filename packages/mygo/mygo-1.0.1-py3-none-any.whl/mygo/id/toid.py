import time
import random


def to_base64(num: int) -> str:
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    if num == 0:
        return BASE64_CHARS[0]

    result = []
    while num:
        remainder = num & 0x3F  # 等价于 num % 64
        result.append(BASE64_CHARS[remainder])
        num >>= 6
    return ''.join(reversed(result))

def reverse_bits(n: int) -> int:
    res = 0
    for i in range(64):
        res = (res << 1) | ((n >> i) & 1)
    return res

def toid(msid:int = 0) -> str:
    # 获取纳秒级时间戳
    nanoseconds_timestamp: int = time.time_ns()
    rev_ts: int = reverse_bits(nanoseconds_timestamp)
    return to_base64(rev_ts + msid)

print(toid())
