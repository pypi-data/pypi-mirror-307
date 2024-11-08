# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/26
# 文件名称： decorators.py
# 项目描述： 常用装饰器模块，自动识别同步和异步函数，注意：多个装饰器的执行顺序是从内到外，也就是越靠近原函数的装饰器越先执行。
# 开发工具： PyCharm
import asyncio
import time
import functools
import inspect
from typing import Callable, Any, Optional
from xiaoqiangclub.config.log_config import log


def get_caller_info(depth: int = 2) -> str:
    """
    获取调用者的信息
    :param depth: 堆栈深度，默认值为 2
    :return: 调用者的函数名
    """
    caller_frame = inspect.stack()[depth]
    return caller_frame.function


def get_original_func_str(func_name: str, args: tuple, kwargs: dict) -> str:
    """
    获取原始函数调用的字符串
    :param func_name: 函数名
    :param args: 参数元组
    :param kwargs: 关键字参数字典
    :return: 原始函数调用的字符串
    """
    args_str = ', '.join(repr(arg) for arg in args)
    kwargs_str = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())

    if args_str and kwargs_str:
        original_func = f'{func_name}({args_str}, {kwargs_str})'
    elif args_str:
        original_func = f'{func_name}({args_str})'
    elif kwargs_str:
        original_func = f'{func_name}({kwargs_str})'
    else:
        original_func = f"{func_name}()"

    return original_func


def log_execution_time(func: Callable) -> Callable:
    """
    装饰器：记录函数执行时间
    :param func: 被装饰的函数
    :return: 包装后的函数
    """

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        log.info(f"同步函数：{get_original_func_str(func.__name__, args, kwargs)} 执行时间: {execution_time:.4f} 秒")
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        log.info(f"异步函数：{get_original_func_str(func.__name__, args, kwargs)} 执行时间: {execution_time:.4f} 秒")
        return result

    return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper


def log_function_call(func: Callable) -> Callable:
    """
    装饰器：记录函数调用信息和调用者
    :param func: 被装饰的函数
    :return: 包装后的函数
    """

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        # 获取调用者的信息
        caller_name = get_caller_info(4)
        log.info(f"调用者: {caller_name}, 同步函数: {get_original_func_str(func.__name__, args, kwargs)}")
        return func(*args, **kwargs)

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        # 获取调用者的信息
        caller_name = get_caller_info(4)
        log.info(f"调用者: {caller_name}, 异步函数: {get_original_func_str(func.__name__, args, kwargs)}")
        return await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)

    return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper


def is_valid_return(value: Any) -> bool:
    """
    retry装饰器的valid_check示例参数：
    检查返回值是否有效，即返回值不为 None 且不是异常对象
    :param value: 函数返回的值
    :return: 是否为有效返回值
    """
    return value is not None and not isinstance(value, Exception)


