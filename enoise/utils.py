"""
工具函数：颜色映射
"""

import colorsys


def hsv_to_rgb(h, s, v):
    """
    HSV -> RGB
    h: [0, 360)，s/v: [0, 1]
    返回 (r, g, b)，各分量 [0, 255]
    """
    r, g, b = colorsys.hsv_to_rgb((h % 360) / 360.0, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def colorize(value, mode="color", hue_range=120.0, hue_offset=180.0):
    """
    把噪声值 [-1, 1] 映射为颜色

    参数:
        value: 噪声值
        mode: "color" 彩色 / "gray" 灰度
        hue_range: 色相范围
        hue_offset: 色相偏移

    返回:
        (r, g, b) 元组
    """
    if mode == "gray":
        v = int((value * 0.5 + 0.5) * 255)
        v = max(0, min(255, v))
        return v, v, v

    hue = (value * hue_range + hue_offset) % 360.0
    return hsv_to_rgb(hue, 220 / 255.0, 1.0)
