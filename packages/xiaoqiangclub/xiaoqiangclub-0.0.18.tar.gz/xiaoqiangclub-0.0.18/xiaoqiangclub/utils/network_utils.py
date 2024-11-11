# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 8:50
# 文件名称： network_utils.py
# 项目描述： 网络工具模块，提供发送 HTTP 请求并返回响应的功能，包括同步和异步版本。
# 开发工具： PyCharm
import time
import httpx
import asyncio
from httpx import Limits
from parsel import Selector
from xiaoqiangclub.config.log_config import log
from typing import (Any, Optional, Union, Dict, Tuple)

VALID_REQUEST_METHODS = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'}


def format_method(method: Optional[str], data: Optional[dict], json: Optional[Union[dict, str]]) -> str:
    """格式化请求方法为大写，并验证是否合法。"""
    if method is None:
        # 根据 data 和 json 判断请求方法
        if data or json:
            return 'POST'
        return 'GET'
    method_upper = method.upper()
    if method_upper not in VALID_REQUEST_METHODS:
        raise ValueError(f"无效的请求方法: {method}. 允许的方法包括: {', '.join(VALID_REQUEST_METHODS)}")
    return method_upper


def handle_error(e: Exception, attempt: int, retries: int, raise_on_failure: bool, logger: Any) -> None:
    """处理错误的通用函数。

    :param e: 异常对象
    :param attempt: 当前尝试次数
    :param retries: 最大重试次数
    :param raise_on_failure: 是否在失败时抛出异常
    :param logger: 日志记录器
    """
    if attempt == retries:
        if raise_on_failure:
            raise
        if retries > 0:
            logger.error(f"请求错误: {type(e).__name__}: {e}, 已达到最大重试次数 {retries} 次",
                         exc_info=not raise_on_failure)
        else:
            logger.error(f"请求错误: {type(e).__name__}: {e}", exc_info=not raise_on_failure)
    else:
        logger.error(f"请求错误: {type(e).__name__}: {e}, 进行第 {attempt + 1}/{retries} 次重试:...")


