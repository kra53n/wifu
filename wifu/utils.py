def notify(sign: str, length: int, msg: str):
    diff = length - len(msg) - 2
    half = diff // 2
    remainder = diff % 2
    print(f'{sign * (half+remainder)} {msg} {sign * half}')