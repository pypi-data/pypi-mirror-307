<div align="center">
  <a href="https://github.com/tomorinao-www">
    <img src="https://avatars.githubusercontent.com/u/53679884" 
    width="300" alt="NaoLogo" 
    style="border-radius: 50%; object-fit: cover;">
  </a>
  <br>

</div>

<div align="center">

# naotool

_✨ 🍬A packge of utils or tools keeps Python sweet. 让 py 保持甜甜的 ✨_

<a href="https://github.com/tomorinao-www/naotool/blob/main/LICENSE">
  <img src="https://img.shields.io/github/license/tomorinao-www/naotool.svg" alt="license:MIT">
</a>
<a href="https://pypi.python.org/pypi/naotool">
  <img src="https://img.shields.io/pypi/v/naotool.svg" alt="pypi">
</a>
<a hred="https://www.python.org/">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python:3.10+">
</a>
<a href="https://github.com/tomorinao-www/naotool">
  <img src="https://img.shields.io/github/stars/tomorinao-www/naotool.svg?style=social">
</a>
 
</div>

# naotool

🍬A packge of utils or tools keeps Python sweet.

# 快速上手

```sh
pip install naotool
```

# 最佳实践

```python
from naotool import deco

@deco.compat_arg_error
def f():
    pass
f(1, 2, 3, a=1)
print("ok!")
```

```python
""" 最佳实践，把一个文件夹内的 .jpg 都重命名为:{md5}.jpg"""
import asyncio
import os
from pathlib import Path
from PIL import Image
from naotool.img.op import img_md5hex
from naotool.img import get

Image.MAX_IMAGE_PIXELS = None
img_dir = Path(r"../../imgs/")
img_name_list = filter(lambda x: x.endswith(".jpg"), os.listdir(str(img_dir)))
path_list = [img_dir / name for name in img_name_list]

async def rename_image(src: Path):
    try:
        md5 = img_md5hex(await get(str(src)))
        new_path = img_dir / f"{md5}{src.suffix}"
        os.rename(src, new_path)
    except Exception as e:
        print(f"Failed to process {src}: {e}")
async def main():
    await asyncio.gather(*(rename_image(src) for src in path_list))
asyncio.run(main())
```

# tools

| module    | example                                 | description        |
| --------- | --------------------------------------- | ------------------ |
| img       | get("http://img.png")                   | 图片               |
| deco      | @deco.compat_arg_error()                | 装饰器             |
| httpn     | AutoCloseAsyncClient(auto_close_time=3) | 更简洁的 http      |
| cls       | copy_attr(a, b)                         | SpringBean (?)     |
| strs      | tight("delete b l a n k char")          | 你的字符串有点松弛 |
| exception | NOException                             | 没有异常           |

# python 设计哲学

- 需求至上原则
- 最小重复原则
- 向后兼容原则
- 数学哲学美学

```py
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
>>>
```

```txt
Python 之禅（作者 Tim Peters）

美优于丑
明确的而不是隐晦的
简单的而不是复杂的
复杂的而不是繁杂的
扁平的而不是嵌套的
稀疏的而不是密集的
可读性至关重要
特例也不能破坏规则
即使假借实用性之名
不应让异常悄悄溜走
除非明确容忍错误
当面临不确定性，不要尝试去猜测
应当只有一种 —— 最好是唯一一种 —— 明显的解决方案
虽然这一开始可能并不容易，除非你是 Dutch
做也许好过不做
但不假思索就动手还不如不做
如果实现是难以解释的，那可能不是个好主意
如果实现是容易解释的，那可能是个好主意
命名空间是一种绝妙的理念 —— 我们要多加利用！
```
