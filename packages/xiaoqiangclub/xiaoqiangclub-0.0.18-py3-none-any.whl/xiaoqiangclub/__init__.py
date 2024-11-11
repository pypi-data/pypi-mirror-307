# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/25 18:06
# 文件名称： __init__.py
# 项目描述： 自用工具包
# 开发工具： PyCharm

# api
from xiaoqiangclub.api.ai.big_model import ZhiPuAIAPI
from xiaoqiangclub.api.ai.chatgpt import (chatgpt, chat_with_chatgpt)
from xiaoqiangclub.api.ai.chatbot import WeChatBotAPI
from xiaoqiangclub.api.ai.spark_lite import SparkLiteAPI
from xiaoqiangclub.api.hao6v import hao6v
from xiaoqiangclub.api.xunlei import xunlei
from xiaoqiangclub.api.xunlei.xunlei import Xunlei
from xiaoqiangclub.api.xunlei.xunlei_base import XunleiBase
from xiaoqiangclub.api.xunlei.xunlei_cloud_disk import XunleiCloudDisk
from xiaoqiangclub.api.xunlei.xunlei_remote_downloader import XunleiRemoteDownloader
from xiaoqiangclub.api.message_sender import (email_sender, wechat_sender, dingtalk_sender, bark_sender,
                                              telegram_sender,
                                              igot_sender, push_plus_sender, an_push_sender, feishu_sender,
                                              discord_sender, whatsapp_sender, async_sender, sender)
from xiaoqiangclub.api.message_sender.sender import MessageSender
from xiaoqiangclub.api.message_sender.async_sender import AsyncMessageSender
from xiaoqiangclub.api.ctfile import Ctfile
from xiaoqiangclub.api.playwright_codegen import (playwright_codegen, install_playwright)

# config
from xiaoqiangclub.config.constants import (VERSION, UA, CURRENT_SYSTEM)
from xiaoqiangclub.config.log_config import (logger_xiaoqiangclub, log)

# data
from xiaoqiangclub.data.deduplication import (Deduplication, dict_list_deduplicate)
from xiaoqiangclub.data.file_utils import (read_file, write_file, read_file_async,
                                           write_file_async, delete_file, clean_filename)
from xiaoqiangclub.data.redis_manager import RedisManager
from xiaoqiangclub.data.sqlite3_manager import (SQLite3Manager, SQLite3DictManager)
from xiaoqiangclub.data.tiny_db import TinyDBManager
from xiaoqiangclub.data.token_manager import (TokenManager, TokenManagerAsync)
from xiaoqiangclub.data import (zip, tiny_db)

# templates
from xiaoqiangclub.templates.template_generator.cli_tool_template_generator import generate_cli_tool_template

# utils
from xiaoqiangclub.utils.decorators import (get_caller_info, log_execution_time, try_log_exceptions,
                                            log_function_call, retry, cache_result, validate_before_execution)
from xiaoqiangclub.utils.encrypt_utils import SimpleCrypto
from xiaoqiangclub.utils.env_var_manager import (set_env_var, get_env_var, load_env, delete_env_var)
from xiaoqiangclub.utils.image_utils import image_to_base64
from xiaoqiangclub.utils.logger import LoggerBase
from xiaoqiangclub.utils.module_installer import (check_and_install_module, check_module, install_module)
from xiaoqiangclub.utils.network_utils import (get_response, get_response_async)
from xiaoqiangclub.utils.qinglong_task_trigger import (minutes_to_time, ql_task_trigger, ql_task_trigger_decorator)
from xiaoqiangclub.utils.regex_validators import RegexValidator
from xiaoqiangclub.utils.terminal_command_executor import (execute_terminal_command, execute_terminal_command_async)
from xiaoqiangclub.utils.text_splitter import text_splitter
from xiaoqiangclub.utils.time_utils import (get_current_weekday, get_current_date, get_current_time, get_full_time_info)

__title__ = "xiaoqiangclub"
__description__ = "一个基于Python3的自用工具包"
__version__ = VERSION

__all__ = [
    # api
    "ZhiPuAIAPI",
    "chatgpt", "chat_with_chatgpt",
    "WeChatBotAPI",
    "SparkLiteAPI",
    "hao6v",
    "xunlei", "Xunlei", "XunleiBase", "XunleiCloudDisk", "XunleiRemoteDownloader",
    "email_sender", "wechat_sender", "dingtalk_sender", "bark_sender", "telegram_sender",
    "igot_sender", "push_plus_sender", "an_push_sender", "feishu_sender", "discord_sender",
    "whatsapp_sender", "async_sender", "sender", "MessageSender", "AsyncMessageSender",
    "Ctfile",
    "playwright_codegen", "install_playwright",

    # config
    "VERSION", "UA", "CURRENT_SYSTEM",
    "logger_xiaoqiangclub", "log",

    # data
    "Deduplication", "dict_list_deduplicate",
    "read_file", "write_file", "read_file_async", "write_file_async", "delete_file", "clean_filename",
    "RedisManager",
    "SQLite3Manager", "SQLite3DictManager",
    "TinyDBManager",
    "TokenManager", "TokenManagerAsync",
    "zip", "tiny_db",

    # templates
    "generate_cli_tool_template",

    # utils
    "log_function_call", "retry", "cache_result", "validate_before_execution",
    "get_caller_info", "log_execution_time", "try_log_exceptions",
    "SimpleCrypto",
    "set_env_var", "get_env_var", "load_env", "delete_env_var",
    "image_to_base64",
    "LoggerBase",
    "check_and_install_module", "check_module", "install_module",
    "get_response", "get_response_async",
    "minutes_to_time", "ql_task_trigger", "ql_task_trigger_decorator",
    "RegexValidator",
    "execute_terminal_command", "execute_terminal_command_async",
    "text_splitter",
    "get_current_weekday", "get_current_date", "get_current_time", "get_full_time_info",
]

# Windows Only
if CURRENT_SYSTEM == "Windows":
    try:
        # gui
        from xiaoqiangclub.gui.autogui import AutoGUI
        from xiaoqiangclub.gui.windows_manager import WindowsManager
        from xiaoqiangclub.gui.show_subtitles import ShowSubtitles
        from xiaoqiangclub.gui import (logo, show_message, show_subtitles, mouse_keyboard_clipboard_listener)
        from xiaoqiangclub.gui.play_system_sound import play_system_sound

        __all__.extend([
            "AutoGUI",
            "WindowsManager",
            "ShowSubtitles",
            "logo", "show_message", "show_subtitles", "mouse_keyboard_clipboard_listener",
            "play_system_sound"
        ])
    except ImportError:
        pass
