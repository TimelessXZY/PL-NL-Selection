import time

import requests
from bs4 import BeautifulSoup


def ExtractCode(page, language):
    # curl命令中的参数总结：cookies、headers、params
    cookies = {
        '_octo': 'GH1.1.786653495.1665492107',
        '_device_id': 'c5a177b36bf9d61f295165d653ea9efb',
        'preferred_color_mode': 'light',
        'tz': 'Asia%2FHong_Kong',
        'has_recent_activity': '1',
        'tz': 'Asia%2FHong_Kong',
        'color_mode': '%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D',
        'logged_in': 'no',
        '_gh_sess': '06QuDm1uwWlKAuqT9GUQ5%2B2Kbk5l3P4ZP93T7AqwvY8t3o3e6pZo51mucrA16hVpuX5JXgDSs8SLcv0Yo9%2BW0oqawO7qa%2BDMkU9QnEAZaj7be12D9g8O4D9x5Rh11ZtGhAZ%2Bfr0TWMdeepM6ztZmcEchUcA6ASZXwQws2vNDaGhPeSgfJLgXaIoYr1zXAL4pyijtPOAoo8iiiOp2dJvIn%2BDdbP3y5HP%2BUGFwOdBVzB5A8JXoGEoosIefoajgl4oIcz%2BHgsuP6aP2oG5sguywJ4o8L5tAPprTbw%3D%3D--CJ2Yrc8qeowhfw0K--xquSItYuduUNsETaQel20g%3D%3D',
    }

    headers = {
        'authority': 'github.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,zh;q=0.8',
        'cache-control': 'no-cache',
        # 'cookie': '_octo=GH1.1.786653495.1665492107; _device_id=c5a177b36bf9d61f295165d653ea9efb; preferred_color_mode=light; tz=Asia%2FHong_Kong; has_recent_activity=1; tz=Asia%2FHong_Kong; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; logged_in=no; _gh_sess=06QuDm1uwWlKAuqT9GUQ5%2B2Kbk5l3P4ZP93T7AqwvY8t3o3e6pZo51mucrA16hVpuX5JXgDSs8SLcv0Yo9%2BW0oqawO7qa%2BDMkU9QnEAZaj7be12D9g8O4D9x5Rh11ZtGhAZ%2Bfr0TWMdeepM6ztZmcEchUcA6ASZXwQws2vNDaGhPeSgfJLgXaIoYr1zXAL4pyijtPOAoo8iiiOp2dJvIn%2BDdbP3y5HP%2BUGFwOdBVzB5A8JXoGEoosIefoajgl4oIcz%2BHgsuP6aP2oG5sguywJ4o8L5tAPprTbw%3D%3D--CJ2Yrc8qeowhfw0K--xquSItYuduUNsETaQel20g%3D%3D',
        'pragma': 'no-cache',
        'referer': 'https://github.com/search?q=language%3Apython%2Bstars+%3E+1000',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'p': page,
        'q': 'language:' + language + ' stars:>1000',
        'type': 'repositories',
    }
    # 获取回应
    response = requests.get('https://github.com/search', params=params, cookies=cookies, headers=headers)
    # 创建解析器
    soup = BeautifulSoup(response.text, 'html.parser')
    # 找所有的a标签下的span元素，该元素里的文本为可以拼接为链接
    # SpanTags = soup.find_all('a', class_='v-align-middle') #貌似夜晚mode，html相应的标签会改变
    SpanTags = soup.find_all('span', class_='qaOIC')
    # 链接文本存储
    LinksPath = r"../RepositoriesLinks/" + language + ".txt"
    with open(LinksPath, "a", encoding="utf8") as f:
        for tag in SpanTags:
            # 获取每一个span tag的文本内容
            SpanText = tag.text
            git_link = "https://github.com/" + SpanText + ".git"
            print(git_link)
            f.write(git_link + "\n")


if __name__ == '__main__':
    # 允许搜索的语言
    searchLanguage = ['java', 'python', 'c++', 'c']
    # GitHub token value
    for i in range(1, 100):
        # 选择搜索语言
        ExtractCode(i, searchLanguage[1])
        # 一页停5秒，防止限制
        time.sleep(5)
