# PL-NL-Selection

## 项目简介
针对提供项目题目三，开发的一个小项目。该项目为一个基于python的对GitHub开源库中高质量代码和对应注释的挖掘工具。

## 实现功能
* Python爬虫，爬取GitHub开源库内的项目工程仓库git链接。
* 运用大模型对高质量代码函数和注释进行筛选。
* 可以实现多种编程语言的筛选。

## 运行结果
首先，运行ExtractCode.py文件，获取链接均被print出来（如下），最终每种编程语言获取1000个项目工程git链接。在RepositoriesLinks文件夹下，获取的链接根据编程语言不同存放在不同的txt文件中。
  ```
  https://github.com/Snailclimb/JavaGuide.git
  https://github.com/facebook/react-native.git
  https://github.com/iluwatar/java-design-patterns.git
  https://github.com/MisterBooo/LeetCodeAnimation.git
  https://github.com/doocs/advanced-java.git
  https://github.com/spring-projects/spring-boot.git
  https://github.com/macrozheng/mall.git
  https://github.com/elastic/elasticsearch.git
  https://github.com/GrowingGit/GitHub-Chinese-Top-Charts.git
  https://github.com/kdn251/interviews.git
  https://github.com/TheAlgorithms/Java.git
  https://github.com/spring-projects/spring-framework.git
  https://github.com/google/guava.git
  https://github.com/ReactiveX/RxJava.git
  https://github.com/square/retrofit.git
  https://github.com/NationalSecurityAgency/ghidra.git
  ...
  ```
其次，运行CodeSelection.py，利用ChatGPT依次检查获取的链接中的工程项目是否符合设定的高质量代码标准，根据返回的综合评分，决定是否下载该项目代码，大于7分则下载（print结果如下）。
  ```
  github项目地址：https://github.com/public-apis/public-apis.git
  {"综合得分": 8}
  已下载
  github项目地址：https://github.com/donnemartin/system-design-primer.git
  {"综合得分": 9}
  已下载
  github项目地址：https://github.com/vinta/awesome-python.git
  {"综合得分": 10}
  已下载
  ...
  ```

## 使用技术
整体思路为两层筛选，筛选出高质量的代码以及对应的注释。
* **第一层筛选方法**：通过python脚本对GitHub开源库里的代码进行爬取，限定两个选择条件，一个是编程语言、另一个是星级数（主要筛选星级数大于1000的工程项目代码）。爬取GitHub中经过上述筛选搜索出来的仓库名，通过字符串拼接成git clone的HTTPS链接，以便后续下载文件。

* **第二层筛选方法**：通过调用ChatGPT的API，在询问语句中限定对包含注释的代码的评分标准，ChatGPT根据历史训练数据，对整个工程项目进行评分。最后筛选综合得分大于7的项目代码，然后git clone下来。询问prompt以及ChatGPT回复如下。（**注：由于OpenAI的API key限额，我运用了一个免费的类ChatGPT模型进行测试，网址 https://c.binjie.fun**）
  ```
  prompt = "代码结构和可读性：检查该项目的代码结构是否清晰、模块化，并且易于理解和维护。一般来说，清洗结构和良好的代码风格可以提高项目的可维护性。
            功能稳定性：查看项目的READM和文档，了解它所提供的功能、API、使用示例等等。还可以查看项目的issues（问题）页面，以了解是否有未解决的bug或功能请求。如果项目没有明显的问题且功能表现稳定，那么可以认为它具有较好的质量。
            文档完整性：考虑项目的文档是否详尽清晰，好的文档能够帮助用户更好地理解和使用项目，包括安装说明、用法示例、API参考等等。缺乏文档可能会增加使用难度。
            社区支持和活跃度：查看项目的社区活动情况，包括提交的PR(合并请求)、解决问题、讨论等等。活跃的社区意味着更有可能得到持续维护和支持，以及及时的修复bug和更新功能。
            针对以上的标准。对于"+line+"这个项目，根据这几个方面的质量，在1-10分得出一个综合的评分，评分为整数， 只能回答一个json字符串，其中key为综合得分,value为得分，不允许回答任何其他多余的文字。"
  result = '{"综合得分": 7}' #ChatGPT的最终回复
  ```

## 难点及解决办法
* **难点**：爬虫步骤中，对于获取的HTML文本，无法直接爬取相应的项目git链接。**解决办法**：通过找到所有包含文件名链接a标签，找到共有类class，通过类名获取该类下的文本，即为文件名，然后再用字符串拼接成相应的git链接。（**注：在测试过程中发现登录态和非登录态以及白天和夜晚html页面的具体标签会发生变化**）
* **难点**：很多时候写给ChatGPT的prompt，最终得到的答复比较冗长，并且对高质量代码的判定标准很含糊。**解决办法**：确定精确的对于高质量代码的描述以及严格限定回答的规范。

## 额外调研
以上针对题目三开发的小项目或许并不是很优秀的解答，今后在实践过程中需要更好的优化。优化方案有：
* **运用CodeBERT模型进行更细粒度的筛选**：在获取的项目工程文件中，提取相关的代码文件，对代码文本进行预处理，分离注释和代码，运用CodeBERT模型分别对代码文本和注释文本进行矢量表征，然后算两者相似度，达到一定相似度以上，则提取出来，作为筛选结果。
* **通过矢量化表征整个工程文件**：现阶段的项目，只能识别19年之前（训练数据截止于2019年）的工程文件，会有部分文件识别疏漏（19年之后）。可以运用ChatGPT的API，获取矢量表征的整个工程文件并放入大模型中与询问语句进行匹配，最终获取代码质量评分，可以弥补部分疏漏。