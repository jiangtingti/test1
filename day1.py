import requests
import pandas as pd
from fake_useragent import UserAgent
import time
import random
import csv
class BilibiliSpider:
    def __init__(self):
        self.url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'

    def get_html(self, url):
        headers = {
            'User-Agent': UserAgent().random
        }
        html = requests.get(url=url, headers=headers).json()
        return html

    def parse_data(self, html):
        data = html['data']['list']
        data_df = pd.DataFrame(data)
        owner_list = data_df['owner'].values.tolist()
        stat_list = data_df['stat'].values.tolist()
        temp_owner = pd.DataFrame(owner_list)
        temp_stat = pd.DataFrame(stat_list)

        # 查看粉丝数
        mid_list = temp_owner['mid'].values.tolist()
        fans_list = self.check_fans(mid_list)
        fans_dict={'fans':fans_list}
        temp_fans = pd.DataFrame(fans_dict)

        # 处理发布时间
        pubdate_list = data_df[['pubdate']].values.tolist()
        pub_localtime_list = []
        for pubdate in pubdate_list:
            temp_time = time.localtime(pubdate[0])
            localtime = str(temp_time[0]) + '-' + str(temp_time[1]) + '-' + str(temp_time[2])
            pub_localtime_list.append(localtime)

        title = html['data']['config']['label']
        weekly_df = data_df[['tname', 'title', 'pubdate', 'desc', 'duration', 'short_link']]
        weekly_df.loc[:, 'pubdate'] = pub_localtime_list
        weekly_df = weekly_df.join(temp_stat['view'])
        weekly_df = weekly_df.join(temp_stat['like'])
        weekly_df = weekly_df.join(temp_stat['coin'])
        weekly_df = weekly_df.join(temp_stat['favorite'])
        weekly_df = weekly_df.join(temp_owner['name'])
        weekly_df = weekly_df.join(temp_fans)

        return weekly_df, title

    def check_fans(self, mid_list):
        fans_list = []
        url = "https://api.bilibili.com/x/web-interface/card?mid={}"

        for mid in mid_list:
            html = self.get_html(url.format(mid))
            time.sleep(random.randint(1, 3))
            fans = html['data']['follower']
            fans_list.append(fans)
        return fans_list

    def run(self):
        pages = input("请输入要爬取的范围：").split(' ')
        pages = [int(i) for i in pages]
        for page in range(pages[0], pages[1] + 1):
            url = self.url.format(page)
            html = self.get_html(url)
            weekly_df, title = self.parse_data(html)
            weekly_df.index = weekly_df.index + 1
            weekly_df.to_excel('D:/output/bilibili/' + title + '.xlsx')
            print(title + "爬取完成！")
            time.sleep(random.randint(3, 5))


if __name__ == '__main__':
    bilibili = BilibiliSpider()
    bilibili.run()
