import inspect
from inspect import Parameter
from collections.abc import Callable
from functools import wraps


def compat_arg_error(func: Callable = None, rm_None: bool = True) -> Callable:
    """这个装饰器使得函数在接收错误的参数时，仍然正常执行，消除异常。（但不保证完全正确）
    正常情况下，在调用函数时传入了错误参数，Python 会抛出 TypeError 异常。有2种情况：
    1.位置参数：如果你传入了超过函数定义的参数数量，或者传入了一个不接受的位置参数，Python 会报错。
    2.关键字参数：如果你传入了不在函数定义中的关键字参数，Python 也会抛出 TypeError。

    Args:
        func (Callable): 被装饰的函数
        rm_None(bool) : 是否移除为None的参数. (default True)
    Returns:
        Callable: 装饰后的函数
    """
    if func is None:
        return lambda f: compat_arg_error(f)

    @wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        params = signature.parameters
        # 1.过滤掉未定义的关键字参数, 以及None(当rm_None为True)
        filtered_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k in params
            and not (rm_None and v is None)
            and (
                params[k].kind
                in {
                    Parameter.KEYWORD_ONLY,
                    Parameter.VAR_KEYWORD,
                    Parameter.POSITIONAL_OR_KEYWORD,
                }
            )
        }
        # 2.位置参数
        # 2.1.类型检查，自动类型转换
        for i, (k, v) in enumerate(params.items()):
            if i < len(args):
                true_type = v.annotation
                if true_type is not Parameter.empty:
                    try:
                        args[i] = true_type(args[i])  # 尝试转换
                    except (TypeError, ValueError):
                        raise TypeError.with_traceback(
                            f"Warning: arg '{k}' need type{true_type}"
                        )

        # 2.2.数量检查，减少多余参数
        position_param_nums = sum(
            1
            for p in params.values()
            if p.kind
            in {
                Parameter.POSITIONAL_ONLY,
                Parameter.POSITIONAL_OR_KEYWORD,
            }
        )
        if len(args) > position_param_nums:
            args = args[:position_param_nums]

        # 3.正确性检验
        try:
            bound_args = signature.bind_partial(*args, **filtered_kwargs)
            bound_args.apply_defaults()  # 应用默认值
        except TypeError as e:
            raise TypeError(f"TypeError! Bug detected! Please report this issue:\n{e}")
        return func(*bound_args.args, **filtered_kwargs)

    return wrapper


if __name__ == "__main__":

    # 示例用法
    @compat_arg_error
    def example_function(a, b, c=10):
        return a + b + c

    result = example_function("6", 1, 2, "9", 9, d="")  # d 参数将被忽略
    print(result)  # 输出

    # 示例用法2
    @compat_arg_error()
    def example_function2(a, b, c=10):
        return a + b + c

    # 测试
    result2 = example_function2("", 1, 2, "9", 9, d="")  # d 参数将被忽略
    print(result2)  # 输出
