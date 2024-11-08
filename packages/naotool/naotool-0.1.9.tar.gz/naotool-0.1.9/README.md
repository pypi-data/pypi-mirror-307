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

| module    | example                                 | description                |
| --------- | --------------------------------------- | -------------------------- |
| img       | get()                                   | get 图片                   |
| deco      | @deco.compat_arg_error()                | 装饰器                     |
| httpn     | AutoCloseAsyncClient(auto_close_time=3) | 会话自动关闭，严格规范代理 |
| exception | NOException                             | 自定义异常                 |
