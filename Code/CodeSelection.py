# coding=UTF8
import os
import requests
import json
from git import Repo

def get_GPT_result(title):
    # 免费gpt调用参数
    headers = {
        'authority': 'api.binjie.fun',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://c.binjie.fun',
        'referer': 'https://c.binjie.fun/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    json_data = {
        'prompt': title,
        'userId': '#/chat/1688568173798',
        'network': False,
        'system': '',
        'withoutContext': False,
        'stream': False,
    }
    response = requests.post('https://api.aichatos.cloud/api/generateStream', headers=headers, json=json_data)
    response.encoding = 'utf-8'  # 替换为正确的编码方式
    return response.text

def ChatGpt(content, key):
    # gpt调用参数
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful assistant.',
            },
            {
                'role': 'user',
                'content': content,
            },
        ],
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    content = response.json()
    return content["choices"][0]["message"]["content"]

if __name__ == '__main__':
    # 语言选择
    language = ['python', 'java']
    # 获取仓库存储地址
    localPath = '../ExtractRepositories/'
    for lang in language:
        # 链接文本存储地址
        linksPath = r"../RepositoriesLinks/" + lang + ".txt"
        if os.path.exists(linksPath):
            # 存在就打开
            with open(linksPath, "r", encoding="utf8") as f:
                for line in f.readlines():
                    line = line.replace("\n","")
                    # -------------------付费版----------------------
                    # 询问语句
                    prompt = "代码结构和可读性：检查该项目的代码结构是否清晰、模块化，并且易于理解和维护。一般来说，清洗结构和良好的代码风格可以提高项目的可维护性。功能稳定性：查看项目的READM和文档，了解它所提供的功能、API、使用示例等等。还可以查看项目的issues（问题）页面，以了解是否有未解决的bug或功能请求。如果项目没有明显的问题且功能表现稳定，那么可以认为它具有较好的质量。文档完整性：考虑项目的文档是否详尽清晰，好的文档能够帮助用户更好地理解和使用项目，包括安装说明、用法示例、API参考等等。缺乏文档可能会增加使用难度。社区支持和活跃度：查看项目的社区活动情况，包括提交的PR(合并请求)、解决问题、讨论等等。活跃的社区意味着更有可能得到持续维护和支持，以及及时的修复bug和更新功能。针对以上的标准。对于"+line+"这个项目，根据这几个方面的质量，在1-10分得出一个综合的评分，评分为整数， 只能回答一个json字符串，其中key为综合得分,value为得分，不允许回答任何其他多余的文字"
                    # # chatgpt的key
                    # key = "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"
                    # # 获取gpt回复
                    # result = ChatGpt(prompt, key)
                    # -------------------付费版----------------------

                    # -------------------免费版----------------------
                    # 获取免费gpt回复
                    result = get_GPT_result(prompt)
                    # -------------------免费版----------------------
                    print("github项目地址：" + line)
                    # 格式化回复，用字典存储
                    json_format_response = json.loads(result)
                    print(result)
                    # 取综合得分进行判断
                    if json_format_response["综合得分"] >= 7:
                        segments = line.split('/')
                        # 取仓库名
                        project_name = segments[-1].replace(".git", "")
                        # git clone到仓库
                        Repo.clone_from(line, localPath + project_name + "/")
                        print("已下载")
        else:
            print("该语言的代码函数和注释尚未被筛选和摘取。")



