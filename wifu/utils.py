def notify(sign: str, length: int, msg: str) -> str:
    diff = length - len(msg) - 2
    half = diff // 2
    remainder = diff % 2
    return f'{sign * (half+remainder)} {msg} {sign * half}'