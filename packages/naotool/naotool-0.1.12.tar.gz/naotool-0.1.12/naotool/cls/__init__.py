"""class tools"""

import copy
import time


def copy_attr(
    o: object,
    other: object,
    add_new_attr: bool = True,
    cover: bool = True,
):
    """copy o's attr to other, by deepcopy.

    Args:
        o (object): copy from: o
        other (object): copy to: other
        add_new_attr (bool, optional):whether to add new attr,
        if `other` has not attr. Defaults to True.
        cover (bool, optional): whether to cover the value of `other.attr`,
        if `other.attr` is not None. Defaults to True.
    """
    b1 = add_new_attr
    b3 = cover
    for k, v in vars(o).items():
        b2 = hasattr(other, k)
        b4 = getattr(other, k) is None
        # 2. bool calculate
        if (b1 and ((not b2) or b4)) or (b2 and (b3 or b4)):
            setattr(other, k, copy.deepcopy(v))
        # 1.最普通的方法
        # if b1 and not b2 or b4:
        #     # 如果允许添加新属性 (条件1), 并且没有旧的属性(条件2）或者没有有效的属性（条件4）
        #     setattr(other, k, copy.deepcopy(v))
        # elif b2:  # 如果目标对象含有该属性(条件2)，才可能会赋值
        #     if b3:  # 如果允许覆盖(条件3)，直接拷贝
        #         setattr(other, k, copy.deepcopy(v))
        #     elif b4:  # 如果不允许覆盖，当other.attr为None时(条件4)候拷贝
        #         setattr(other, k, copy.deepcopy(v))


if __name__ == "__main__":

    class T:
        x: int
        y: int

    start = time.time()
    for i in range(1234567):
        a = T()
        a.x = 1
        a.y = 2
        b = T()
        b.x = 1
        b.y = None
        copy_attr(a, b)
    end = time.time()
    print(end - start)
