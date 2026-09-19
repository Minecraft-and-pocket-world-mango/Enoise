# ENoise

一个轻量级柏林噪声（Perlin Noise）库，纯 Python 实现，可选 NumPy 加速。
支持 **Python 3.6.5+**。

- 作者：Minecraft-and-pocket-world-mango
- 邮箱：2929547146@qq.com
- 版本：1.0.1

## 安装

```bash
pip install enoise
```

可选加速：

```bash
pip install enoise[fast]
```

## 快速开始

```python
from enoise import perlin, fbm, Perlin

# 单点噪声
v = perlin(12.3, 45.6, grid=100.0)
print(v)

# 分形噪声
v = fbm(12.3, 45.6, octaves=4, grid=100.0)
print(v)

# 类接口
p = Perlin(grid=80.0, seed=42)
print(p.noise(10, 20))
```

## NumPy 加速

```python
from enoise import fbm_array

noise = fbm_array(0, 0, 800, 600, octaves=4, grid=100.0)
print(noise.shape)   # (600, 800)
```

## 颜色映射

```python
from enoise import colorize

rgb = colorize(0.3, mode="color")
print(rgb)   # (r, g, b)
```

## License

MIT