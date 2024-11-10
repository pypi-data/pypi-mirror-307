def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b


def qerp(a: float, b: float, c: float, t: float) -> float:
    return lerp(lerp(a, b, t), lerp(b, c, t), t)


def cerp(a: float, b: float, c: float, d: float, t: float) -> float:
    return lerp(qerp(a, b, c, t), qerp(b, c, d, t), t)
