"""
柏林噪声核心实现
纯 Python，无依赖；安装 numpy 后自动使用加速版本。
"""

import math

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False


# ------------------------------------------------------------
# 工具函数
# ------------------------------------------------------------

def _smoothstep(t):
    """平滑插值：3t^2 - 2t^3"""
    return t * t * (3.0 - 2.0 * t)


def _lerp(a, b, t):
    return a + (b - a) * t


def _hash_gradient(a, b):
    """用格点坐标 (a, b) 生成伪随机梯度角度"""
    angle = a * 0.1 + b * 0.1
    return math.cos(angle), math.sin(angle)


# ------------------------------------------------------------
# 纯 Python 版本
# ------------------------------------------------------------

def perlin(x, y, grid=100.0):
    """
    二维柏林噪声（纯 Python）

    参数:
        x, y: 坐标（int 或 float）
        grid: 格子大小，越小噪声越密，默认 100.0

    返回:
        float，大致在 [-1, 1] 区间
    """
    x0 = math.floor(x / grid) * grid
    y0 = math.floor(y / grid) * grid

    dx = x - x0
    dy = y - y0

    gx1, gy1 = _hash_gradient(x0, y0)
    d1 = gx1 * dx + gy1 * dy

    gx2, gy2 = _hash_gradient(x0 + grid, y0)
    d2 = gx2 * (dx - grid) + gy2 * dy

    gx3, gy3 = _hash_gradient(x0, y0 + grid)
    d3 = gx3 * dx + gy3 * (dy - grid)

    gx4, gy4 = _hash_gradient(x0 + grid, y0 + grid)
    d4 = gx4 * (dx - grid) + gy4 * (dy - grid)

    sx = _smoothstep(dx / grid)
    sy = _smoothstep(dy / grid)

    rx = _lerp(d1, d2, sx)
    ry = _lerp(d3, d4, sx)
    return _lerp(rx, ry, sy)


# ------------------------------------------------------------
# NumPy 加速版本
# ------------------------------------------------------------

def _perlin_np(x, y, grid=100.0):
    """向量化柏林噪声，x/y 可以是 numpy 数组"""
    x0 = np.floor(x / grid) * grid
    y0 = np.floor(y / grid) * grid

    dx = x - x0
    dy = y - y0

    def grad(ax, ay):
        angle = ax * 0.1 + ay * 0.1
        return np.cos(angle), np.sin(angle)

    gx1, gy1 = grad(x0, y0)
    d1 = gx1 * dx + gy1 * dy

    gx2, gy2 = grad(x0 + grid, y0)
    d2 = gx2 * (dx - grid) + gy2 * dy

    gx3, gy3 = grad(x0, y0 + grid)
    d3 = gx3 * dx + gy3 * (dy - grid)

    gx4, gy4 = grad(x0 + grid, y0 + grid)
    d4 = gx4 * (dx - grid) + gy4 * (dy - grid)

    sx = _smoothstep(dx / grid)
    sy = _smoothstep(dy / grid)

    rx = d1 + (d2 - d1) * sx
    ry = d3 + (d4 - d3) * sx
    return rx + (ry - rx) * sy


def perlin_np(x, y, grid=100.0):
    """公开的 numpy 版本（需要安装 numpy）"""
    if not _HAS_NUMPY:
        raise ImportError("perlin_np 需要安装 numpy：pip install numpy")
    return _perlin_np(x, y, grid)


# ------------------------------------------------------------
# 类接口
# ------------------------------------------------------------

class Perlin:
    """
    柏林噪声生成器（类接口）

    用法:
        p = Perlin(grid=100.0, seed=0)
        v = p.noise(12.3, 45.6)
        arr = p.noise_array(0, 0, 100, 100)   # 需要 numpy
    """

    def __init__(self, grid=100.0, seed=0):
        self.grid = float(grid)
        self.seed = int(seed)

    def noise(self, x, y):
        """单点噪声"""
        return perlin(x + self.seed * 1000.0,
                      y + self.seed * 1000.0,
                      self.grid)

    def noise_array(self, x0, y0, width, height, scale=1.0):
        """
        批量生成噪声矩阵（需要 numpy）
        返回 shape 为 (height, width) 的 numpy 数组
        """
        if not _HAS_NUMPY:
            raise ImportError("noise_array 需要安装 numpy：pip install numpy")

        xs = np.arange(width, dtype=np.float64) * scale
        ys = np.arange(height, dtype=np.float64) * scale
        X, Y = np.meshgrid(xs, ys)

        X = X + x0 + self.seed * 1000.0
        Y = Y + y0 + self.seed * 1000.0

        return _perlin_np(X, Y, self.grid)
