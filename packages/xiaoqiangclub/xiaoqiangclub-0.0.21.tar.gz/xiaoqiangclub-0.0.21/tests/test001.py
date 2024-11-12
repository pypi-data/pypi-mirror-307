async def search_details_links(search_query: str, get_info: bool = False):
    """
    搜索页面获取到详情页链接

    :param search_query: 搜索关键字。
    :param get_info: 是否获取文本内容。
    :return: ([详情页链接], [对应的文本内容])搜索词对应的详情链接列表，以及相关链接对应的文本内容列表。
    """
    # 取标题
    links = []
    title = search_query.split('：')[0].strip()
    title = title.split(':')[0].strip()
    title_len = len(title) + 1

    # 循环3次
    while True:
        title_len -= 1
        search_query = title[:title_len]
        log.debug(f"搜索关键字: {search_query}")
        data = {
            "show": "title",
            "tempid": "1",
            "tbname": "article",
            "mid": "1",
            "dopost": "search",
            "submit": "",
            "keyboard": search_query  # 限制搜索关键字长度为6
        }

        url = "https://www.xb6v.com/e/search/index.php"

        response = await get_response_async(url, parse=False, json_data=False, retry_times=1, sleep_time=SLEEP_TIME,
                                            cookies=None, headers=HEADERS, timeout=10, verify=False, is_get=False,
                                            follow_redirects=True, data=data)

        if not response or response.status_code != 200:
            try:
                # 如果请求失败，重定向到备用 URL
                url = "https://www.66s6.cc/e/search/index.php"
                response = await get_response_async(url, parse=False, json_data=False, retry_times=1,
                                                    sleep_time=SLEEP_TIME,
                                                    cookies=None, headers=HEADERS, timeout=10, verify=False,
                                                    is_get=False,
                                                    follow_redirects=True, data=data)
                if not response or response.status_code != 200:
                    return [], []
            except Exception as e:
                log.warning(f"请求失败: {e}")
                return [], []

        check_strings = ["没有搜索到相关的内容", "系统限制的搜索关键字只能在"]
        if any(string in response.text for string in check_strings):
            if title_len < 2:
                return [], []
        else:
            log.debug(f"搜索6v资源结果页面：{response.url}")
            # 使用 parsel 提取链接
            selector = Selector(response.text)

            async def get_links(s: Selector):
                """
                提取详情页面链接
                """
                url_list = s.css('#post_container li div.article a::attr(href)').getall()
                # 拼接url
                links.extend([urljoin(str(response.url), link) for link in url_list])

            await get_links(selector)
            while True:
                # 判断是否有下一页
                next_url = selector.xpath("//a[contains(text(),'下一页')]/@href").get()
                if next_url:
                    # 拼接路径，提取url的base_url与next_url拼接
                    next_url = urljoin(str(response.url), next_url)
                    log.debug(f"正在请求下一页: {next_url}")
                    selector = await get_response_async(next_url, parse=True, json_data=False, retry_times=1,
                                                        sleep_time=SLEEP_TIME,
                                                        cookies=None, headers=HEADERS, timeout=10, verify=False,
                                                        is_get=False,
                                                        follow_redirects=True)
                    await get_links(selector)
                else:
                    log.debug("已到达最后一页")
                    break

            # 提取文本内容
            text_list = []
            if get_info:
                p_list = selector.css('#post_container li div.article p')
                for p in p_list:
                    text = p.css('::text').getall()
                    # 去除空格去除一些无效字符，使用|分隔拼接成一个字符串
                    text = ''.join(text).replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '').replace(
                        '\u3000', ' ')
                    text_list.append(text)
            return links, text_list