def try_log_exceptions(rethrow: bool = False, no_print_exc_info: bool = False):
    """
    装饰器：执行并捕获记录函数中的异常
    :param rethrow: 是否在捕获到异常后重新抛出异常，注意：抛出异常，函数将不会继续执行。
    :param no_print_exc_info: 是否不输出任何异常信息
    :return: 包装后的函数
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # 获取调用者的信息
            caller_name = get_caller_info(2)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if no_print_exc_info:
                    # 记录错误信息
                    log.error(
                        f"调用者: {caller_name}, 同步函数: {get_original_func_str(func.__name__, args, kwargs)}，报错：{e}",
                        exc_info=False)
                else:
                    exc_info = False if rethrow else True
                    # 记录错误信息
                    log.error(
                        f"调用者: {caller_name}, 同步函数: {get_original_func_str(func.__name__, args, kwargs)}，报错：{e}",
                        exc_info=exc_info)
                    if rethrow:
                        raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 获取调用者的信息
            caller_name = get_caller_info(2)
            try:
                return await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)
            except Exception as e:
                if no_print_exc_info:
                    # 记录错误信息
                    log.error(
                        f"调用者: {caller_name}, 异步函数: {get_original_func_str(func.__name__, args, kwargs)}，报错：{e}",
                        exc_info=False)
                else:
                    exc_info = False if rethrow else True
                    # 记录错误信息
                    log.error(
                        f"调用者: {caller_name}, 异步函数: {get_original_func_str(func.__name__, args, kwargs)}，报错：{e}",
                        exc_info=exc_info)
                    if rethrow:
                        raise

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator


def retry(max_retries: int = 1, delay: float = 1, raise_on_fail: bool = True,
          valid_check: Optional[Callable[[Any], bool]] = None) -> Callable:
    """
    装饰器：重试函数，若函数执行失败或返回无效结果则进行重试
    :param max_retries: 最大重试次数（不包含第一次执行），默认当程序执行错误时重试 1 次。当设置为 0，则不重试。
    :param delay: 每次重试的延迟时间（秒）
    :param raise_on_fail: 是否在函数执行失败时抛出异常，抛出异常后函数将不会继续执行
    :param valid_check: 用于检查函数返回值是否有效的函数，返回 True 表示有效
    :return: 包装后的函数
    """
    assert isinstance(max_retries, int) and max_retries > 0, "max_retries 必须是大于 0 的整数"
    assert isinstance(delay, (int, float)) and delay >= 0, "delay 必须是非负数"

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    # 使用 valid_check 检查结果有效性
                    if valid_check and not valid_check(result):
                        log.warning(
                            f"同步函数：{get_original_func_str(func.__name__, args, kwargs)} 返回无效值: {result}，将进行第 {attempt + 1}/{max_retries} 次重试...")
                        time.sleep(delay)
                        continue
                    return result

                except Exception as e:
                    if attempt == max_retries:
                        log.error(
                            f"同步函数：{get_original_func_str(func.__name__, args, kwargs)} 在 {max_retries} 次重试后仍然失败。")

                        if raise_on_fail:
                            raise

                    log.warning(
                        f"同步函数：{get_original_func_str(func.__name__, args, kwargs)} 报错：{e}, 将进行第 {attempt + 1}/{max_retries} 次重试...")
                    time.sleep(delay)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    result = await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)
                    # 使用 valid_check 检查结果有效性
                    if valid_check and not valid_check(result):
                        log.warning(
                            f"异步函数：{get_original_func_str(func.__name__, args, kwargs)} 返回无效值: {result}，将进行第 {attempt + 1}/{max_retries} 次重试...")
                        await asyncio.sleep(delay)
                        continue
                    return result

                except Exception as e:
                    if attempt == max_retries:
                        log.error(
                            f"异步函数：{get_original_func_str(func.__name__, args, kwargs)} 在 {max_retries} 次重试后仍然失败。")

                        if raise_on_fail:
                            raise

                    log.warning(
                        f"异步函数：{get_original_func_str(func.__name__, args, kwargs)} 报错：{e}, 将进行第 {attempt + 1}/{max_retries} 次重试...")
                    await asyncio.sleep(delay)

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator


def cache_result(func: Callable) -> Callable:
    """
    装饰器：缓存函数的结果，避免重复计算
    :param func: 被装饰的函数
    :return: 包装后的函数
    """
    cache = {}

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        # 生成一个不可变的字典，用作缓存的键
        key = (args, frozenset(kwargs.items()))
        if key in cache:
            # 优化日志输出，使用更清晰的格式
            log.info(f"（同步）使用缓存的结果: {get_original_func_str(func.__name__, args, kwargs)}")
            return cache[key]
        # 调用原函数并缓存结果
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        # 生成一个不可变的字典，用作缓存的键
        key = (args, frozenset(kwargs.items()))
        if key in cache:
            log.info(f"（异步）使用缓存的结果: {get_original_func_str(func.__name__, args, kwargs)}")
            return cache[key]
        # 调用原函数并缓存结果
        result = await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)
        cache[key] = result
        return result

    return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper


def is_valid_credentials(username: str, password: str, correct_username: str, correct_password: str) -> bool:
    """
    validate_before_execution装饰器示例参数。
    验证函数：检查用户的账号和密码是否正确。
    :param username: 用户名
    :param password: 密码
    :param correct_username: 正确的用户名
    :param correct_password: 正确的密码
    :return: 若账号和密码均正确返回 True，否则返回 False
    """
    return username == correct_username and password == correct_password


def default_on_fail() -> None:
    """validate_before_execution中on_fail的默认回调函数：验证失败时的处理，记录日志并返回 None。"""
    log.warning("验证未通过，未执行目标函数。")
    return None


def validate_before_execution(
        validator: Callable[..., bool],
        on_fail: Optional[Callable[[], Any]] = default_on_fail,
        **validator_args: Any  # 允许传入额外的验证参数
) -> Callable:
    """
    装饰器：仅当通过验证函数时，才执行目标函数。

    :param validator: 验证函数，接受与目标函数相同的参数，并返回布尔值。
    :param on_fail: 当验证失败时的回调函数，默认记录日志并返回 None。
    :param validator_args: 额外的参数，传递给 validator 验证函数。
    :return: 包装后的函数。
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 调用验证函数进行检查
            if validator(*args, **validator_args, **kwargs):
                return await func(*args, **kwargs)
            else:
                return on_fail()

        def sync_wrapper(*args, **kwargs):
            # 调用验证函数进行检查
            if validator(*args, **validator_args, **kwargs):
                return func(*args, **kwargs)
            else:
                return on_fail()

        # 检测函数是异步还是同步
        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator
