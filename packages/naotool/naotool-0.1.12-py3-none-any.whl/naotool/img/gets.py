import asyncio
from pathlib import Path
from time import sleep
from urllib.request import urlopen

from PIL import Image
from io import BytesIO

from naotool.exception import ImageGetError
from naotool.httpn import AutoCloseAsyncClient


# 最外层接口get，大一统接口
async def get(links: Path | str | list, client=None) -> Image.Image | list[Image.Image]:
    """下载单张图片、或批量图片

    Args:
        links (Path | str | list): 链接列表, 或者链接str, Path
        client (AsyncClient, None): 用户可以自定义client用于代理、反爬等等, 默认不使用代理.

    Returns:
        Image.Image | list[Image.Image]: Image图片,or图片列表
    """
    # 1.统一处理为字符串列表
    one = not isinstance(links, list)
    if isinstance(links, str):
        links = [links]
    if isinstance(links, Path):
        links = [str(links)]
    # 2.处理client
    async with AutoCloseAsyncClient() if not client else client as client:
        imgs = await get_imgs(links, client)
    return imgs[0] if one and imgs else imgs


async def get_local(link: str) -> Image.Image:
    """打开本地图片"""
    if not link.startswith("file:"):
        raise ImageGetError(link, f"\nget_local error.")
    with urlopen(link) as response:
        file_data = response.read()
        return Image.open(BytesIO(file_data)).convert("RGB")


async def get_http(link: str, client: AutoCloseAsyncClient) -> Image.Image:
    """下载网络图片"""
    if not link.startswith("http"):
        raise ImageGetError(link, f"\nget_local error.")
    res = await client.get(link)
    if res.is_error:
        raise ImageGetError(link, f"\nget_http error.")
    return Image.open(BytesIO(res.content)).convert("RGB")


async def get_path(link: str) -> Image.Image:
    return Image.open(Path(link)).convert("RGB")


async def get_img(link: str, client: AutoCloseAsyncClient) -> Image.Image:
    """get一个图片"""
    try:
        if link.startswith("http"):
            return await get_http(link, client)
        elif link.startswith("file"):
            return await get_local(link)
        else:
            return await get_path(link)
    except ImageGetError:
        raise
    except Exception as e:
        raise ImageGetError(link, e=e)


async def get_imgs(links: list[str], client: AutoCloseAsyncClient) -> list[Image.Image]:
    """批量下载图片"""
    img_list = []
    # 并行
    tasks = (get_img(link, client) for link in links)
    res_list = await asyncio.gather(*tasks)
    img_list.extend(filter(None, res_list))
    return img_list


async def test():
    images = await get(
        [
            "https://avatars.githubusercontent.com/u/53679884",
            "https://avatars.githubusercontent.com/u/53679884",
        ]
    )
    images[0].save("tmp.jpg", format="JPEG")


if __name__ == "__main__":
    images = asyncio.run(test())
