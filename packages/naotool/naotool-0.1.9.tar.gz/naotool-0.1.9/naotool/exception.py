class BaseError(Exception):
    """自定义异常基类，通用抽象接口"""

    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message if self.message else "An error occurred."


class ImageGetError(BaseError):
    """自定义异常类，用于表示图片获取失败的情况。"""

    link: str
    e: Exception

    def __init__(
        self, link: str = "", message: str = "图片获取失败", e: Exception = None
    ):
        self.link = link
        self.e = e
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}. link={self.link}. {self.e}"