def __extract_kwargs(kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    处理 kwargs 参数，返回两个字典：http_client_params 和 request_params。
    :param kwargs: **kwargs 参数
    :return: httpx.Client的参数, client.request的参数
    """

    # 定义默认值
    http_client_default_params = {
        "auth": None,
        "cookies": None,
        "verify": True,
        "cert": None,
        "http1": True,
        "http2": False,
        "proxy": None,
        "proxies": None,
        "mounts": None,
        "timeout": 5.0,
        "limits": Limits(max_connections=100, max_keepalive_connections=20),
        "max_redirects": 20,
        "event_hooks": None,
        "base_url": "",
        "transport": None,
        "app": None,
        "trust_env": True,
    }

    # 从 kwargs 中提取 http_client 参数
    http_client_params = {key: kwargs.pop(key) for key in list(kwargs) if key in http_client_default_params}

    return http_client_params, kwargs


def get_response(
        url: str,
        method: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        retries: int = 0,
        retry_delay: float = 1,
        raise_on_failure: bool = False,
        return_json: bool = False,
        return_parsel_selector: bool = False,
        logger: Optional[Any] = None,
        default_encoding: Optional[str] = None,
        **kwargs: Any
) -> Any:
    """
    发送 HTTP 请求并返回响应。

    :param url: 请求的 URL 地址
    :param method: HTTP 请求方法
    :param session: 使用session发送请求，可传入自定义的session对象
    :param data: 请求体数据
    :param headers: 请求头
    :param retries: 最大重试次数， 默认为 0 次不重试
    :param retry_delay: 重试延迟时间（秒）
    :param raise_on_failure: 失败时是否抛出异常，注意：当抛出异常时，将会终止主线程的执行
    :param return_json: 是否返回 JSON 格式的响应
    :param return_parsel_selector: 是否返回 parsel 选择器对象
    :param logger: 日志记录器
    :param default_encoding: 响应文本编码格式：默认为 utf-8，
                            UTF-8：最常用的编码格式，支持所有字符，包括中文。
                            GBK：常用于简体中文编码，特别是在某些旧版系统中。
                            GB2312：较早的简体中文编码，但支持的字符集较少。
                            ISO-8859-1（Latin-1）：西欧语言的编码，不支持中文。
                            ISO-8859-2：中欧语言的编码，也不支持中文。
                            Shift_JIS：日文编码，适用于日文内容。
                            Big5：繁体中文编码，常用于香港和台湾。
    :param kwargs: 其他请求参数
    :return: HTTP 响应对象或 JSON 数据
    """
    json = kwargs.pop('json', None)  # 兼容json参数
    method = format_method(method, data, json)
    retries = retries if retries and retries > 0 else 0  # 防止负数和None

    if logger is None:
        logger = log

    default_encoding = default_encoding or 'utf-8'  # 默认编码
    http_client_params, request_params = __extract_kwargs(kwargs)
    client = session if session else httpx.Client(default_encoding=default_encoding, **http_client_params)

    for attempt in range(retries + 1):
        logger.debug(f"发送请求: {method} {url}...")
        try:
            response = client.request(method, url, data=data, json=json, headers=headers, **request_params)
            response.raise_for_status()

            if return_json:
                return response.json()
            if return_parsel_selector:
                return Selector(text=response.text)
            return response
        except httpx.HTTPStatusError as e:
            handle_error(e, attempt, retries, raise_on_failure, logger)
        except Exception as e:
            handle_error(e, attempt, retries, raise_on_failure, logger)
        # 等待一段时间再重试
        time.sleep(retry_delay)

    if session is None:  # 不使用自定义session时，需要关闭
        client.close()
    return None


async def __get_response_async(
        url: str,
        method: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        data: Optional[dict] = None,
        retries: int = 0,
        retry_delay: float = 1,
        raise_on_failure: bool = False,
        return_json: bool = False,
        return_parsel_selector: bool = False,
        logger: Optional[Any] = None,
        default_encoding: Optional[str] = None,
        **kwargs: Any
) -> Any:
    """
    异步发送 HTTP 请求

    :param url: 请求的 URL 地址
    :param method: HTTP 请求方法
    :param session: 使用session发送请求，可传入自定义的session对象
    :param data: 请求体数据
    :param retries: 最大重试次数， 默认为 0 次不重试
    :param retry_delay: 重试延迟时间（秒）
    :param raise_on_failure: 失败时是否抛出异常，注意：当抛出异常时，将会终止主线程的执行
    :param return_json: 是否返回 JSON 格式的响应
    :param return_parsel_selector: 是否返回 parsel 选择器对象
    :param logger: 日志记录器
    :param default_encoding: 响应文本编码格式：默认为 utf-8，
                    UTF-8：最常用的编码格式，支持所有字符，包括中文。
                    GBK：常用于简体中文编码，特别是在某些旧版系统中。
                    GB2312：较早的简体中文编码，但支持的字符集较少。
                    ISO-8859-1（Latin-1）：西欧语言的编码，不支持中文。
                    ISO-8859-2：中欧语言的编码，也不支持中文。
                    Shift_JIS：日文编码，适用于日文内容。
                    Big5：繁体中文编码，常用于香港和台湾。
    :param kwargs: 其他请求参数
    :return: HTTP 响应对象或 JSON 数据
    """
    json = kwargs.pop('json', None)
    method = format_method(method, data, json)
    retries = retries if retries and retries > 0 else 0  # 防止负数和None

    if logger is None:
        logger = log

    default_encoding = default_encoding or 'utf-8'  # 默认编码
    http_client_params, request_params = __extract_kwargs(kwargs)

    async_client = session if session else httpx.AsyncClient(default_encoding=default_encoding, **http_client_params)

    for attempt in range(retries + 1):
        try:
            logger.debug(f"发送异步请求: {method} {url}...")
            response = await async_client.request(method, url, data=data, json=json, **request_params)
            response.raise_for_status()

            if return_json:
                return response.json()
            if return_parsel_selector:
                return Selector(text=response.text)
            return response
        except httpx.HTTPStatusError as e:
            handle_error(e, attempt, retries, raise_on_failure, logger)
        except Exception as e:
            handle_error(e, attempt, retries, raise_on_failure, logger)
        # 等待一段时间再重试
        await asyncio.sleep(retry_delay)

    if session is None:  # 不使用自定义session时，需要关闭
        await async_client.aclose()

    return None


async def get_response_async(
        url: str,
        method: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        data: Optional[dict] = None,
        retries: int = 0,
        retry_delay: float = 1,
        sem: asyncio.Semaphore = None,
        raise_on_failure: bool = False,
        return_json: bool = False,
        return_parsel_selector: bool = False,
        logger: Optional[Any] = None,
        default_encoding: Optional[str] = None,
        **kwargs: Any
) -> Any:
    """
    异步发送 HTTP 请求并返回响应。

    :param url: 请求的 URL 地址
    :param method: HTTP 请求方法
    :param session: 使用session发送请求，可传入自定义的session对象
    :param data: 请求体数据
    :param retries: 最大重试次数， 默认为 0 次不重试
    :param retry_delay: 重试延迟时间（秒）
    :param sem: asyncio.Semaphore对象，用于控制并发请求的数量，默认为 None，不控制并发数量
    :param raise_on_failure: 失败时是否抛出异常，注意：当抛出异常时，将会终止主线程的执行
    :param return_json: 是否返回 JSON 格式的响应
    :param return_parsel_selector: 是否返回 parsel 选择器对象
    :param logger: 日志记录器
    :param default_encoding: 响应文本编码格式：默认为 utf-8，
                    UTF-8：最常用的编码格式，支持所有字符，包括中文。
                    GBK：常用于简体中文编码，特别是在某些旧版系统中。
                    GB2312：较早的简体中文编码，但支持的字符集较少。
                    ISO-8859-1（Latin-1）：西欧语言的编码，不支持中文。
                    ISO-8859-2：中欧语言的编码，也不支持中文。
                    Shift_JIS：日文编码，适用于日文内容。
                    Big5：繁体中文编码，常用于香港和台湾。
    :param kwargs: 其他请求参数
    :return: HTTP 响应对象或 JSON 数据
    """
    if sem:
        async with sem:  # 限制并发请求
            return await __get_response_async(url=url, method=method, session=session, data=data, retries=retries,
                                              retry_delay=retry_delay, raise_on_failure=raise_on_failure,
                                              return_json=return_json, return_parsel_selector=return_parsel_selector,
                                              logger=logger, default_encoding=default_encoding, **kwargs)
    else:
        return await __get_response_async(url=url, method=method, session=session, data=data, retries=retries,
                                          retry_delay=retry_delay, raise_on_failure=raise_on_failure,
                                          return_json=return_json, return_parsel_selector=return_parsel_selector,
                                          logger=logger, default_encoding=default_encoding, **kwargs)
