import hashlib
from PIL import Image


def img_md5hex(img: Image.Image) -> str:
    """计算一个图片的md5"""
    # 将图片转换为二进制数据
    img_bytes = img.tobytes()
    # 创建一个MD5哈希对象
    md5_hash = hashlib.md5()
    # 更新哈希对象，img一般不会大，不用分块处理
    md5_hash.update(img_bytes)
    return md5_hash.hexdigest()
