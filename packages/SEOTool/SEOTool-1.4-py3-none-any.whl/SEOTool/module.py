import requests
from urllib import parse
from fake_useragent import UserAgent
from lxml import html
from time import sleep
from random import uniform

class SEOTool:

    print("SEO小助手Ver1.4 by Tr0nTan\n本脚本无任何反爬手段，大量搜索推荐使用代理隧道\n效率取决于代理和网络")

    def __init__(self, proxyUrl: str = None):
        # 创建User-Agent
        self.ua = UserAgent(browsers=['chrome','edge','firefox'],os=['windows'],platforms=['pc'])
        # 创建代理
        if proxyUrl:
            self.proxies = {
                "http": proxyUrl,
                "https": proxyUrl
            }
        else:
            self.proxies=None

    def request_sender(self, url: str) -> requests.Response:
        '''
        该辅助函数用以发送请求\n
        若直接使用请输入目标url
        '''
        response = None
        try:
            response = requests.get(url, proxies=self.proxies)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            pass
        finally:
            return response

    def baidu_rank_checker(self, search_word: str, targeturl: str) -> tuple:
        '''
        该函数用以查询目标url的百度排名\n
        使用示例：\n
        result = baidu_rank_checker(search_word = '牛战士', targeturl = 'https://www.zhihu.com/question/286807184/answer/3296579670')
        '''
        baidu_url = f'http://www.baidu.com/s?wd={parse.quote(search_word)}&rn={50}'
        mu_pattern = f'mu="{targeturl}"'
        while True:
            sleep(uniform(0,1))
            response = self.request_sender(baidu_url)
            # 响应检测
            if response:
                # 解码
                response.encoding = response.apparent_encoding
                # 标题检测
                if '安全验证' in response.text:
                    continue
                else:
                    pass
                # 目标链接检测
                if mu_pattern in response.text:
                    pass
                else:
                    return (targeturl,'前50无匹配')
                # tree生成
                try:
                    tree = html.fromstring(response.text)
                except:
                    continue
                # 排名列表
                try:
                    ranklist = tree.xpath("//div[@id='content_left' and @tabindex='0']")[0].getchildren()
                except:
                    continue
                # 遍历排行列表
                for item in ranklist:
                    try:
                        url = item.attrib['mu']
                        if url == targeturl:
                            return (targeturl,item.attrib['id'])
                    except:
                        pass
            else:
                pass
    
    def baidu_index_checker(self, targeturl: str) -> tuple:
        '''
        该函数用以查询目标url的百度收录\n
        使用示例：\n
        result = baidu_index_checker(targeturl = 'https://www.zhihu.com/question/286807184/answer/3296579670')
        '''
        baidu_url = f'http://www.baidu.com/s?wd={targeturl}&rn={10}'
        mu_pattern = f'mu="{targeturl}"'
        while True:
            sleep(uniform(0,1))
            response = self.request_sender(baidu_url)
            # 响应检测
            if response:
                # 解码
                response.encoding = response.apparent_encoding
                # 标题检测
                if '安全验证' in response.text:
                    continue
                else:
                    pass
                # 目标链接检测
                if mu_pattern in response.text:
                    return (targeturl,True)
                else:
                    return (targeturl,False)
            else:
                pass

    def baidu_rs_collector(self, search_word: str) -> tuple:
        '''
        该函数用以查询搜索词的百度相关搜索\n
        使用示例：\n
        result = baidu_rs_collector(search_word = '牛战士')
        '''
        baidu_url = f'http://www.baidu.com/s?wd={parse.quote(search_word)}&rn={10}'
        while True:
            response = self.request_sender(baidu_url)
            # 响应检测
            if response:
                # 解码
                response.encoding = response.apparent_encoding
                # 标题检测
                if '安全验证' in response.text:
                    continue
                else:
                    pass
                # 相关搜索检测
                if '相关搜索' in response.text:
                    pass
                else:
                    return (search_word, 'NO_RS')
                # tree生成
                try:
                    tree = html.fromstring(response.text)
                except:
                    print('tree')
                    continue
                # 相关搜索收集
                try:
                    rs = tree.xpath("//a[@class='rs-link_2DE3Q c-line-clamp1 c-color-link']/@title")
                except:
                    rs=[]
                return (search_word, rs)
            else:
                pass
