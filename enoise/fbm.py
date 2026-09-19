"""
分形柏林噪声（fBm）
"""

from .perlin import perlin, _perlin_np, _HAS_NUMPY


def fbm(x, y, octaves=4, grid=100.0, persistence=0.5, lacunarity=2.0):
    """
    分形柏林噪声（单点，纯 Python）

    参数:
        x, y: 坐标
        octaves: 叠加层数
        grid: 基础格子大小
        persistence: 每层振幅衰减，默认 0.5
        lacunarity: 每层频率倍增，默认 2.0

    返回:
        float，归一化到 [-1, 1]
    """
    total = 0.0
    amp = 1.0
    freq = 1.0
    max_amp = 0.0

    for _ in range(octaves):
        total += perlin(x * freq, y * freq, grid) * amp
        max_amp += amp
        amp *= persistence
        freq *= lacunarity

    return total / max_amp if max_amp > 0 else 0.0


def fbm2(x, y, octaves=4, grid=100.0, persistence=0.5):
    """二维分形噪声的便捷别名"""
    return fbm(x, y, octaves, grid, persistence)


def fbm3(x, y, z, octaves=4, grid=100.0, persistence=0.5):
    """
    三维分形噪声（简化版，用两个二维噪声混合模拟）
    """
    n1 = fbm(x, y, octaves, grid, persistence)
    n2 = fbm(y, z, octaves, grid, persistence)
    return (n1 + n2) * 0.5


def fbm_array(x0, y0, width, height, octaves=4, grid=100.0,
              persistence=0.5, lacunarity=2.0, scale=1.0):
    """
    批量生成分形噪声矩阵（需要 numpy）
    返回 shape 为 (height, width) 的 numpy 数组
    """
    if not _HAS_NUMPY:
        raise ImportError("fbm_array 需要安装 numpy：pip install numpy")

    import numpy as np

    xs = np.arange(width, dtype=np.float64) * scale
    ys = np.arange(height, dtype=np.float64) * scale
    X, Y = np.meshgrid(xs, ys)
    X = X + x0
    Y = Y + y0

    total = np.zeros_like(X)
    amp = 1.0
    freq = 1.0
    max_amp = 0.0

    for _ in range(octaves):
        total += _perlin_np(X * freq, Y * freq, grid) * amp
        max_amp += amp
        amp *= persistence
        freq *= lacunarity

    return total / max_amp if max_amp > 0 else total
