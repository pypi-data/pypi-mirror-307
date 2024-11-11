# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 6:13
# 文件名称： file_utils.py
# 项目描述： 常用文件的读写删等工具
# 开发工具： PyCharm
import os
import json
import re
import yaml
import aiofiles
from typing import (Union, Optional, List)
from xiaoqiangclub.config.log_config import log


class FileFormatError(Exception):
    """自定义异常，表示文件格式不支持"""
    pass


def read_file(file_path: str, mode: str = 'r', encoding: str = 'utf-8',
              log_errors: bool = True, by_line: bool = False) -> Union[dict, str, List[str], None]:
    """
    读取文件内容

    :param file_path: 文件路径
    :param mode: 读取模式，支持 'r' 或 'rb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行读取文件，默认为 False
    :return: 文件内容，格式根据文件类型返回不同类型
    """
    try:
        if mode == 'r':
            with open(file_path, 'r', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    return json.load(file)
                elif file_path.endswith(('.yaml', '.yml')):
                    return yaml.safe_load(file)
                elif file_path.endswith('.txt'):
                    if by_line:
                        return file.readlines()  # 按行读取
                    else:
                        return file.read()  # 整体读取
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'rb':
            with open(file_path, 'rb') as file:
                return file.read()
        else:
            log.error(f"不支持的读取模式: {mode}")
            return None

    except Exception as e:
        log_errors and log.error(f"读取文件 {file_path} 时出错: {e}")
        return None


def write_file(file_path: str, content: Union[dict, str], mode: str = 'w', encoding: str = 'utf-8',
               ensure_ascii: bool = False, log_errors: bool = True, by_line: bool = False) -> Optional[bool]:
    """
    写入内容到文件

    :param file_path: 文件路径
    :param content: 要写入的内容，支持字符串或字典
    :param mode: 写入模式，支持 'w' 或 'wb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param ensure_ascii: json文件使用 ASCII 编码，默认为 False
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行写入文件，默认为 False
    :return: 是否写入成功
    """
    try:
        if mode == 'w':
            with open(file_path, 'w', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    json.dump(content, file, ensure_ascii=ensure_ascii, indent=4)
                elif file_path.endswith(('.yaml', '.yml')):
                    yaml.dump(content, file, allow_unicode=True)
                elif file_path.endswith('.txt'):
                    if by_line and isinstance(content, list):
                        file.writelines([line + "\n" for line in content])  # 按行写入
                    else:
                        file.write(content)  # 整体写入
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'wb':
            with open(file_path, 'wb') as file:
                file.write(content)
        else:
            log.error(f"不支持的写入模式: {mode}")
            raise FileFormatError(f"不支持的写入模式: {mode}")
        return True

    except Exception as e:
        log_errors and log.error(f"写入文件 {file_path} 时出错: {e}")
        return False


async def read_file_async(file_path: str, mode: str = 'r', encoding: str = 'utf-8',
                          log_errors: bool = True, by_line: bool = False) -> Optional[Union[dict, str, List[str]]]:
    """
    异步读取文件内容

    :param file_path: 文件路径
    :param mode: 读取模式，支持 'r' 或 'rb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行读取文件，默认为 False
    :return: 文件内容，格式根据文件类型返回不同类型
    """
    try:
        if mode == 'r':
            async with aiofiles.open(file_path, mode='r', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    content = await file.read()
                    return json.loads(content)
                elif file_path.endswith(('.yaml', '.yml')):
                    content = await file.read()
                    return yaml.safe_load(content)
                elif file_path.endswith('.txt'):
                    if by_line:
                        return [line async for line in file]  # 按行读取
                    else:
                        return await file.read()  # 整体读取
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'rb':
            async with aiofiles.open(file_path, mode='rb') as file:
                return await file.read()
        else:
            log.error(f"不支持的读取模式: {mode}")
            raise FileFormatError(f"不支持的读取模式: {mode}")

    except Exception as e:
        log_errors and log.error(f"读取文件 {file_path} 时出错: {e}")
        return None


async def write_file_async(file_path: str, content: Union[dict, str], mode: str = 'w', encoding: str = 'utf-8',
                           ensure_ascii: bool = False, log_errors: bool = True, by_line: bool = False) -> Optional[
    bool]:
    """
    异步写入内容到文件

    :param file_path: 文件路径
    :param content: 要写入的内容，支持字符串或字典
    :param mode: 写入模式，支持 'w' 或 'wb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param ensure_ascii: json文件使用 ASCII 编码，默认为 False
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行写入文件，默认为 False
    :return: 是否写入成功
    """
    try:
        if mode == 'w':
            async with aiofiles.open(file_path, mode='w', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    await file.write(json.dumps(content, ensure_ascii=ensure_ascii, indent=4))
                elif file_path.endswith(('.yaml', '.yml')):
                    await file.write(yaml.dump(content, allow_unicode=True))
                elif file_path.endswith('.txt'):
                    if by_line and isinstance(content, list):
                        await file.writelines([line + "\n" for line in content])  # 按行写入
                    else:
                        await file.write(content)  # 整体写入
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'wb':
            async with aiofiles.open(file_path, mode='wb') as file:
                await file.write(content)
        else:
            raise FileFormatError(f"不支持的写入模式: {mode}")
        return True

    except Exception as e:
        log_errors and log.error(f"写入文件 {file_path} 时出错: {e}")
        return False


def delete_file(file_path: str) -> bool:
    """
    删除指定文件

    :param file_path: 文件路径
    """
    try:
        os.remove(file_path)
        log.info(f"成功删除文件: {file_path}")
        return True
    except Exception as e:
        log.error(f"删除文件 {file_path} 时出错: {e}")
        return False


def clean_filename(filename: str, extra_chars: Union[str, List[str]] = None, replacement: str = '') -> str:
    """
    清理文件名，去除特殊字符，包括反斜杠、正斜杠、冒号、星号、问号、双引号、小于号、大于号、管道符。

    :param filename: 原始文件名，类型为字符串。
    :param extra_chars: 可选参数，可以是一个字符串或者字符串列表，用于指定额外要从文件名中去除的字符。默认为 None。
    :param replacement: 可选参数，用于指定去除特殊字符后用什么字符来代替，默认为空字符串。
    :return: 优化后的文件名，类型为字符串。
    """
    invalid_chars = r'[\\/:*?"<>|]'
    if extra_chars:
        if isinstance(extra_chars, str):
            extra_chars = re.escape(extra_chars)
        elif isinstance(extra_chars, List):
            escaped_additional_chars = [re.escape(char) for char in extra_chars]
            extra_chars = '|'.join(escaped_additional_chars)
        invalid_chars += f'|{extra_chars}'
    return re.sub(invalid_chars, replacement, filename)
