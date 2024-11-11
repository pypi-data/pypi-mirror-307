import dataclasses
import functools
import time
from typing import Callable, Tuple

Vector = list[float]

IntTuple = Tuple[int, ...] | None
StrTuple = Tuple[str, ...] | None


@dataclasses.dataclass
class MsgInfo:
    msg: str
    # 0 方法开始, 1 方法执行结尾
    p: int
    cost: float = None
    ex: Exception = None


def logfn(msg_info: MsgInfo):
    if msg_info.ex:
        print(msg_info.msg)
    else:
        print(msg_info.msg)


def log(func=None, /, *, ins: IntTuple = None, inskw: StrTuple = None, out: bool = True,
        logfn: Callable[[MsgInfo], None] = logfn):
    """
    示例:

    >>> @log  # 所有入参将被记录日志
    ... def test1(a,b):
    ...     pass
    ... @log(ins=(2,4), inskw=('name', 'age'), out=False)
    ... def test2(name, age):
    ...     pass

    问题:
        配置的位置参数过滤, 但调用时采用字典参数方式调用, 拦截会失效

    :param func: 被装饰函数. 自动打进来, 属于 Special Variables
    :param ins: args, 指定位置形参那些需要记录日志, 缺省 None 都记录. 可传入字符Tuple, 指定要记录的参数名. `()` 表示都不记录
    :param inskw: kwargs, 字典参数那些需要记录, 参数名, 缺省 None 都记录. 可传入字符Tuple, 指定要记录的参数名. `()` 表示都不记录
    :param out: 是否记录出参日志, 默认记录
    :param logfn: `(msg: str, cost_time: float, ex: Exception) -> None` . 输出info日志的方法, 默认使用 print 输出
    """

    # 无参拿不到 func, 延迟才能拿到, 返回 out_wrapper
    # 有参拿得到 func, 调一下 out_wrapper() 返回 wrapper
    # Tip: 两个 ()(), 无括号装饰, 就补上一个, 有括号装饰, 就不用补

    def parse_log_ins(args, kwargs):
        log_in_args = []
        if ins is None:
            # 记录所有入参
            log_in_args = list(args)
        elif len(ins) > 0:
            for ix, arg in enumerate(args):
                if ix in ins:
                    log_in_args.append(arg)

        log_in_kwargs = {}
        if inskw is None:
            # 记录所有字典参数
            log_in_kwargs = kwargs
        elif len(inskw) > 0:
            for k, v in kwargs.items():
                if k in inskw:
                    log_in_kwargs[k] = v

        return log_in_args, log_in_kwargs

    def out_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            st = time.time()
            log_in_args, log_in_kwargs = parse_log_ins(args, kwargs)
            logfn(MsgInfo(f'[{func.__name__}] begin: [args]: {log_in_args}, [kwargs]: {log_in_kwargs}', 0))
            try:
                res = func(*args, **kwargs)
                res_log = f', [return]: {res}' if out else ''
                cost = time.time() - st
                logfn(MsgInfo(f'[{func.__name__}] end: cost: {cost:.3f}S{res_log}', 1, cost))
                return res
            except Exception as e:
                cost = time.time() - st
                logfn(MsgInfo(f'[{func.__name__}] end: cost: {cost:.3f}S, [exception]: {e}', 1, cost, e))
                raise

        return wrapper

    if func:
        return out_wrapper(func)
    return out_wrapper
