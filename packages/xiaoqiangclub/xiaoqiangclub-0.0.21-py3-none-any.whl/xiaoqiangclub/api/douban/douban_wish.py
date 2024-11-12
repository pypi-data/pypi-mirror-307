# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/11 11:22
# 文件名称： douban_wish.py
# 项目描述： 豆瓣平台相关接口：https://feizhaojun.com/?p=3813&link2key=8a7b3bc570
# 开发工具： PyCharm
import os
import asyncio
from typing import List, Dict, Union
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.utils.decorators import retry
from xiaoqiangclub.utils.network_utils import get_response_async
from xiaoqiangclub.data.file_utils import read_file_async, write_file_async


class DoubanWish:
    def __init__(self, user_ids: Union[str, List[str]] = None):
        """
        初始化豆瓣想看的影视接口。

        :param user_ids: 用户ID：登入豆瓣账号后，可以在 个人主页 页面看到（右上角头像旁边，或者网址链接中获取）
        """
        self.user_ids = [user_ids] if isinstance(user_ids, str) else user_ids or []

    @staticmethod
    async def get_detail_url_data(movie_url: str, get_all_data: bool = False) -> Dict[str, str]:
        """
        获取电影详情页数据。

        :param movie_url: 电影的详情页面链接
        :param get_all_data: 是否获取所有信息
        :return: 电影详情字典
        """
        log.debug(f'正在获取电影信息: {movie_url}')
        selector = await get_response_async(url=movie_url, return_parsel_selector=True, random_ua=True, retry_delay=2,
                                            follow_redirects=True)

        if not selector:
            return {}

        movie_info = {
            'title': selector.css('span[property="v:itemreviewed"]::text').get(),
            '导演': [tag.strip() for tag in selector.css('span:contains("导演") + span.attrs a::text').getall()],
            '主演': [tag.strip() for tag in selector.css('span:contains("主演") + span.attrs a::text').getall()],
            '上映日期': selector.css('span[property="v:initialReleaseDate"]::text').get(),
            '集数': selector.xpath(
                '//span[contains(text(), "集数:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
            '片长': selector.css('span[property="v:runtime"]::text').get() or selector.xpath(
                '//span[contains(text(), "单集片长:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
        }

        # 获取所有详细数据
        if get_all_data:
            movie_info.update({
                '海报': selector.css('#mainpic img::attr(src)').get(),
                '评分': selector.css('.ll.rating_num::text').get(),
                '国家': selector.xpath(
                    '//span[contains(text(), "制片国家/地区:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
                '编剧': [tag.strip() for tag in selector.css('span:contains("编剧") + span.attrs a::text').getall()],
                '类型': [tag.strip() for tag in selector.css('span[property="v:genre"]::text').getall()],
                '语言': selector.xpath(
                    '//span[contains(text(), "语言:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
                '又名': [tag.strip() for tag in (selector.xpath(
                    '//span[contains(text(), "又名:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get() or '').split(
                    '/')],
                'imdb': selector.xpath(
                    '//span[contains(text(), "IMDb:")]/following-sibling::text()[normalize-space() and following-sibling::br][1]').get(),
            })

        return {k: v.strip() if isinstance(v, str) else v for k, v in movie_info.items() if v}

    @staticmethod
    @retry(max_retries=2, delay=2, valid_check=lambda ret: bool(ret))
    async def get_wish_detail_urls(user_id: str) -> List[str]:
        """
        获取用户想看电影的详情页面链接。

        :param user_id: 用户ID
        :return: 电影详情页面链接列表
        """
        base_url = f'https://movie.douban.com/people/{user_id}/wish'
        links, start = [], 0

        while True:
            url = f'{base_url}?start={start}&sort=rating&mode=grid&tags_sort=count'
            try:
                response = await get_response_async(url, retry_delay=2, random_ua=True, return_parsel_selector=True,
                                                    follow_redirects=True)
                if response:
                    selector = response
                    page_links = selector.css('div.info ul li.title a::attr(href)').getall()
                    if not page_links:
                        break  # 如果当前页没有电影信息，说明没有更多页面
                    links.extend(page_links)
                    start += 15  # 翻页，每次增加15个条目
                else:
                    break
            except Exception as e:
                log.warning(f"处理时发生错误: {e}")
                break

        return links

    async def get_all_wish_data(self, user_ids: Union[str, List[str]] = None, print_results: bool = False,
                                save_file_path: str = None, get_all_data: bool = False, skip_existing: bool = True) -> \
            Dict[str, Dict[str, str]]:
        """
        获取所有豆瓣用户想看影视的详细数据。

        :param user_ids: 用户ID列表或单个ID
        :param print_results: 是否打印结果
        :param save_file_path: 保存文件路径
        :param get_all_data: 是否获取所有数据
        :param skip_existing: 是否跳过已存在数据
        :return: 包含电影链接和详情的字典
        """
        if isinstance(user_ids, str):
            user_ids = [user_ids]

        self.user_ids = user_ids or self.user_ids

        if not self.user_ids:
            raise ValueError("请提供用户ID")

        douban_wish_dict = {}
        existing_links = set()
        save_file_path = save_file_path or 'douban_wish_data.json'

        # 检查已保存数据
        if skip_existing and os.path.exists(save_file_path):
            history_data = await read_file_async(save_file_path)
            if history_data:
                existing_links = set(history_data.keys())
                douban_wish_dict.update(history_data)

        # 获取每个用户的电影链接
        users_wish_urls = await asyncio.gather(*[self.get_wish_detail_urls(user_id) for user_id in self.user_ids])

        # 合并所有链接
        all_wish_urls = list({link for wish_urls in users_wish_urls if wish_urls for link in wish_urls})

        # 过滤已经存在的链接
        need_parse_urls = list({link for link in all_wish_urls if link not in existing_links})

        new_data = []

        if need_parse_urls:
            # 获取电影详细信息
            tasks = [self.get_detail_url_data(url, get_all_data) for url in need_parse_urls]
            results = await asyncio.gather(*tasks)
            for link, details in zip(need_parse_urls, results):
                if details:
                    new_data.append(details.get('title').split(' ')[0].strip())
                    douban_wish_dict[link] = details

            # 保存文件
            if douban_wish_dict:
                await write_file_async(save_file_path, douban_wish_dict)

        # 打印结果
        if print_results:
            for link, details in douban_wish_dict.items():
                print(f"详情链接: {link}")
                for key, value in details.items():
                    print(f"{key.capitalize()}: {value}")
                print("-" * 40)

        log.info(
            f'任务完成，共收录"想看的影视" {len(douban_wish_dict)} 部。新收录 {len(new_data)} 部 >>> {" | ".join(new_data)}')
        return douban_wish_dict
