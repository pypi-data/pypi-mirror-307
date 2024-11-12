from typing import Callable


def tight(
    s1: list[str] | str, sep1: str = "\n", sep2: str = " ", ext_func: Callable = None
) -> str:
    """去除大部分空白字符，自定义1、2级分隔符

    Args:
        s_list (list[str]): 原始str list
        sepa1 (str, optional): 1级别分隔符, 用于分隔拼接原始字符串列表. Defaults to "\\n".
        sepa2 (str, optional): 2级别分隔符, 用于分隔拼接原始字符串。Defaults to " ".
        ext_func (Callable, optional): 自定义过滤函数。Defaults to `None`
    Returns:
        str:
    """
    if isinstance(s1, list):
        return sep1.join(
            ext_func(
                sep2.join(ext_func(s3.strip()) for s3 in s2.split(sep2) if s3.strip())
            )
            for s2 in s1
            if s2.strip()
        )
    elif isinstance(s1, str):
        return sep1.join(
            ext_func(
                sep2.join(ext_func(s3.strip()) for s3 in s2.split(sep2) if s3.strip())
            )
            for s2 in s1.split(sep1)
            if s2.strip()
        )
    raise TypeError(s1, "only support type str, list[str]")


if __name__ == "__main__":
    s = """   去除大部分
    空     白    字        符，
    自定义1、2级分隔符
    """
    s = tight(s)
    print(s)
