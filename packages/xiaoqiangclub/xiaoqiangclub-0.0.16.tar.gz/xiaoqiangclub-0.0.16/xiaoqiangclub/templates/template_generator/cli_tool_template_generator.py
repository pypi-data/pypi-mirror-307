# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/3 11:35
# 文件名称： generate_cli_tool_template.py
# 项目描述： 生成命令行工具模板
# 开发工具： PyCharm
import os
import argparse
import shutil


def copy_cli_tool_template(template_name: str = 'cli_tool_template', output_dir: str = None) -> None:
    """
    复制命令行工具模板文件到指定输出目录

    :param output_dir: 输出目录，默认为当前目录
    :param template_name: 模板名称，默认为 'cli_tool_template'
    """
    if output_dir is None:
        output_dir = os.path.abspath(os.getcwd())

    if not os.path.exists(output_dir):
        raise ValueError("输出目录不存在")

    os.makedirs(output_dir, exist_ok=True)

    template_file = os.path.join(os.path.dirname(__file__), 'template_file', f"{template_name}.py")
    if not os.path.exists(template_file):
        raise ValueError(f"模板文件 '{template_name}.py' 不存在")

    destination = os.path.join(output_dir, f"{template_name}.py")
    shutil.copy(template_file, destination)

    print(f"命令行工具模板 '{template_name}.py' 已生成在 '{output_dir}' 目录下。")


def generate_cli_tool_template() -> None:
    """
    主函数，处理命令行参数并生成命令行工具模板
    """
    parser = argparse.ArgumentParser(
        prog='generate_cli_tool_template',
        description='生成命令行工具模板的工具',
        epilog='使用帮助底部显示的内容',
    )
    parser.add_argument('-n', '--name', type=str, default='cli_tool_template',
                        help='模板名称，默认为 "cli_tool_template"')
    parser.add_argument('-d', '--directory', type=str, default='.', help='生成模板的目录路径，默认为当前目录')

    args = parser.parse_args()
    copy_cli_tool_template(args.name, args.directory)


if __name__ == '__main__':
    generate_cli_tool_template()
