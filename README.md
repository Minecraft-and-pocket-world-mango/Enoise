# ENoise

一个轻量级柏林噪声（Perlin Noise）库，纯 Python 实现，可选 NumPy 加速。
支持 **Python 3.6.5+**。

- 作者：Minecraft-and-pocket-world-mango
- 邮箱：2929547146@qq.com
- 版本：1.0.1
- 仓库：https://github.com/Minecraft-and-pocket-world-mango/ENoise

---

## 特性

- 纯 Python 核心，零依赖
- 可选 NumPy 加速，批量生成快 100 倍以上
- 支持单点噪声、分形噪声（fBm）、批量矩阵生成
- 自带 HSV / 灰度颜色映射工具
- 函数式 + 类式两套接口

---

## 安装

### 从 GitHub 安装

```bash
pip install git+https://github.com/Minecraft-and-pocket-world-mango/ENoise.git
```

### 本地安装

```bash
git clone https://github.com/Minecraft-and-pocket-world-mango/ENoise.git
cd ENoise
pip install .
```

可选加速（需要 NumPy）：

```bash
pip install .[fast]
```

---

## 快速开始

### 单点噪声

```python
from enoise import perlin

v = perlin(12.3, 45.6, grid=100.0)
print(v)   # 大致在 [-1, 1] 区间
```

### 分形噪声（fBm）

```python
from enoise import fbm

v = fbm(12.3, 45.6, octaves=4, grid=100.0, persistence=0.5)
print(v)
```

### 类接口

```python
from enoise import Perlin

p = Perlin(grid=80.0, seed=42)
print(p.noise(10, 20))
```

---

## NumPy 加速

安装了 NumPy 后，可以一次性生成整张噪声矩阵：

```python
from enoise import fbm_array

noise = fbm_array(
    0, 0, 800, 600,
    octaves=4,
    grid=100.0,
    persistence=0.5,
    scale=1.0,
)
print(noise.shape)   # (600, 800)
```

也可以用 `perlin_np` 直接传数组：

```python
import numpy as np
from enoise import perlin_np

x = np.linspace(0, 100, 200)
y = np.linspace(0, 100, 200)
X, Y = np.meshgrid(x, y)
noise = perlin_np(X, Y, grid=50.0)
```

---

## 颜色映射

```python
from enoise import colorize, hsv_to_rgb

# 噪声值 -> RGB
rgb = colorize(0.3, mode="color")
print(rgb)   # (r, g, b)

# 灰度
gray = colorize(0.3, mode="gray")
print(gray)  # (v, v, v)

# 直接 HSV -> RGB
print(hsv_to_rgb(200, 0.8, 1.0))
```

---

## API 一览

| 函数 / 类 | 说明 |
|-----------|------|
| `perlin(x, y, grid=100.0)` | 二维柏林噪声，单点 |
| `perlin_np(x, y, grid=100.0)` | NumPy 向量化版本 |
| `Perlin(grid, seed)` | 类接口，支持 `noise()` / `noise_array()` |
| `fbm(x, y, octaves, grid, persistence, lacunarity)` | 分形噪声，单点 |
| `fbm2(x, y, ...)` | `fbm` 的二维别名 |
| `fbm3(x, y, z, ...)` | 三维近似分形噪声 |
| `fbm_array(x0, y0, width, height, ...)` | 批量生成矩阵（需 NumPy） |
| `hsv_to_rgb(h, s, v)` | HSV 转 RGB |
| `colorize(value, mode, ...)` | 噪声值转颜色 |

---

## 参数说明

- `grid`：格子大小，越小噪声越密，默认 `100.0`
- `octaves`：分形叠加层数，默认 `4`
- `persistence`：每层振幅衰减，默认 `0.5`
- `lacunarity`：每层频率倍增，默认 `2.0`
- `seed`：随机种子，同一 seed 结果可复现

---

## 示例：生成一张噪声图

```python
from enoise import fbm_array, colorize

W, H = 400, 300
noise = fbm_array(0, 0, W, H, octaves=4, grid=80.0, scale=0.8)

# 转成 RGB 像素列表
pixels = [colorize(v, mode="color") for v in noise.flatten()]
```

配合 Pillow 或 PySide6 就能保存成 PNG。

---

## 兼容性

- Python 3.6.5 及以上
- 无强制依赖
- 可选 NumPy ≥ 1.16

---

## License

MIT
